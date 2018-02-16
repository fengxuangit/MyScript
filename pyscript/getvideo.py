#!/usr/bin/env python
#!coding:utf-8

import requests
import sys
import os
import json
import time
import datetime
import random
from pprint import pprint
from urlparse import urlparse
from mysql import MySQLHander
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

mysql = MySQLHander()


rootpath = '/root/code/friend/pics'
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
    with open('failed.txt', 'ab') as f:
        data = "{0}\n".format(url)
        f.write(data)


def getjson():
    url = "https://api2.i999.pw/v2/videos/index/"
    for num in xrange(1, 9):
        nurl = "{0}{1}0".format(url, num)
        req = requests.get(nurl, headers=headers)
        data = json.loads(req.text)
        for name in data['data']:
            getsigle(name['id'])


def getsigle(name):
    global mysql
    url = "https://api2.i999.pw/v2/videos/{name}?v=134&lang=CN".format(name=name)
    req = requests.get(url, headers=headers)
    data = json.loads(req.text)
    sql = "INSERT INTO resource VALUES (null, '{title}', '{desc}', '{thumb}', '{url}',{duration}, '{publisher}', {vister}, {likes},{creat_time}, '{up_time}')".format(title=data['title'].encode('utf-8', 'ignore'), desc=data['title'].encode('utf-8', 'ignore'), thumb=data['cover'], url=data['hls'],duration=data['duration'], publisher=json.dumps(data['publisher']), vister=random.randint(4500, 9999), likes=random.randint(500, 2000), creat_time=time.time(), up_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())));
    lastid = mysql.insert(sql)
    sql = "INSERT INTO category_mapping VALUES (null, 1, {rid}, {time})".format(rid=lastid, time=time.time());
    mysql.insert(sql)


def spider(url):
    dcap = dict(DesiredCapabilities.PHANTOMJS)  #设置useragent
    dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')  #根据需要设置具体的浏览器信息
    driver = webdriver.PhantomJS(desired_capabilities=dcap)  #封装浏览器信息
    driver.get(url)   #加载网页
    time.sleep(2)
    html = driver.page_source   #获取网页文本
    driver.quit()
    return html

def getpage():
    source = []
    data = spider("http://dcxzoduioiasiuioe0o0o0.renoushi.org:9005/index.html")
    soup = BeautifulSoup(data, 'lxml')
    for elem in soup.findAll('div', attrs={'class': 'mui-col-xs-6'}):
        tmp = {'thumb': elem.div.img['src'], 'name': elem.div.find_all('span')[0].text.strip().encode('utf-8', 'ignore'),
        'tag1': elem.div.find_all('span')[1].text.strip().encode('utf-8', 'ignore'), 
        'tag2': elem.div.find_all('span')[2].text.strip().encode('utf-8', 'ignore')}
        source.append(tmp)

    return source

def getonepage(res):
    videourl = "http://dsadasdhaj.hzwjyy.org:8082/1/{c}.mp4"
    print res['thumb']
    u = urlparse(res['thumb'])
    p = os.path.basename(u.path)
    c = p[:p.find('.')]
    print "c: {0}".format(c)
    print "spider on page {0}".format(c)
    url = "http://dcxzoduioiasiuioe0o0o0.renoushi.org:9005/Static/detail.html?a=1&res=%2F1%2F{c}&name=%E7%AB%9E%E6%B3%B3%E6%B0%B4%E7%9D%80%E6%92%AE%E5%BD%B1%E4%BC%9A%E3%81%AE%E5%85%A8&tag1=%E5%AD%A6%E7%94%9F&tag2=%E5%BC%BA%E5%A5%B8&cate=%E8%93%9D%E5%85%89&menuindex=0".format(c=c)
    html = spider(url)
    soup = BeautifulSoup(html, 'lxml')
    data = {"screen": [], "comments": [], 'url': videourl.format(c=c)}

    for elem in soup.findAll('div', attrs={'class': 'mui-col-xs-4'}):
        data['screen'].append(elem.img['src'])

    for elem in soup.findAll('div', attrs={'class': 'comment'}):
        data['comments'].append({'headpic': elem.img['src'], 
            'name': elem.find('div', attrs={'class': 'username'}).text.encode('utf-8','ignore'),
            'content': elem.find('div', attrs={'class': 'usermsg'}).text.encode('utf-8','ignore')})

    source = res.copy()
    source.update(data)

    return source


def save2sql(data):
    jsonstr = json.dumps(data)
    with open('video.json', 'ab') as f:
        f.write(jsonstr+",\n")
    print "save done"

def main():
    source = getpage()
    print "index spider ok"
    for res in source:
        data = getonepage(res)
        save2sql(data)

    print "Done"

if __name__ == '__main__':
    main()

