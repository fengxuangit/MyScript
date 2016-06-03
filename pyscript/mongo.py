#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient

conn = MongoClient('virtual.ub',27017)
db = conn.work
task = db.task

result = task.find({"banner_name":"tcp_1023_NULL"})


for line in result:
	print line