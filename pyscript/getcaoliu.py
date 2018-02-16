#!/usr/bin/env python
#!coding:utf-8

import requests
import time
import json
from mysql import MySQLHander

def getjson():
    url = "http://api.365mtys.com/vodapi.html"
    for num in xrange(1, 9):
        nurl = "{0}{1}0".format(url, num)
        req = requests.get(nurl, headers=headers)
        data = json.loads(req.text)
        for name in data['data']:
            getsigle(name['id'])


def getgirls():
    url = "http://api.365mtys.com/vodapi.html"
    postdata = {"data": '{"Action":"GetActor2","Message":{"PageIndex":2,"PageSize":100}}'}
    req = requests.post(url, data=postdata)
    text = json.loads(req.text)
    girls = []
    i = 0
    for g in text['Message']['Data']:
        if (i > 6):
            girls.append({'pic': g['Pic'], 'Count': g['Count'], 'id': g['ID'], 'name': g['Name']})
        i+=1
    return girls


def videodetails(id):
    url = "http://api.365mtys.com/vodapi.html"
    print "spider movie id {0}".format(id)
    postdata = {"data": '{"Action":"GetMovieInfoByMember","Message":{"MovieID":%s,"MemberID":"2642603","Token":"C4C0B48D783F4411B1373300932B60D0"}}' % (id)}
    req = requests.post(url, data=postdata, headers={"User-Agent": 'Mozilla/5.0 (Linux; U; Android 5.1; zh-cn; m1 metal Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.6 Mobile Safari/537.36'})
    time.sleep(0.1)
    try:
        text = json.loads(req.text)
    except:
        return False

    return text['Message']


def getgirlvideo(data):
    url = "http://api.365mtys.com/vodapi.html"
    pd = '{"Action":"GetMovies","Message":{"PageIndex":1,"ID":[%s],"Data":"","Type":5,"PageSize":100}}' % (data['id'])
    # pd = '{"Action":"GetMovies","Message":{"PageIndex":1,"ID":[%s],"Data":"","Type":5,"PageSize":100}}' % (data)
    postdata = {"data": pd}
    try:
        req = requests.post(url, data=postdata)
        text = json.loads(req.text)
    except:
        return False
    ids = []
    for t in text['Message']['Movies']:
        ids.append(t['MovieID'])

    return ids

def getsigle(name):
    global mysql
    url = "https://api2.i999.pw/v2/videos/{name}?v=134&lang=CN".format(name=name)
    req = requests.get(url, headers=headers)
    data = json.loads(req.text)
    sql = "INSERT INTO resource VALUES (null, '{title}', '{desc}', '{thumb}', '{url}',{duration}, {vister}, {likes},{creat_time}, '{up_time}')".format(title=data['title'].encode('utf-8', 'ignore'), desc=data['title'].encode('utf-8', 'ignore'), thumb=data['cover'], url=data['hls'],duration=data['duration'], vister=random.randint(4500, 9999), likes=random.randint(500, 2000), creat_time=time.time(), up_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    lastid = mysql.insert(sql)
    sql = "INSERT INTO category_mapping VALUES (null, 1, {rid}, {time})".format(rid=lastid, time=time.time());
    mysql.insert(sql)


def save2sql(data):
    jsonstr = json.dumps(data)
    with open('caoliu.json', 'ab') as f:
        f.write(jsonstr+",\n")

    print "save done"


def main():
    # girls = getgirls()
    with open('failed.txt') as f:
        for line in f.readlines():
            ids = getgirlvideo(line.replace('\n', ''))
            if not ids:
                return False
            one = []
            for mid in ids:
                detail = videodetails(mid)
                if not detail:
                    continue
                one.append(detail)
            save2sql({"girl": line.replace('\n', ''), "movie": one})


if __name__ == '__main__':
    main()
