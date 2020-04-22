import os
import json
import pandas as pd
import numpy as np
import time
import sys

def filter(filename):
	input_file = open(filename, "r")
	num_lines = sum(1 for line in input_file)
	numberoflines = 0
	if(filename == "callblocker_new_trial.txt"):
		output_file = open("callblocker_only_method_calls.txt", "w")
	else:
		output_file = open("only_method_calls.txt", "w")
		# output_file = open("roughrough_only_method_calls.txt", "w")
	output_file.truncate()
	cnt = 0

	# For part of the file
	with open(filename) as file:
		lines = [line.strip() for line in file]
	
	
	# if(filename == "roughrough_new_trial.txt"):
	if(filename == "callblocker_new_trial.txt"):
	# if(filename == "r4.txt"):
		numberoflines = len(lines)
	else:
		numberoflines = 10000
	for i in range(0, numberoflines):
		count = 0
		for k in lines[i]:
		    if(k.isspace()):
		        count = count + 1
		if(count > 4):
			s = 0
			tempLine = ""
			remainingArg = lines[i].split(" ")
			for k in range(0, 3):
				tempLine = tempLine + remainingArg[k] + " "
			ttemp = ""
			for k in range(3, len(remainingArg) - 1):
				ttemp = ttemp + remainingArg[k]
			ttemp.replace(" ", "")
			tempLine = tempLine + ttemp + " " + remainingArg[-1]
			lines[i] = tempLine
		output_file.write(lines[i] + "\n")
		# if(i < len(lines) - 1):
		# 	output_file.write(lines[i]+"\n")
		# else:
		# 	output_file.write(lines[i])
		cnt = cnt + 1

# # Past remove non start that takes O(n^2)
# def remove_non_start_past():
# 	start = time.time()
# 	df = pd.read_csv("only_method_calls.txt", delimiter = " ", header = None, names = ['Call', 'IO', 'ThreadID', 'Method'])
# 	alone = []
# 	for j in range(0, len(df)):
# 	    flag = 0
# 	    if(df['Call'][j] == 'Method' and df['IO'][j] == "<"):
# 	        for i in range(0, j):
# 	            if(df['Call'][i] == 'Method' and df['ThreadID'][j] == df['ThreadID'][i] and df['Method'][j] == df['Method'][i] and df['IO'][i] == ">"):
# 	                flag = 1
# 	                break
# 	        if(flag == 0):
# 	            alone.append(j)
# 	print("Alone")
# 	print(alone)
# 	print(len(alone))
# 	df = df.drop(alone)
# 	np.savetxt('hello.txt', df.values, fmt='%s', delimiter=" ")

#test.txt USE THIS TO SHOW ALL CASES SUCCESSFUL
#only_method_calls.txt
# was initially hello.txt
# def parse():
# 	file = open("hello.txt", "r")
# 	data = []
# 	linenum = 1
# 	print("parse")
# 	for lines in file:
# 		# print(lines)
# 		mydict = {}
# 		s = ""
# 		line = lines[:-1]
# 		spacesplit = line.split(' ')
# 		mydict["Line_no"] = linenum
# 		mydict["Type"] = spacesplit[0]

# 		if(spacesplit[0] == 'BBEntry'):
# 			mydict["Thread_ID"] = spacesplit[1]
# 			mydict["BB_ID"] = spacesplit[2]
# 			mydict["Method"] = None
# 			mydict["Args"] = None
# 			mydict["Direction"] = None

# 		elif(spacesplit[0] == 'Method' or spacesplit[0] == 'API'):
# 			mydict["Thread_ID"] = spacesplit[2]
# 			mydict["BB_ID"] = spacesplit[4]
# 			mydict["Direction"] = spacesplit[1]
# 			methodparsed = spacesplit[3].split('(')
# 			mydict["Method"] = methodparsed[0]
# 			args = methodparsed[1][:-1]
# 			if(args == ""):
# 				mydict["Args"] = None
# 			else:
# 				mydict["Args"] = args
# 			# getting each argument
# 			# print(mydict["Args"][0])
# 		else:
# 			continue;

# 		linenum = linenum + 1
# 		print(linenum)
# 		data.append(mydict)
# 		if(lines == "API > 1 android.app.Activity.registerReceiver(com.androidrocker.callblocker.MainActivity@75235272<activity=true>,com.androidrocker.callblocker.f@254168966,android.content.IntentFilter@164517713) 1090038"):
# 			print(data)
# 			sys.exit(0)
# 	print("done parse")
# 	return data

def parse():
	file = open("hello1.txt", "r")
	data = []
	linenum = 1
	for lines in file:
		mydict = {}
		s = ""
		line = lines[:-1]
		if(line == ""):
			continue
		spacesplit = line.split(' ')
		mydict["Line_no"] = linenum
		mydict["Type"] = spacesplit[0]
		mydict["Thread_ID"] = spacesplit[2]
		mydict["BB_ID"] = spacesplit[4]
		mydict["Direction"] = spacesplit[1]
		methodparsed = spacesplit[3].split('(')
		mydict["Method"] = methodparsed[0]
		args = methodparsed[1][:-1]
		if(args == ""):
			mydict["Args"] = None
		else:
			mydict["Args"] = args

		linenum = linenum + 1
		data.append(mydict)
	return data

def getTheAPIOut(data):
	finalData = []
	i = 0
	l = 1
	finalData.append(data[i])
	while(l < len(data)):
		if(data[i]["Type"] == 'API' and data[l]["Type"] != 'API' and data[i]['Direction'] == '>'):
			finalData = finalData[:-1]
			i = i + 2
			l = i + 1
			break
		else:
			finalData.append(data[l])
			i = i + 1
			l = l + 1
	return finalData