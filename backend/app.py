from flask import Flask, request, jsonify
from LegadoParser2.Search import search
from LegadoParser2.BookInfo import getBookInfo
from LegadoParser2.ChapterList import getChapterList
from LegadoParser2.Chapter import getChapterContent
from LegadoParser2.RuleCompile import compileBookSource
import json

app = Flask(__name__)

def read_book_source(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.loads(f.read())
    except Exception as e:
        print(f"Error reading book source file: {e}")
        return None

def search_books(compiled_book_source, keyword):
    try:
        search_result = search(compiled_book_source, keyword)
        if search_result:
            return search_result[0]
        else:
            return None
    except Exception as e:
        print(f"Error during search: {e}")
        return None

def get_book_info(compiled_book_source, book_url, variables):
    try:
        book_info = getBookInfo(compiled_book_source, book_url, variables)
        if book_info:
            return book_info
        else:
            return None
    except Exception as e:
        print(f"Error getting book info: {e}")
        return None

def get_chapter_list(compiled_book_source, toc_url, variables):
    try:
        chapter_list = getChapterList(compiled_book_source, toc_url, variables)
        if chapter_list:
            return chapter_list
        else:
            return []
    except Exception as e:
        print(f"Error getting chapter list: {e}")
        return []

def get_chapter_content(compiled_book_source, chapter_url, variables, next_chapter_url=None):
    try:
        book_content = getChapterContent(
            compiled_book_source, chapter_url, variables, next_chapter_url)
        if book_content:
            return book_content
        else:
            return {}
    except Exception as e:
        print(f"Error getting chapter content: {e}")
        return {}

@app.route('/api/search', methods=['POST'])
def perform_search():
    data = request.get_json()
    keyword = data.get('keyword')
    book_source_file = 'booksource.txt'
    book_source = read_book_source(book_source_file)
    if not book_source:
        return jsonify({'error': '无法读取书源文件'}), 500
    compiled_book_source = compileBookSource(book_source)
    search_result = search_books(compiled_book_source, keyword)
    if search_result:
        variables = search_result['variables']
        book_info = get_book_info(
            compiled_book_source, search_result['bookUrl'], variables)
        if book_info:
            chapter_list = get_chapter_list(
                compiled_book_source, book_info['tocUrl'], variables)
            if chapter_list:
                if len(chapter_list) >= 2:
                    variables = chapter_list[0]['variables']
                    book_content = get_chapter_content(
                        compiled_book_source, chapter_list[0]['url'], variables, chapter_list[1]['url'])
                else:
                    variables = chapter_list[0]['variables']
                    book_content = get_chapter_content(
                        compiled_book_source, chapter_list[0]['url'], variables)
                return jsonify({
                    'searchResult': search_result,
                    'bookInfo': book_info,
                    'chapterList': chapter_list,
                    'bookContent': book_content
                })
            else:
                return jsonify({
                    'searchResult': search_result,
                    'bookInfo': book_info,
                    'chapterList': [],
                    'bookContent': {}
                })
        else:
            return jsonify({
                'searchResult': search_result,
                'bookInfo': {},
                'chapterList': [],
                'bookContent': {}
            })
    else:
        return jsonify({
            'searchResult': None,
            'bookInfo': {},
            'chapterList': [],
            'bookContent': {}
        })

if __name__ == '__main__':
    app.run()