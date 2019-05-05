#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from network import BaseDigraphByNode
import networkx as nx 
import csv
mdigraph=BaseDigraphByNode()
gra=mdigraph.getDigraph()
betweeness_dic=nx.betweenness_centrality(gra)
csv_row=[]
for key in betweeness_dic.keys():
    cs=[]
    cs.append(key)
    cs.append(betweeness_dic[key])
    csv_row.append(cs)
with open("betweeness.csv","wb") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(csv_row) 