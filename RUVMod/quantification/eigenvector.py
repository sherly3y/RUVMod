#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from network import BaseDigraphByNode
import networkx as nx 
import csv
mdigraph=BaseDigraphByNode()
gra=mdigraph.getDigraph()
try:
	eigenvector_dic=nx.eigenvector_centrality_numpy(gra)
except:
	raise  nx.NetworkXError
csv_row=[]
for key in eigenvector_dic.keys():
    cs=[]
    cs.append(key)
    cs.append(eigenvector_dic[key])
    csv_row.append(cs)
with open("eigenvector.csv","wb") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(csv_row) 
