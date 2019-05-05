#!/usr/bin/env python
#coding=utf-8

from __future__ import division
import csv

def getPM():  
	fina=[]
	#select author,avg(r),avg(u) from data group by author
	with open('Data.csv','rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			author=row[0]
			coauthor=row[1]
			r=float(row[2])
			u=float(row[3])
			with open('avgru.csv','rb') as csvfile:
				reader=csv.reader(csvfile)
				for row in reader:
					if author==row[0]:
						if (r>float(row[1])) and (u<float(row[2])):
							temp=[]
							temp.append(author)
							temp.append(coauthor)
							fina.append(temp)
						break
	with open("PM_all.csv","ab+") as csvfile:
		writer = csv.writer(csvfile)
		writer.writerows(fina)

def serendipity():
	intersection=0
	unexpected=0.0
	usefuln=0.0
	srdp=uxp=use=0.0
	dic1={}
	dic2={}
	with open('PM_all.csv','rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			key=row[0]+':'+row[1]
			if not dic1.has_key(key):
				dic1[key]=0
	with open('valid.csv','rb') as csvfile:  #测试集中的合作次数
		reader = csv.reader(csvfile)
		for row in reader:
			coauthors=row[1].split("*")
			for i in range(0,len(coauthors)):
				for j in range(i+1,len(coauthors)):
					key1=coauthors[i]+':'+coauthors[j]
					key2=coauthors[j]+':'+coauthors[i]
					if not dic2.has_key(key1) and not dic2.has_key(key2):
						dic2[key1]=1
						dic2[key2]=1
					else:
						dic2[key1]+=1
						dic2[key2]+=1
	with open('SOM/serendipitous cluster.csv','rb') as csvfile: 
		reader = csv.reader(csvfile)
		for row in reader:
			targetNode=row[0]
			coauthor=row[1]
			key=targetNode+':'+coauthor
			if (not dic1.has_key(key)):
				unexpected+=1
			if (dic2.has_key(key)):
				if (dic2[key]>=3):
					usefuln+=1
			if dic2.has_key(key):
				if (not dic1.has_key(key)) and (dic2[key]>=3):
					intersection+=1
	srdp=intersection/96139  #96139为新奇合作者簇中的合作者数量
	uxp=unexpected/96139
	use=usefuln/96139
	print uxp,use,srdp    


if __name__ == '__main__':	
	serendipity()


