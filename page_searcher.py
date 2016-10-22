# -*- coding:utf-8 -*-
import os
import random
import time
import json
import sys

from search_helper import GoogleHelper, BaiduHelper

class PageSearcher:

    def __init__(self, result_dir, keyword_list, search_helper):
        self.keyword_list = keyword_list
        self.search_helper = search_helper
        self.result_path = result_dir
        if not os.path.exists(self.result_path):
            os.mkdir(self.result_path)

    def get_page_file_path(self, keyword):
        keyword = keyword.replace('"', '').replace(' ', '_').replace('/', '.')
        if len(keyword) > 50:
            keyword = keyword[0:50]
        path = os.path.join(self.result_path, keyword + '.html')
        return path

    def get_page(self):
        counter = 0
        totnum = len(self.keyword_list)
        for keyword in self.keyword_list:
            counter += 1
            print('[{}/{}]'.format(counter, totnum))
            file_path = self.get_page_file_path(keyword)
            if os.path.exists(file_path):
                print('[EXIST]', keyword)
                continue
            try:
                query_sentence = keyword
                search_page_content = self.search_helper.get_search_page_by_name(query_sentence)
                if search_page_content is None:
                    print('[Error]', self.search_helper, keyword)
                    return False
                search_page_cache_file = open(self.get_page_file_path(keyword), 'w', encoding='utf-8')
                search_page_cache_file.write(search_page_content.decode('utf-8'))
                search_page_cache_file.close()
                time.sleep(random.randint(1, 3))
            except Exception as e:
                if isinstance(e, KeyboardInterrupt):
                    exit()
                else:
                    print(e)

def test():
    result_dir = 'search_result'
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    search_helpers = [GoogleHelper()]
    with open('keywords.txt') as f:
        keyword_list = [line.strip() for line in f.readlines()]
    for search_helper in search_helpers:
        searcher = PageSearcher(result_dir, keyword_list, search_helper)
        searcher.get_page()

if __name__ == '__main__':
    test()