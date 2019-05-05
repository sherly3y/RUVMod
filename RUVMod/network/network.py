#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import networkx as nx 
import csv

class BaseDigraphByNode():
    def __init__(self):
        self.mDigraph=nx.DiGraph()

     
    def getDigraph(self):          
        with open('train.csv','rb') as csvfile: 
            reader = csv.reader(csvfile)     
            for row in reader:
                author_list=row[1].split(',')
                for i in range(0,len(author_list)):
                    author_a=author_list[i]
                    for j in range(i+1,len(author_list)):
                        author_c=author_list[j]
                        w=0
                        if (author_a,author_c) in self.mDigraph.edges():
                            w+=1
                        else:
                            w=1
                        self.mDigraph.add_edge(author_a,author_c,weight=w)


        print "add node finished! and node count:" + str(len(self.mDigraph.nodes()))
        print "add edge finished! and edge count:" + str(len(self.mDigraph.edges()))
        return self.mDigraph
if __name__ == '__main__':
    mDigraph=BaseDigraphByNode()
    gra=mDigraph.getDigraph()
