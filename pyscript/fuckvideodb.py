#!/usr/bin/env python
#!coding:utf-8

import json
import time
from pprint import pprint
import random
from mysql import MySQLHander
from pinyin import PinYin

mysql = MySQLHander()

def main():
    mysql = MySQLHander()
    p = PinYin()
    p.load_word()
    with open('video.json') as json_file:
        alldata = json.load(json_file)

    for data in alldata:
        sql = "INSERT INTO resource VALUES (null, '', '{title}', '{desc}', '{thumb}', '{url}',{duration}, {vister}, {likes},{creat_time}, '{up_time}')".format(title=data['name'].encode('utf-8', 'ignore'), desc=data['name'].encode('utf-8', 'ignore'), thumb=data['thumb'], url=data['url'],duration=random.randint(80, 120), vister=random.randint(4500, 9999), likes=random.randint(500, 2000), creat_time=time.time(), up_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        rid = mysql.insert(sql)

        for tag in xrange(1, 2):
            tagname = data["tag{0}".format(tag)].encode('utf-8', 'ignore')
            sql = "SELECT id from category WHERE cname='{0}'".format(tagname)
            mysql.query(sql)
            result = mysql.fetchOneRow()
            if not result:
                ename = p.hanzi2pinyin_split(string=tagname, split="-").replace('-', '')
                sql = "INSERT INTO category values(null, '{ename}', '{cname}', {time})".format(ename=ename, cname=tagname, time=int(time.time()))
                tagid = mysql.insert(sql)
                sql = "INSERT INTO category_mapping values(null, {cid}, {rid}, {time})".format(cid=tagid, rid=rid, time=int(time.time()))
                mysql.insert(sql)
            else:
                tagid = result[0]
                sql = "INSERT INTO category_mapping values(null, {cid}, {rid}, {time})".format(cid=tagid, rid=rid, time=int(time.time()))
                mysql.insert(sql)

        for pic in data['screen']:
            sql = "INSERT INTO screenshots values(null, {rid}, '{pic}', {time})".format(rid=rid, pic=pic, time=int(time.time()))
            mysql.insert(sql)

        print "{0} done".format(data['thumb'])

    mysql.close()

def comments():
    mysql = MySQLHander()
    with open('video.json') as json_file:
        alldata = json.load(json_file)

    for data in alldata:
        for comment in data['comments']:
            sql = "INSERT INTO comments VALUES(null, '{thumb}', '{name}', '{content}', {time})".format(thumb=comment['headpic'], name=comment['name'].encode('utf-8', 'ignore'), content=comment['content'].encode('utf-8', 'ignore'), time=int(time.time()))
            mysql.insert(sql)

        print "{0} is done".format(data['thumb'])

    mysql.close()

def savefaled(data):
    with open('failed.txt', 'ab') as f:
        f.write(data + ",\n")


def insert2db(data):
    global mysql
    for movie in data['movie']:
        if not isinstance(movie, dict):
            print movie[0]
            return False

       
        print "insert movie {0}".format(movie['Name'].encode('utf-8', 'ignore'))
        sql = "SELECT id FROM resource WHERE name='{0}'".format(movie['Name'].encode('utf-8', 'ignore'))
        mysql.query(sql)
        result = mysql.fetchOneRow()
        if result:
            print "this girl {0} has been insert ".format(girlname)
            return True

        sql = "INSERT INTO resource VALUES (null, '{name}', '{title}', '{desc}', '{thumb}', '{coverimg}', '', {duration}, {vister},{likes}, {time}, '{up_time}')".format(name=girlname,
            title=movie['Name'].encode('utf-8', 'ignore'),
            desc=movie['Description'].encode('utf-8', 'ignore'),
            thumb=movie['Img'],
            coverimg=movie['CoverImg'],
            duration=random.randint(60, 120),
            vister=random.randint(2133, 5431),
            likes=random.randint(111, 4231),
            time=int(time.time()),
            up_time=time.strftime('%Y-%m-%d', time.localtime(time.time()))
        )

        resourceid = mysql.insert(sql)

        print "resourceid :{0}".format(resourceid)

        sql = "SELECT id FROM nav WHERE cname='{0}'".format(movie['Channel']['Name'].encode('utf-8', 'ignore'))
        mysql.query(sql)
        result = mysql.fetchOneRow()
        if not result:
            sql = "INSERT INTO nav values (null, '{0}', '', {1})".format(movie['Channel']['Name'].encode('utf-8', 'ignore'), int(time.time()))
            navid = mysql.insert(sql)
        else:
            navid = result[0]
        sql = "INSERT INTO nav_mapping values(null, {0}, {1}, {2})".format(navid, resourceid, int(time.time()))
        mysql.insert(sql)

        for category in movie['Class']:
            sql = "SELECT id FROM category WHERE cname='{0}'".format(category['Name'].encode('utf-8', 'ignore'))
            mysql.query(sql)
            result = mysql.fetchOneRow()
            if not result:
                sql = "INSERT INTO category VALUES (null, '', '{cname}', {time})".format(cname=category['Name'].encode('utf-8', 'ignore'), time=int(time.time()))
                cid = mysql.insert(sql)
            else:
                cid = result[0]

            sql = "INSERT INTO category_mapping values(null, {0}, {1}, {2})".format(cid, resourceid, int(time.time()))
            mysql.insert(sql)

        print "movieid {0} has done!".format(movie['MovieID'])

    return True


def insert112db(data):
    global mysql
    print "insert movie {0}".format(data[1])
    sql = "SELECT id FROM resource WHERE title='{0}'".format(data[1])
    mysql.query(sql)
    result = mysql.fetchOneRow()
    if result:
        print "this movie {0} has been insert ".format(data[1])
        return True

    sql = "INSERT INTO resource VALUES (null, '{name}', '{title}', '{desc}', '{thumb}', '', '{url}', {duration}, {vister},{likes}, {time}, '{up_time}')".format(name='麻生希望',
        title=data[1],
        desc=data[1],
        thumb=data[2],
        url=data[0],
        duration=random.randint(60, 120),
        vister=random.randint(2133, 5431),
        likes=random.randint(111, 4231),
        time=int(time.time()),
        up_time=time.strftime('%Y-%m-%d', time.localtime(time.time()))
    )

    resourceid = mysql.insert(sql)

    print "resourceid :{0}".format(resourceid)

    for num in xrange(3, 10):
        sql = "INSERT INTO screenshots values(null, {rid}, '{pic}', {time})".format(rid=resourceid, pic=data[num], time=int(time.time()))
        mysql.insert(sql)
   
    sql = "INSERT INTO nav_mapping values(null, 1, {0}, {1})".format(resourceid, int(time.time()))
    mysql.insert(sql)

    print "movieid {0} has done!".format(data[10].replace('\r\n', ''))

    return True

def updateuser(data):
    girlname = ''
    for movie in data['movie']:
        if movie['Actor']:
            girlname = movie['Actor'][0]['Name'].encode('utf-8', 'ignore')
        else:
            return False
        
        sql = "SELECT id FROM resource WHERE coverimg='{0}' and name=''".format(movie['CoverImg'])
        mysql.query(sql)
        result = mysql.fetchOneRow()
        if not result:
            return False
        rid = int(result[0])
        sql = "update resource set name='{0}' where id={1}".format(girlname, rid)
        mysql.update(sql)
        print "movie id {0} has been update".format(result[0])

def parsejson():
    global mysql
    with open('caoliu.json') as json_file:
        alldata = json.load(json_file)

    for data in alldata:
        updateuser(data)
        print "girl {0} movie has done!\n\n".format(data['girl'])

    mysql.close()


def insertcomment():
    name = []
    comments = []
    with open('name.txt') as f:
        for line in f.readlines():
            name.append(line.replace('\r\n', ''))

    with open('comments.txt') as f:
        for line in f.readlines():
            comments.append(line.replace('\r\n', ''))

    for num in xrange(0, 42):
        headpic = "http://img.baliup.com:81/images/headPic/{0}.jpg".format(num+1)
        sql = "INSERT INTO comments VALUES(null, '{headpic}', '{name}', '{content}', {time})".format(headpic=headpic, name=name[num], content=comments[num], time=int(time.time()))
        mysql.insert(sql)



def main():
    with open('txt/all.txt') as f:
        for line in f.readlines():
            insert112db(line.split('-'))
    print "done"

if __name__ == '__main__':
    insertcomment()









