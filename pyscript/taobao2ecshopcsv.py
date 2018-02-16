#!/usr/bin/env python
#!-*- coding:utf-8 -*-

import csv
import os
import json
import sys
import logging
import time
import urllib2

ecshopformat = ['title', 'goods_numebr', 'pingpai', 'price', 'ourprice', 'integal', 'bigpic', 'detailpic',
'thumbs', 'keywords', 'simpledescribe', 'detaildescribe', 'kucun']

ecshopdata = {'title': '', 'goods_numebr': '', 'pingpai': u'duleisi', 'price': 0, 'ourprice': 0, 'integal': 0, 'bigpic': '', 
'detailpic':'', 'thumbs': '', 'keywords': '', 'simpledescribe': '', 'detaildescribe': '', 'kucun': 0, 'a': '', 
'1': 1, '2': 1, '3': 1, 4: 1, 5: 1, 6: 1, 7: 1}


logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S')

data = []
picsdict = {
	'detailpic': "201705/source_img/",
	'bigpic': "201705/goods_img/",
	'thumbs': "201705/thumb_img/",
}

global position
position = {}

defaultpicpath = "/Users/apple/Downloads/touxiang2.jpg"
outputcsv = "goods_list1.csv"

def defaultpic():
	global defaultpiccontent
	with open(defaultpicpath) as f:
		defaultpiccontent = f.read()



def safe_json_load(json_data):
    try:
        if not json_data:
            return None
        return json.loads(json_data)
    except Exception, e:
        logging.error("%s, data: %s" % (e, json_data))
        return None



def readcsv():
	taobaocsv = "/Users/apple/Downloads/task_data_519700_2.csv"
	reader = csv.reader(file(taobaocsv, 'rb'))

	flag = 0
	data = []
	for line in reader:
		if flag == 0:
			position = checkpositon(line)
			flag = 1
			continue
		oneline = ecshopdata
		for key in ecshopformat:
			if key == 'pingpai':
				continue
			if key == 'bigpic' or key == 'detailpic' and key == 'thumbs':
				pics = safe_json_load(line[position[key]])
				if not pics:
					continue
				else:
					for pic in pics:
						filename = "{0}/{1}".format(picsdict[key], os.path.basename(pic))
						if download(pic, filename):
							logging.info('download compelte!')
							oneline[key] = filename
							break

			if key not in ['bigpic', 'detailpic', 'thumbs']:
				oneline[key] = line[position[key]]
		
		data.append(oneline)

	logging.info('csv parse complete')
	writecsv(data)


def checkpositon(line):
	for col in ecshopformat:
		i = 0
		for row in line:
			if col == row:
				position[col] = i
				break
			i += 1
	return position



def download(source, dest):
	checkdir()
	content = ""
	flag = 1
	try:
		request = urllib2.Request(source)
		response = urllib2.urlopen(request, timeout=4)
		content = response.read()
		logging.info("download pic file ok")
	except:
		content = defaultpiccontent
		flag = 0
		logging.error("download pic file failed use defaultpic")



	with open(dest, 'wb') as f:
		f.write(content)
		logging.info("write pic file ok")

	if flag:
		return True
	return False


def checkdir():
	for dirs in picsdict.keys():
		if not os.path.exists(picsdict[dirs]):
			os.makedirs(picsdict[dirs])


def get_dict_value(value):
	line = []
	for row in ecshopformat:
		line.append(value[row])

	return line


def writecsv(data):
	writer = csv.writer(file(outputcsv, 'wb'))
	logging.info('csv start write')
	for line in data:
		writer.writerow(get_dict_value(line))

	logging.info("write csv ok!")



def main():
	defaultpic()
	readcsv()

if __name__ == '__main__':
	main()