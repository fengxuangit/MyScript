#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import time
import pymongo

files = "/Users/apple/Downloads/banner_matched_1224"

class MongoOpera:
	db = None
	def __init__(self, server="virtual.ub", port=27017):
		try:
			self.mongo = pymongo.MongoClient(server, port)
		except:
			print "database connect Error!"
			sys.exit()


	def update(self, condition, sql):
		try:
			self.db = self.mongo.work[collection]
			self.db.update(condition, sql, True)
		except:
			print "update sql error! checkout!"
			sys.exit()

	def insert(self, collection, sql):
		try:
			self.db = self.mongo.work[collection]
			self.db.insert(sql)
		except:
			print "insert document error!"
			sys.exit()

	def findLastOne(self, collection):
		try:
			self.db = self.mongo.work[collection]
			result = self.db.find().sort("update_time", pymongo.DESCENDING)#{"update_time":-1}).limit(1)
			return result
		except:
			return None


def main(rules):
	regex = re.compile("(.*?),(\d{0,5}),(.*?)\n(.*?) of (\d{0,20}) banners matched\nerror_banner:(\d{0,20})[\n]{0,1}")
	result = regex.findall(rules)
	for line in result:
		matched = 0.00000
		if line[3] != 'none':
			matched = float(line[3]) / float(int(line[4]) - int(line[5]))
		error = float(line[5]) / float(line[4])
		data = {"update_time":int(time.time()), "error_rate":error, "match_rate":matched, "all_banner":line[4]}
		collname = "{0}_{1}_{2}".format(line[0], line[1], line[2])
		conn = MongoOpera()
		old_dt = conn.findLastOne(collname)
		if old_dt != None and old_dt[0]['match_rate'] < matched:
			conn.insert(collname, data)
	print "done!"

if __name__ == '__main__':
	with open(files) as f:
		data = f.read()
	main(data)
