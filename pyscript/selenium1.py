#!/usr/bin/env python
#!coding:utf-8

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
 
dcap = dict(DesiredCapabilities.PHANTOMJS)  #设置useragent
dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')  #根据需要设置具体的浏览器信息
driver = webdriver.PhantomJS(desired_capabilities=dcap)  #封装浏览器信息
driver.get('http://dcxzoduioiasiuioe0o0o0.renoushi.org:9005/index.html')   #加载网页
data = driver.page_source   #获取网页文本
driver.quit()
soup = BeautifulSoup(data, 'lxml')
for elem in soup.findAll('div', attrs={'class': 'mui-col-xs-6'}):
    print elem
