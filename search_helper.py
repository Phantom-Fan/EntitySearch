# -*- coding:utf-8 -*-
from web_helper import WebHelper

class SearchHelper:

    __parser__ = None
    __SEARCH_ROOT_URL__ = ''
    __RESULT_DIR_PATH__ = ''

    def __init__(self):
        pass

    @classmethod
    def get_search_page_by_name(cls, name):
        '''
        get html content of the search page as a result of the given name
        :param name: name to be searched on search engine
        :return: html content of search page
        '''
        name = str(name).replace(' ', '+')
        search_url = cls.__SEARCH_ROOT_URL__ + name
        return WebHelper.get_page_content_from_url(search_url)

class GoogleHelper(SearchHelper):
    __RESULT_DIR_PATH__ = 'google'
    __SEARCH_ROOT_URL__ = 'https://www.google.com/search?hl=en&safe=off&q='

class BaiduHelper(SearchHelper):
    __RESULT_DIR_PATH__ = 'baidu'
    __SEARCH_ROOT_URL__ = 'https://www.baidu.com/s?ie=UTF-8&wd='