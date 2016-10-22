# -*- coding:utf-8 -*-
import os
import time
import random
import re
from textblob import TextBlob
from web_helper import WebHelper
from google_item_parser import GoogleItemParser
from bs4 import BeautifulSoup

class EntitySearcher:

    def __init__(self, google_page_dir, output_file_name, keywords_filename):
        self.google_page_dir = google_page_dir
        self.output_file_name = output_file_name
        self.html_parser = GoogleItemParser()
        with open(keywords_filename, 'r', encoding='utf-8') as f:
            self.keyword_list = [line.strip() for line in f.readlines()]
        if not os.path.exists(google_page_dir):
            print('[Error] This dir', google_page_dir, 'does not exists.')
            exit()
        else:
            filenames = self.get_filenames_from_dir(google_page_dir)
            self.file_list = [ os.path.join(google_page_dir, filename) for filename in filenames ]
        assert len(self.keyword_list) == len(self.file_list)

    def get_filenames_from_dir(self, input_dir):
        filenames = [ f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return filenames

    def filter_urls(self, url_list):
        filtered_list = []
        illegal_suffix = ['.pdf']
        for url in url_list:
            for suffix in illegal_suffix:
                if url.endswith(suffix):
                    continue
                filtered_list.append(url)
        return filtered_list

    def get_urls(self, filename):
        url_list = []
        content_list = []
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            self.html_parser.feed(content)
            item_list = self.html_parser.get_items()
            for item in item_list:
                url_list.append(item['source_url'])
                content_list.append(item['content'])
        url_list = self.filter_urls(url_list)
        return url_list

    def get_plain_text(self, url):
        text = ''
        try:
            page_content = WebHelper.get_page_content_from_url(url)
            if page_content is None:
                print('[Error]', url)
                return ''
            page_content = page_content.decode('utf-8')
            soup = BeautifulSoup(page_content, 'lxml')
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text()
            # break into lines and remove leading and trailing space on each
            lines = (' '.join(line.strip().split()) for line in text.splitlines())
            text = '\n'.join(lines)
            text = os.linesep.join([s for s in text.splitlines() if s])
            time.sleep(random.randint(1, 3))
        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                exit()
            else:
                print(e)
        return text

    def address_entity(self, entity, index):
        index_str = str(index)
        begin = '<e' + index_str + '>'
        end = '</e' + index_str + '>'
        return begin + entity + end


    def search_sentences(self, entity_pair, query_text):
        '''
        :param entity_pair, a list of strings
               query_text, text search within
        :return a list of sentences that contains entity
        '''
        assert len(entity_pair) == 2
        search_words = set([word.lower() for word in entity_pair])
        blob = TextBlob(query_text)
        matche_candidates = [str(s) for s in blob.sentences if search_words & set(s.words)]
        matches = []
        for match in matche_candidates:
            if all(entity in match for entity in entity_pair):
                res = match.replace(entity_pair[0], self.address_entity(entity_pair[0], 1))
                res = res.replace(entity_pair[1], self.address_entity(entity_pair[1], 2))
                matches.append(res)
        return matches

    def search_entity(self):
        file_counter = 0
        all_sentences = []
        for file in self.file_list:
            url_list = self.get_urls(file)
            entity_string = self.keyword_list[file_counter]
            entity_pair = re.findall('"([^"]*)"', entity_string)
            total_text = ''
            for url in url_list:
                plain_text = self.get_plain_text(url)
                total_text += plain_text
            sentences = self.search_sentences(entity_pair, total_text.lower())
            # print(total_text)
            print(sentences)
            all_sentences.extend(sentences)
            file_counter += 1

def test():
    entitySearcher = EntitySearcher('search_result', 'sentence_result.txt', 'keywords.txt')
    text = 'I like to eat apples. Me too. Let\'s go buy some apples.'
    results = entitySearcher.search_sentences(['buy', 'some apples'], text)
    print(results)
    # entitySearcher.search_entity()

if __name__ == '__main__':
    test()