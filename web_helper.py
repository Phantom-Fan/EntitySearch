# -*- coding:utf-8 -*-
from proxy_helper import ProxyHelper
from urllib.request import ProxyHandler, HTTPBasicAuthHandler, HTTPHandler, build_opener
from urllib.request import URLError, HTTPError

proxyHelper = ProxyHelper()

class WebHelper:

    def __init__(self):
        pass

    @classmethod
    def get_page_content_from_url(cls, page_url):
        try:
            proxy_ip = 'http://:@' + str(proxyHelper.choose_proxy().decode('ascii'))
            print('Getting content from [', page_url, '], ip =', proxy_ip)
            proxy = ProxyHandler({'http:': proxy_ip})
            auth = HTTPBasicAuthHandler()
            opener = build_opener(proxy, auth, HTTPHandler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1 WOW64 rv:23.0) Gecko/20130406 Firefox/23.0')]
            conn = opener.open(page_url)
            page_content = conn.read()
            return page_content
        except (URLError, HTTPError) as e:
            print('[Error]@WebHelper.get_page_content_from_url:', page_url)
            print(e)
            return None 

if __name__ == '__main__':
    page_content = WebHelper.get_page_content_from_url('https://www.google.com/search?hl=en&safe=off&q=southpark')
    with open('test_result.html', 'w', encoding='utf-8') as f:
        f.write(page_content.decode('utf-8'))