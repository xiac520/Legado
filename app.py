from flask import Flask, request, render_template, jsonify
import json
import requests
from LegadoParser2.Search import search
from LegadoParser2.BookInfo import getBookInfo
from LegadoParser2.ChapterList import getChapterList
from LegadoParser2.Chapter import getChapterContent
from LegadoParser2.RuleCompile import compileBookSource
from pprint import pprint
import sys

app = Flask(__name__)

def validate_source(bookSource):
    compiledBookSource = compileBookSource(bookSource)
    searchResult = search(compiledBookSource, '我的')
    if searchResult:
        variables = searchResult[0]['variables']
        bookInfo = getBookInfo(compiledBookSource, searchResult[0]['bookUrl'], variables)
    else:
        bookInfo = {}
    if bookInfo:
        variables = bookInfo['variables']
        chapterList = getChapterList(compiledBookSource, bookInfo['tocUrl'], variables)
    else:
        chapterList = []
    if chapterList and len(chapterList) >= 2:
        variables = chapterList[0]['variables']
        bookContent = getChapterContent(compiledBookSource, chapterList[0]['url'], variables, chapterList[1]['url'])
    elif chapterList:
        variables = chapterList[0]['variables']
        bookContent = getChapterContent(compiledBookSource, chapterList[0]['url'], variables)
    else:
        bookContent = {}
    return bool(bookContent)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename.endswith('.json'):
                bookSource = json.load(file)
                result = validate_source(bookSource)
                return render_template('index.html', result=result)
        elif 'url' in request.form:
            url = request.form['url']
            try:
                response = requests.get(url)
                bookSource = response.json()
                result = validate_source(bookSource)
                return render_template('index.html', result=result)
            except Exception as e:
                return render_template('index.html', result=f'获取 JSON 失败: {str(e)}')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)