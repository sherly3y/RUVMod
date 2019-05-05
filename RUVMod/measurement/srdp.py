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

def unexpectedness(targetNode,coauthor):
	with open('PM_all.csv','rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			if targetNode==row[0] and coauthor==row[1]:
				return False
	return True

def useful(targetNode,coauthor):#13-17 5years  times>=3
	times=0
	with open('valid.csv','rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			coauthors=row[1]
			coauthors=coauthors.split(",")
			if (targetNode in coauthors) and (coauthor in coauthors):
				times+=1
	if times>=3:
		return True
	return False

def serendipity():
	intersection=0
	unexpected=0.0
	usefuln=0.0
	srdp=uxp=use=0.0
	with open('SOM/serendipitous cluster.csv','rb') as csvfile:  
		reader = csv.reader(csvfile)
		for row in reader:
			targetNode=row[0]
			coauthor=row[1]
			if (unexpectedness(targetNode,coauthor)==True):
				unexpected+=1
			if (useful(targetNode,coauthor)==True):
				usefuln+=1
			if (unexpectedness(targetNode,coauthor)==True) and (useful(targetNode,coauthor)==True):
				intersection+=1
	srdp=intersection/96139  #96139为新奇合作者簇中的合作者数量
	uxp=unexpected/96139
	use=usefuln/96139
	print uxp,use,srdp    

if __name__ == '__main__':
	serendipity()


