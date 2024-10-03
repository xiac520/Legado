from flask import Flask, request, jsonify
from book_source_validator import validate_book_source
import json
import requests
import concurrent.futures
import os
from github import Github
from datetime import datetime

app = Flask(__name__)

GH_TOKEN = os.getenv('GH_TOKEN')
GH_REPO = os.getenv('GH_REPO')

def fetch_and_validate_book_source(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        book_source = response.json()
        result = validate_book_source(book_source)
        return url, result
    except Exception as e:
        return url, str(e)

@app.route('/validate', methods=['POST'])
def validate():
    data = request.json
    urls = data.get('urls', [])

    if not urls:
        return jsonify({'error': 'No URLs provided'}), 400

    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        future_to_url = {executor.submit(fetch_and_validate_book_source, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                results[url] = result
            except Exception as e:
                results[url] = str(e)

    # Save results to shuyuan.json
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f'shuyuan_{timestamp}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    # Upload shuyuan.json to GitHub Releases
    g = Github(GH_TOKEN)
    repo = g.get_repo(GH_REPO)
    release = repo.create_git_release(f'shuyuan-{timestamp}', f'Shuyuan {timestamp}', 'Shuyuan validation results', draft=False, prerelease=False)
    with open(filename, 'rb') as f:
        release.upload_asset(filename, label=filename)

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)