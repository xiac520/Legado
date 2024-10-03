from LegadoParser2.Search import search
from LegadoParser2.BookInfo import getBookInfo
from LegadoParser2.ChapterList import getChapterList
from LegadoParser2.Chapter import getChapterContent
from LegadoParser2.RuleCompile import compileBookSource

def validate_book_source(bookSource):
    try:
        compiledBookSource = compileBookSource(bookSource)
        search_result = search(compiledBookSource, '我的')
        if not search_result:
            return 'Search validation failed'
        book_info = getBookInfo(compiledBookSource, search_result[0]['bookUrl'], search_result[0]['variables'])
        if not book_info:
            return 'BookInfo validation failed'
        chapter_list = getChapterList(compiledBookSource, book_info['tocUrl'], book_info['variables'])
        if not chapter_list:
            return 'ChapterList validation failed'
        chapter_content = getChapterContent(compiledBookSource, chapter_list[0]['url'], chapter_list[0]['variables'])
        if not chapter_content:
            return 'ChapterContent validation failed'
        return 'Valid book source'
    except Exception as e:
        return str(e)