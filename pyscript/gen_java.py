#!/usr/bin/env python
# -*- coding: utf-8 -*- # 
__author__ = 'fengxuan'

import os
import sys
import time
import random
import hashlib

xmlstr='''
<activity
            android:name=".ui.activity.add.{name}"
            android:screenOrientation="portrait"
            android:theme="@style/Theme.AppCompat.NoActionBar"></activity>
'''

def md5(str):
    m2 = hashlib.md5()
    m2.update(str)
    return m2.hexdigest()

def main():
    data = ""
    with open('Activity.java') as f:
        data = f.read()

    for i in xrange(101):
        name = "a" + md5(str(time.time() + random.randint(1, 2000))) + "Activity"
        filename = "{0}.java".format(name)

        with open('output/{0}'.format(filename), 'wb') as f:
            f.write(data.replace('fuckclassname', name))

        content = xmlstr.format(name=name)

        with open('output/xml.txt', 'ab') as f:
            f.write(content + "\r\n")


if __name__ == '__main__':
    main()