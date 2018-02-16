#!/usr/bin/env python
#!coding:utf-8

import requests
from bs4 import BeautifulSoup

url = "http://www.taotujie.vip/thread-43836-1-1.html"

def spider(url):
    r = None
    try:
        r = requests.get(url)
    except:
        print "[!] spider the url {0} error".format(url)
        return None

    return r.text



def parse(html):
    soup = BeautifulSoup(html, 'lxml')



def main():
    html = spider(url)
    parse(html)


if __name__ == '__main__':
    main()