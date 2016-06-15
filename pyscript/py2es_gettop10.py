#!/usr/bin/env python
#!-*- coding:utf-8 -*-

import threading
import time
import sys
import Queue
import json
import sys
from elasticsearch import Elasticsearch

MRule_Type_List = ['WEBSHELL', 'SQLI', 'XSS', 'CODE', 'EXP', 'LRFI', 'FILEI', 'SPECIAL', 'OTHER', 'SCANNER']

OTHER_List = ['Source_IP', 'MRule_Type']

class Pyes:
    def __init__(self, MRule_Type=None):
        self.conn = Elasticsearch("10.0.8.91:9200")
        self.GetMRuleTypeTop10(MRule_Type) if MRule_Type in MRule_Type_List else self.getOtherTop10Esdata(MRule_Type)

    def getEsdata(self, **kwargs):
        data = self.conn.search(index="dbcenter", doc_type="auditlog" ,body={
            'query':{
                'bool':{
                    "must":[{
                        "range":{"Time":{
                            "gt": kwargs['starttime'],
                            "lt": kwargs['endtime']
                                }
                            }
                        },
                    {
                    "term":{
                        "MRule_Type": kwargs['MRule_Type']
                        }
                    }
                ]
            }
        },
        "from":kwargs['start'],
        "size":kwargs['size']
        })
        return data['hits']['hits'], data['hits']['total']

    def getOtherTop10Esdata(self, field):
        data = self.conn.search(index="dbcenter", doc_type="auditlog" ,body={
            'query':{
                'bool':{
                    "must":[{
                        "range":{"Time":{
                            "gt": starttime,
                            "lt": endtime
                                }
                            }
                        }
                ]
            }
        },
        "aggs":{
            "top-tags" :{
                "terms":{
                    "field":field,
                    "size": 10
                }
            }
        }
        })
        data = data['aggregations']['top-tags']['buckets']
        result = list()
        for line in data:
            tmp = (line['key'], line['doc_count'])
            result.append(tmp)
        self.filesave(result, field)
        del result

    def GetMRuleTypeTop10(self, MRule_Type):
        # for MRule_Type in MRule_Type_List:
        spend = 200
        result = dict()
        data, count = self.getEsdata(starttime=starttime, endtime=endtime, MRule_Type=MRule_Type, start=0, size=1)
        for num in range(0, 10000, spend):
            print "[!] analysis  MRule_Type:{0} in count: {1}".format(MRule_Type, num)
            data, x = self.getEsdata(starttime=starttime, endtime=endtime, MRule_Type=MRule_Type, start=num, size=spend)
            for line in data:
                if result.has_key(line['_source']['Request_Uri']):
                    result[line['_source']['Request_Uri']] += 1
                else:
                    result[line['_source']['Request_Uri']] = 1
        result = sorted(result.iteritems(), key=lambda d:d[1], reverse=True)
        self.filesave(result, MRule_Type)
        del result
        print "\n[!] MRule_Type:{0} has get top 10 ok! \n".format(MRule_Type)

    def filesave(self, data, MRule_Type):

        with open('result.txt', 'ab') as f:
            f.write("{0}: \n".format(MRule_Type))
            if len(data) != 0 and len(data)>=10:
                for num in range(10):
                    content = "{0}    {1}\n".format(data[num][0], data[num][1])
                    f.write(content)
                f.write("\n\n\n")
            elif len(data) > 0  and len(data) < 10:
                for num in range(len(data)):
                    content = "{0}    {1}\n".format(data[num][0], data[num][1])
                    f.write(content)
                f.write("\n\n\n")
            else:
                f.write("no yet!\n\n\n")
        print "[*] MRule_Type:{0} write file ok!\n".format(MRule_Type)


class MyThread(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while not self.queue.empty():
            MRule_Type = self.queue.get()
            Pyes(MRule_Type)
            self.queue.task_done()

def usage():
    usage='''
        {0} starttime  endtime
    '''.format(sys.argv[0])
    if len(sys.argv) < 3:
        print usage
        sys.exit()
    global starttime, endtime 
    starttime = int(sys.argv[1])
    endtime   = int(sys.argv[2])

def main():
    usage()
    thread_num = 10
    queue = Queue.Queue()
    start = time.time()
    threads = []
    for types in MRule_Type_List:
            queue.put(types)
    for i in range(int(thread_num)):
        t = MyThread(queue)
        t.setDaemon(True)
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

    for line in OTHER_List:
        Pyes(line)
    print "is spend seconds {0}".format(time.time() - start)

def main2():
    usage()
    start = time.time()
    for types in MRule_Type_List:
        Pyes(types)    
    print "is spend seconds {0}".format(time.time() - start)


if __name__ == '__main__':
    main()


