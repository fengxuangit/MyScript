#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import time
#tcp,1023,NULL
#none of 1667637 banners matched
#error_banner:152513
def kw_dict(**kwargs):
	print kwargs
    




# files = "/Users/apple/Downloads/banner_matched_1224"

# with open(files) as f:
# 	data = f.read()

# # print data
# result = rege.findall(data)

# with open('/Users/apple/Downloads/banner_matched_1224_result.csv', 'w') as csvfile:
# 	writer = csv.writer(csvfile, dialect="excel")
# 	for line in result:
# 		base = 0.00000
# 		if line[3] != 'none':
# 			base = float(line[3]) / float(int(line[4]) - int(line[5]))
# 		error = float(line[5]) / float(line[4])
# 		print error
# 		writer.writerow([line[0], line[1], line[2], str(base), str(error)])
	# print "done!"

# def main(string):
# 	regex = re.compile("(.*?),(\d{0,5}),(.*?)\n(.*?) of (\d{0,20}) banners matched\nerror_banner:(\d{0,20})[\n]{0,1}")
# 	result = regex.findall(string)



if __name__ == '__main__':
	print kw_dict(a=1,b=2,c=3) 