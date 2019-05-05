#!/usr/bin/env python
#coding=utf-8

import math
import numpy as plt
import matplotlib.pyplot as plt1
from matplotlib import cm
import scipy.io as sio  
import csv
from mpl_toolkits.mplot3d import Axes3D

#初始化输入层与竞争层神经元的连接权值矩阵
def initCompetition(n , m , d):
    #随机产生0-1之间的数作为权值
    array = plt.random.random(size=n * m *d)
    com_weight = array.reshape(n,m,d)
    return com_weight

#计算向量的二范数
def cal2NF(X):
    res = 0
    for x in X:
        res += x*x
    return res ** 0.5

#对数据集进行归一化处理
def normalize(dataSet):
    old_dataSet = plt.copy(dataSet)
    for data in dataSet:
        two_NF = cal2NF(data)
        for i in range(len(data)):
            data[i] = data[i] / two_NF
    return dataSet , old_dataSet

#对权值矩阵进行归一化处理
def normalize_weight(com_weight):
    for x in com_weight:
        for data in x:
            two_NF = cal2NF(data)
            for i in range(len(data)):
                data[i] = data[i] / two_NF
    return com_weight

#得到获胜神经元的索引值
def getWinner(data , com_weight):
    max_sim = 0
    n,m,d = plt.shape(com_weight)
    mark_n = 0
    mark_m = 0
    for i in range(n):
        for j in range(m):
            if sum(data * com_weight[i,j]) > max_sim:
                max_sim = sum(data * com_weight[i,j])
                mark_n = i
                mark_m = j
    return mark_n , mark_m

#得到神经元的N邻域
def getNeibor(n , m , N_neibor , com_weight):
    res = []
    nn,mm , _ = plt.shape(com_weight)
    for i in range(nn):
        for j in range(mm):
            N = int(((i-n)**2+(j-m)**2)**0.5)
            if N<=N_neibor:
                res.append((i,j,N))
    return res

#学习率函数
def eta(t,N):
    return (0.3/(t+1))* (math.e ** -N) #初始学习率0.3

#SOM算法的实现
def do_som(dataSet , com_weight, T , N_neibor):
    '''
    T:最大迭代次数
    N_neibor:初始近邻数
    '''

    for t in range(T-1):
        com_weight = normalize_weight(com_weight)
        for data in dataSet:
            n , m = getWinner(data , com_weight)
            neibor = getNeibor(n , m , N_neibor , com_weight)
            for x in neibor:
                j_n=x[0];j_m=x[1];N=x[2]
                #权值调整
                com_weight[j_n][j_m] = com_weight[j_n][j_m] + eta(t,N)*(data - com_weight[j_n][j_m])
            N_neibor = N_neibor+1-(t+1)/200
    res = {}
    N , M , _ =plt.shape(com_weight)
    for i in range(len(dataSet)):
        n, m = getWinner(dataSet[i], com_weight)
        key = n*M + m  #第几类
        if res.has_key(key):
            res[key].append(i)
        else:
            res[key] = []
            res[key].append(i)
    return res
    
def writeto(dataSet,res):
    i=0   
    for key in res.keys():
        li=res[key]
        fina=[]
        for item in li:
            temp=[]
            temp.append(dataSet[item][0])
            temp.append(dataSet[item][1])
            temp.append(dataSet[item][2])
            temp.append(item)
            fina.append(temp)  
        with open("SOM//"+str(i)+".csv","wb") as csvfile:  #写入第i个簇
            writer=csv.writer(csvfile)
            writer.writerows(fina)
        i+=1    



#SOM算法主方法
def SOM(dataSet,com_n,com_m,T,N_neibor):
    dataSet,old_dataSet = normalize(dataSet)
    com_weight = initCompetition(com_n,com_m,plt.shape(dataSet)[1])
    C_res = do_som(dataSet, com_weight, T, N_neibor)
    print len(C_res)
    draw(C_res, dataSet)  #按照归一化的数据绘制的聚类结果
    draw(C_res, old_dataSet)   #按照原数据绘制的聚类结果
    writeto(old_dataSet,C_res)

       
def draw(C , dataSet):
    color = ['r', 'y', 'g', 'b', 'm', 'k', 'c' , '#00ff00']
    ty = ['o', 'v', 's', '*', '+', '<', '>' , '^']
    count = 0
    label=0
    j1=0
    flagset=['01','02','03','04','05','06','07','08']
    ax=plt1.subplot(111,projection='3d') #创建一个三维的绘图工程
    for i in C.keys(): 
        X = []
        Y = []
        Z = []
        datas = C[i]
        for j in range(len(datas)):
            X.append(dataSet[datas[j]][0])
            Y.append(dataSet[datas[j]][1])
            Z.append(dataSet[datas[j]][2])
        ax.scatter(X, Y, Z,marker=ty[count % len(ty)], color=color[count % len(color)], label=flagset[count % len(flagset)])
        count += 1
        j1+=1
    plt1.legend(loc='upper center', bbox_to_anchor=(0.52,1.1),ncol=3,fontsize=11,fancybox=True)
    ax.set_zlabel('V',fontsize=11,labelpad = 9.5) #坐标轴
    ax.set_ylabel('U',fontsize=11,labelpad = 9.5)
    ax.set_xlabel('R',fontsize=11,labelpad = 9.5)
    plt1.show()

    
def readData(path):
    data = []
    with open(path,'rb') as csvfile:
        reader = csv.reader(csvfile)        
        for row in reader:
            temp=[]
            temp.append(float(row[2]))
            temp.append(float(row[3]))
            temp.append(float(row[4]))
            data.append(temp)       
    return data
    
if __name__ == '__main__':
    data = readData('Data.csv')
    data = plt.array(data)
    datatest=plt.array(data)
    SOM(datatest,3,9,15,6)  #(datatest,com_n,com_m ,T总迭代次数,N_neibor)