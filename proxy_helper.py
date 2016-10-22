# -*- coding:utf-8 -*-
import random
import socket
from urllib.request import urlopen, ProxyHandler, HTTPHandler, HTTPBasicAuthHandler, build_opener

class ProxyHelper:

    def __init__(self):
        self.proxies = []
        self.request20proxy = ''
        self.request20proxy = 'http://erwx.daili666.com/ip/?tid=558045424788230&num=20&foreign=only'
        self.request1proxy = 'http://erwx.daili666.com/ip/?tid=558045424788230&num=1&foreign=only'
        proxy = urlopen(self.request20proxy)
        for line in proxy.readlines():
            self.proxies.append(line.strip())

    def choose_proxy(self):
        if self.proxies:
            random.shuffle(self.proxies)
            return self.proxies[0]
        proxy = urlopen(self.request1proxy)
        proxy_candidate = proxy.readlines()[0].strip()
        while not self.test_proxy(proxy_candidate):
            proxy = urlopen(self.request1proxy)
            proxy_candidate = proxy.readlines()[0].strip()
        self.proxies.append(proxy_candidate)
        print('Proxy', proxy_candidate, 'is added.')
        return proxy_candidate

    @classmethod
    def test_proxy(cls, proxy_ip):
        socket.setdefaulttimeout(3.0)
        test_url = 'https://www.google.com/search?hl=en&safe=off&q=southpark'
        try:
            proxy = ProxyHandler({'http': 'http://:@' + proxy_ip.decode('ascii')})
            auth = HTTPBasicAuthHandler()
            opener = build_opener(proxy, auth, HTTPHandler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1 WOW64 rv:23.0) Gecko/20130406 Firefox/23.0')]
            f = opener.open(test_url)
        except Exception as e:
            print('Proxy', proxy_ip, 'fails!.', e)
            return False
        if f.getcode() != 200:
            print('Proxy', proxy_ip, 'fails!', f.getcode())
            return False
        print(proxy_ip, 'OK...', f.getcode())
        return True

if __name__ == '__main__':
    proxy_helper = ProxyHelper()
    proxy_ip = proxy_helper.choose_proxy()
    print(proxy_ip)