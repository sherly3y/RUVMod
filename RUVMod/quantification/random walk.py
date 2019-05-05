#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from operator import itemgetter
import networkx as nx

def PageRank(graph, current_node='129972', damping_factor=0.85,\
        max_iterations=25, min_delta=0.0001):
    nodes = graph.nodes()
    graph_size = len(nodes)
    if graph_size == 0:
        return {}
    '''if the random walk start from one node,set the rank as 1.0,while others 0'''
    pagerank = dict.fromkeys(nodes, 0)     #给每个节点赋予初始的PR值
    pagerank[current_node] = 1.0
    Svalue = {}
    min_value = (1.0-damping_factor) / graph_size
    itertimes = 0
    for i in range(max_iterations):
        diff = 0         
        for node in nodes:
            rank = min_value
            for referring_page in list(graph.neighbors(node)):    #遍历与node相邻的结点
                rank += damping_factor * pagerank[referring_page] * \
                         getRankTo(flag, graph, node, referring_page, Svalue)   #计算该node的rank
            diff += abs(pagerank[node] - rank)
            pagerank[node] = rank
        '''重启动概率'''
        pagerank[current_node] += 1*(1-damping_factor)
        itertimes = i
        '''stop if PageRank has converged'''
        if diff < min_delta:
            break
    print '\niterition time:'+ str(itertimes)
    return sorted(pagerank.iteritems(), key=itemgetter(1), reverse=True)

def getRankTo(gra, from_node, to_node, S):
    if  S.has_key(from_node+':'+to_node):
        return S[from_node+':'+to_node]
    total_wt = 0.0
    for tmp_node in list(gra.neighbors(from_node)):
        total_wt = total_wt + gra.get_edge_data(from_node, tmp_node)['weight']
    if total_wt!=0:   
        S[from_node+':'+to_node] = gra.get_edge_data(from_node, to_node)['weight']/total_wt
    else:
        S[from_node+':'+to_node]=0
    return  S[from_node+':'+to_node]
