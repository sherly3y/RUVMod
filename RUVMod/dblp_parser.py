#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import xml.sax
import re
import mysql_util
from mysql_util import mysqlutil
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8') 

#paper_tags = ('article','inproceedings','proceedings','book', 'incollection','phdthesis','mastersthesis','www')
paper_tags = ('inproceedings','') 
sub_tags = ('crossref','booktitle')

class MovieHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.id = 1
        self.kv = {}
        self.reset()
        self.util = mysqlutil()
        self.params = []
        self.batch_len = 10
        
    def reset(self):
        self.curtag = None
        self.pid = None
        self.ptag = None
        self.title = None
        self.author = None
        self.subtext = None
        self.year = None
        self.url = None
        self.kv = {}

    #元素开始事件处理(主要识别author,year,title等标签)
    def startElement(self, tag, attributes):
        if tag is not None and len(tag.strip()) > 0:
            self.curtag = tag
            if tag in paper_tags:
                self.reset()
                self.pid = self.id
                self.kv['ptag'] = str(tag)
                self.kv['id'] = self.id
                self.id += 1

    # 元素结束事件处理（重置变量值）
    def endElement(self, tag):
        if tag == 'title':
            self.kv['title'] = str(self.title)
        elif tag == 'author':
            self.author = re.sub(' ','_', str(self.author))
            if self.kv.has_key('author') == False:
                self.kv['author'] = []
                self.kv['author'].append(str(self.author))
            else:
                self.kv['author'].append(str(self.author))

        elif tag in sub_tags:
            self.kv['sub_detail'] = str(self.subtext)

        elif tag == 'url':
            self.kv['url'] = str(self.url)

        elif tag == 'year':
            self.kv['year'] = str(self.year)

        elif tag in paper_tags:
            tid = int(self.kv['id']) if self.kv.has_key('id') else 0
            ptag = self.kv['ptag'] if self.kv.has_key('ptag') else 'NULL'
            
            try:
                title = self.kv['title'] if self.kv.has_key('title') else 'NULL'
            except Exception, e:
                print e
                title = ''
            author = self.kv['author'] if self.kv.has_key('author') else 'NULL'
            author = ','.join(author) if author is not None else 'NULL'
            sub_detail = self.kv['sub_detail'] if self.kv.has_key('sub_detail') else 'NULL'
            year = self.kv['year'] if self.kv.has_key('year') else 0
            url = self.kv['url'] if self.kv.has_key('url') else 'NULL'
           
            param = (author,year,title,url)
            self.params.append(param)
            
            if len(self.params) % self.batch_len == 0:
                sql = "insert into `paper_conf`(author, year,title,url，sub_detail) values(%s,%s,%s,%s,%s)"
                self.util.execute_sql_params(sql, self.params)
                self.params = []

    # 内容事件处理（读取标签内容，得到title,author列表等）
    def characters(self, content):
        if self.curtag == "title":
            self.title = content.strip()
        elif self.curtag == "author":
            self.author = content.strip()
        elif self.curtag in sub_tags:
            self.subtext = content.strip()
        elif self.curtag == "year":
            self.year = content.strip()
        elif self.curtag == "url":
            self.url = content.strip()


if __name__ == "__main__":
   
    filename = 'dblp.xml'
    if len(sys.argv) == 2:
        filename = sys.argv[1]

    if os.path.exists(filename) == False:
        print '[%s] not exists!' % filename
        exit(1)

    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = MovieHandler()
    parser.setContentHandler( Handler )

    parser.parse(filename)
    print 'Parser Complete!'
