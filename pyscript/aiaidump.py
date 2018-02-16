#!/usr/bin/env python2
# coding=utf-8

import requests
import json
from pprint import pprint

api_addr = "http://api.diej9977.com:888/admin.php/api2/phonelist?channel=701&parentid=70104"


headers = {"User-Agent":"Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; HM NOTE 1LTE Build/KTU84P) AppleWebKit/534.30 \
    (KHTML, like Gecko) Version/4.0 Mobile Safari/534.3"}

def getjson():
    r = requests.get(api_addr, headers=headers)
    data = json.loads(r.text)
    for girl in data['list']:
        print girl['bigpic']

def main():
    getjson()

if __name__ == '__main__':
    main()