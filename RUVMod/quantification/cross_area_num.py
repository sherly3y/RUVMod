#!/usr/bin/env python
#coding=utf-8
import csv

	
def getbridgenum(target,targetNode,venue):
	bridge=0
	with open('Artificial Intelligence/AI.csv','rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			author=row[1].split(',')
			if targetNode in author and 'AI' not in venue:
				bridge+=1
				break
	csvfile.close()
	with open('computer graphics and media/computer graphics and multimedia.csv','rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			author=row[1].split(',')
			if targetNode in author and 'CG' not in venue:
				bridge+=1
    			break
	csvfile.close()
	with open('computer network/computer networks.csv','rb') as csvfile:
		for row in csv.reader(csvfile):
			author=row[1].split(',')
			if targetNode in author and 'CN' not in venue:
				bridge+=1
				break
	csvfile.close()    			
	with open('Data mining/datamining.csv','rb') as csvfile:
		for row in csv.reader(csvfile):
			author=row[1].split(',')
			if targetNode in author and 'DM' not in venue:
				bridge+=1
				break  			  
	csvfile.close()
	with open('software engineering/software engineering.csv','rb') as csvfile:
		for row in csv.reader(csvfile):
			author=row[1].split(',')
			if targetNode in author and 'SE' not in venue:
				bridge+=1
				break
	csvfile.close()
	with open('computer architecture/CA.csv','rb') as csvfile:
		for row in csv.reader(csvfile):
			author=row[1].split(',')
			if targetNode in author and 'CA' not in venue:
				bridge+=1
				break
	csvfile.close()
	with open('computer science theory/CST.csv','rb') as csvfile:
		for row in csv.reader(csvfile):
			author=row[1].split(',')
			if targetNode in author and 'CST' not in venue:
				bridge+=1
				break
	csvfile.close()
	with open('human-machine interaction/HMI.csv','rb') as csvfile:
		for row in csv.reader(csvfile):
			author=row[1].split(',')
			if targetNode in author and 'HMI' not in venue:
				bridge+=1
				break
	csvfile.close()
	with open('information security/IS.csv','rb') as csvfile:
		for row in csv.reader(csvfile):
			author=row[1].split(',')
			if targetNode in author and 'IS' not in venue:
				bridge+=1
				break
	csvfile.close()
	with open('interdispline/INT.csv','rb') as csvfile:
		for row in csv.reader(csvfile):
			author=row[1].split(',')
			if targetNode in author and 'INT' not in venue:
				bridge+=1
				break
	csvfile.close()    				
	fina=[]
	temp=[]
	temp.append(target)
	temp.append(targetNode)
	temp.append(bridge) 
	fina.append(temp) 
	with open("cross_area_num.csv","ab") as csvfile:
		csv.writer(csvfile).writerows(fina)

if __name__ == '__main__':
	with open('author_pair.csv','rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			author=row[0]
			coauthor=row[1]
			venue=row[2].split(',')
			getbridgenum(author,coauthor,venue)

