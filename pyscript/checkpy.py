#!/usr/bin/env python
#!-*- coding:utf-8 -*-

import os
import sys
import re

reg_name = r"'name': '(.*?)',\n"
if len(sys.argv) < 2:
	print "arguments error"
	sys.exit()

checkfile = sys.argv[1]
with open(checkfile) as file:
	for line in file.readlines():
		
			
