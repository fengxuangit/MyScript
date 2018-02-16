#!/usr/bin/env python
#!coding:utf-8

import urllib
import urllib2
import requests
import cookielib
import gzip
import time
from bs4 import BeautifulSoup

headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
            "Accept-Encoding":"gzip",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Referer":"http://www.example.com/",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
            }

class Discuz:
    def __init__(self,username,password ,fid,tid,charset):
        self.username = username #这里使用用户名登录，邮箱登录修改post中的
        self.password = password #密码
        self.charset = charset #网页编码方式
        self.fid=fid #论坛板块id
        self.tid=tid #主题帖子id
        self.host = "www.taotujie.vip"  # 主机
        self.discuz_address = "http://www.taotujie.vip/"  #论坛安装地址

        self.url = {
            "index":self.discuz_address,
            "login":self.discuz_address+\
            "member.php?mod=logging&action=login",#登陆地址,获取登录的formhash
            "login_submit":self.discuz_address+\
            "member.php?mod=logging&action=login&loginsubmit=yes&loginhash=Lp2tl&inajax=1",#登陆post的地址
            "reply_submit":self.discuz_address+\
            "forum.php?mod=post&action=reply&fid={0}&tid={1}&extra=page%3D1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1".format(self.fid,self.tid),#回帖post地址
            "article":self.discuz_address+\
            "forum.php?mod=post&action=newthread&fid={0}".format(self.fid),#发布帖子post所需posttime值
            "article_submit":self.discuz_address+\
            "forum.php?mod=post&action=newthread&fid={0}&extra=&topicsubmit=yes".format(self.fid),#发布主题贴的post地址
            "theme":self.discuz_address+\
            "thread-{0}-1-1.html".format(self.tid),#主题帖地址。获取回帖所需posttime值，这里论坛开启了静态url，没开启需修改
        }

    def get_formhash(self,login = "False"):
        #获取登录或发帖所需的formhash值
        import ipdb;ipdb.set_trace()
        # if login =="True":
        self.opener = self.getOpener()
        page = self.opener.open(self.url["login"])
        # else:
        #     page = requests.get(self.url["login"], headers=headers).text
        # page = self.ungzip(page)
        bsObj = BeautifulSoup(page, "lxml")
        formhash_tag = bsObj.find("input", attrs={"name": "formhash"})
        formhash = formhash_tag["value"]
        return formhash

    def get_posttime(self,url):
        #获取回帖或发帖子所需的posttime值
        page = self.opener.open(url)
        page = self.ungzip(page)
        bsObj = BeautifulSoup(page,"lxml")
        posttime_tag = bsObj.find("input", attrs={"name": "posttime"})
        posttime = posttime_tag["value"]
        return posttime
 
    def getOpener(self):
        #处理Cookies，登陆后可以用kookie登陆其他页面
        cookie = cookielib.CookieJar()
        handler=urllib2.HTTPCookieProcessor(cookie)
        # opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
        opener = urllib2.build_opener(handler)
        header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)" ,
            "Host": self.host,
            "Cookie": "UM_distinctid=15f435fd9013b3-04e10763219d0a-49576d-fa000-15f435fd90294; "
                      "CNZZDATA1253317155=1046496923-1508661899-%7C1508678151; pgv_pvi=455603874; "
                      "pgv_info=ssi=s8712194200; ZI7Q_2132_sid=yR68RM; ZI7Q_2132_saltkey=h5Ig4j99;"
                      " ZI7Q_2132_lastrequest=6ff0P%2F6%2BpEop8I10zmBw0stjuLGJcJ22vzu7FNEByg2RhBdVJB3x;"
                      " ZI7Q_2132_lastvisit=1508670775; ZI7Q_2132_lastact=1508680733%09home.php%09misc; "
                      "ZI7Q_2132_nofocus_member=1; ZI7Q_2132_st_p=0%7C1508679452%7C02debf10b832c727039e97a66a7cbc10; "
                      "ZI7Q_2132_visitedfid=83; ZI7Q_2132_viewid=tid_25932; ZI7Q_2132_nofocus_forum=1; ZI7Q_2132_sendmail=1",
            "referer": self.discuz_address,
        }
        headers = []
        for key, value in header.items():
            headers.append((key, value))
        opener.addheaders = headers
        return opener
 
    def ungzip(self,page):
        #处理服务器发回的zip压缩网页
        try:        # 尝试解压
            print('正在解压.....')
            page = gzip.decompress(page)
            print('解压完毕!')
        except:
            print('未经压缩, 无需解压')
        return page
 
    def login(self):
        #登录网站
        login_post_Date = {
            "formhash": self.get_formhash(),
            "loginfield" : "username",
            "username" : self.username,
            "password" : self.password,
            "questionid": 0,
            "answer": "",
            "cookietime" : 2592000,
        }
        self.opener = self.getOpener()
        login_post_date = urllib.urlencode(login_post_Date).encode()#生成登录所需post的数据
        page = self.opener.open(self.url["login_submit"],login_post_date)
        if 'succeedmessage' in page.read().decode(self.charset):
            print("login succeed...")
 
    def reply(self):
        #回复帖子
        # file = open(r"filepath","r")
        # content = file.read()#文件读取发帖子内容
        content = "你好啊,我是帅哥,hello"
        reply_post_Date = {
            "formhash" : self.get_formhash(login ="True"),#获取登陆后的formhas值
            "message" : content,
            "usesig" : "1",
            "subject":"",
            "posttime" : self.get_posttime(url = self.url["theme"]),#从帖子源码获取posttime
        }
        reply_post_date = urllib.urlencode(reply_post_Date).encode()#生成回帖所需post的数据
        time.sleep(7)#我的论坛设置的是查看文章5秒后回帖无需验证，所以要等待7秒
        page = self.opener.open(self.url["reply_submit"],reply_post_date)
        if "succeedhandle" in page.read().decode(self.charset):
            print("reply succeed...")
 
    def article(self):
        #发布主题
        subject=time.strftime('%Y-%m-%d',time.localtime(time.time()))+"精彩足球赛事"
        with open(r"filepath","r") as file:#文件是另一个爬虫生成
            message = file.read()
        theme_post_Date = {
            "subject": subject,
            "allownoticeauthor":"1",
            "message": message,
            "formhash": self.get_formhash(login="True"),
            "usesig": "1",
            "posttime":self.get_posttime(url = self.url["article"]),
            "creditlimit":"",
            "price":"",
            "readperm":"",
            "replycredit_extcredits":"0",
            "replycredit_membertimes":"1",
            "replycredit_random":"100",
            "replycredit_times":"1",
            "replylimit":"",
            "rewardfloor":"",
            "rushreplyfrom":"",
            "rushreplyto":"",
            "save":"",
            "stopfloor":"",
            "tags":"足球",
            "wysiwyg":"1",
        }
        theme_post_date = urllib.parse.urlencode(theme_post_Date).encode()
        time.sleep(2)
        page = self.opener.open(self.url["article_submit"],theme_post_date)
        if "精彩足球赛事" in page.read().decode(self.charset):
            print("post succeed...")
 
if __name__ == "__main__":
    liqiang = Discuz(username="fucktaotu",password="zxcvb123456",fid="98",tid="43836",charset="utf-8")#各个值类中有说明
    liqiang.login()
    liqiang.reply()