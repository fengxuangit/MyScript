#!/usr/bin/env python
#!coding:utf-8

import requests
import os
from urlparse import urlparse
from mysql import MySQLHander


rootpath = 'pics/'
headers = {"User-Agent":"Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"}

def getpic(url):
    print "[*] spider url {0}".format(url)
    r = None
    try:
        r = requests.get(url, timeout=3)
    except:
        recordfailed(url)
        print "[!] requests {0} failed".format(url)
        return None
    save2file(url, r.content)

def save2file(url, content):
    schema = urlparse(url)
    dirs = "{0}{1}".format(rootpath, schema.path[:schema.path.rfind('/')])
    filename = "{0}{1}".format(dirs, schema.path[schema.path.rfind('/'):])
    if not os.path.exists(dirs):
        os.makedirs(dirs)

    with open(filename, 'wb') as f:
        f.write(content)

    print "[!] save file {0} ok".format(filename)

def recordfailed(url):
    with open('failed1.txt', 'ab') as f:
        data = "{0}\n".format(url)
        f.write(data)

def getdata():
    mysql = MySQLHander()
    sql = "select thumb,coverimg from resource";
    mysql.query(sql)
    result = mysql.fetchAllRows()
    mysql.close()
    for line in result:
        getpic(line[0])
        if not line[1]:
            getpic(line[1])


if __name__ == '__main__':
    getdata()

