# EntitySearch

## Description
A tool to download and parse web page from search engines like Google. Developed and tested on Windows/Python 3.5.  
Derived from Eric's gopage package.

## Requirements
* Network connected to a VPN outside mainland China.
* Python 3
* textblob package. To install:

		$ pip install -U textblob
		$ python -m textblob.download_corpora

* BeautifulSoup

		$ pip install beautifulsoup4

## Usage

1. Edit a keywords list and store it into a '.txt' file.
2. Use PageSearcher to get corresponding html pages for given queries.
3. Use EntitySearcher to get text and extract relevent sentences from html files generated from Step 2.

## Major Classes

### EntitySearcher

* Description
	
	* Given a list of query keywords, generate sentences that contain given keyword pair.
	
* Example:

		from textblob import TextBlob
		from web_helper import WebHelper
		from google_item_parser import GoogleItemParser
		from bs4 import BeautifulSoup
		from entity_sentence_search import EntitySearcher
		
		entitySearcher = EntitySearcher('search_result', 'sentence_result.txt', 'keywords.txt')
	
		text = 'I like to eat apples. Me too. Let\'s go buy some apples.'
		results = entitySearcher.search_sentences(['buy', 'some apples'], text)
	
		entitySearcher.search_entity()

### PageSearcher
	
* Description
	* Given a list of query keywords, download corresponding web pages from search engines.
* PageSearcher(output\_dir, keyword\_list, search\_helper)
	* output_dir: where your downloaded pages will be stored. PageSearcher will create the folder if needed.
	* keyword\_list: a list of keywords, one for each query.
	* search_helper: depends on which search engine you wanna use(GoogleHelper, BaiduHelper, SogouHelper, etc).
* Example:

		from page_searcher.page_searcher import PageSearcher
		from search_helper.search_helper import GoogleHelper
		keyword_list = ['Tsinghua', 'PKU', 'hello world']
		searcher = PageSearcher('output_dir', keyword_list, GoogleHelper())
		searcher.get_page()
	
###GoogleItemParser

* Description
	* Given the content of a web page from Google, parse the page to the form of a list of items(snippets).
	* Each item is a dict with 'title', 'content', 'cite_url' etc.
* Example
	
		with open('test.html') as f:
			content = f.read()
			parser = GoogleItemParser()
			parser.feed(content)
			item_list = parser.get_items()