import os	
import json
import pandas as pd
import numpy as np

# I was previously using this --> called rewritten-source_previousCopy in the folder
# filename = "/Users/snehagathani/Desktop/Sem 2/IR/projectcopy2/rewritten-source"

# Currently I am using this
# filename = "/Users/snehagathani/Desktop/Sem 2/IR/projectcopy2/sourceCode"
method = "android.content.UriMatcher.addURI(android.content.UriMatcher@72819199,"","",124415509&java.lang.Integer@124415509)"

def find_file(method, nameApp):
	# if(nameApp == "Test"):
	# 	filename = "/Users/snehagathani/Desktop/Sem 2/IR/projectcopy2/CallBlockerSourceCode"
	# else:
	# 	filename = "/Users/snehagathani/Desktop/Sem 2/IR/projectcopy2/sourceCode"
	filename = "/Users/snehagathani/Desktop/Sem 2/IR/projectcopy2/CallBlockerSourceCode"
	path_array1 = method.split("(")
	path_array = path_array1[0].split(".")
	path = ""
	for i in range(0, len(path_array) - 1):
		path = path + "/" + path_array[i]
	filename_path = filename + path + ".java"
	if(not os.path.isfile(filename_path)):
		filename = "/Users/snehagathani/Desktop/Sem 2/IR/projectcopy2/sourceCode"
		filename_path = filename + path + ".java"
	return filename_path, path_array[len(path_array) - 1], path_array1[1:]

def find_line_no(filename_path, method, args, method_found, log_bbid):
	print("Inside find_line_no")
	def locations_of_substring(string, substring):
		print(string)
		print(substring)
		substring_length = len(substring)
		def recurse(locations_found, start):
			location = string.find(substring, start)
			if location != -1:
				return recurse(locations_found + [location], location+substring_length)
			else:
				return locations_found
		return recurse([], 0)

	valid_args=[]
	for i in range(0, len(args)):
		if(args[i].find("\"\"")==(-1) and args[i].find("null")==(-1)):
			valid_args.append(args[i])

	method = method_found + "("
	exist = os.path.isfile(filename_path)
	if not exist:
		return "Out of scope! :("
	data = open(filename_path, "r")

	# Finding which line is the BBID
	temp = []
	line_no_complete_line = []
	all_lines_line_no = []
	bbid_line_number = 0

	line_no = 0
	for line in data:
		line_no += 1
		dic = {}
		dic["line_no"] = line_no
		dic["line"] = line.lstrip()
		all_lines_line_no.append(dic)
		if method in line:
			comp = {}
			comp["line_no"] = line_no
			comp["line"] = line.lstrip()
			line_no_complete_line.append(comp)

		if log_bbid in line:
			bbid_line_number = line_no
			break

	if(len(line_no_complete_line) == 0):
		exact_line_no = 0
		
		for i in range(len(all_lines_line_no)-1, -1, -1):
			temp = all_lines_line_no[i]["line"].replace("\n","")
			if(temp != '{'):
				exact_line_no = i - 1
				break

		actual_line = all_lines_line_no[exact_line_no - 1]
		all_characters_and_line_numbers = 0
		return actual_line["line_no"], all_characters_and_line_numbers
	else:
		actual_line = line_no_complete_line[-1:][0]

		all_characters_and_line_numbers = locations_of_substring(actual_line["line"], method)
		return actual_line["line_no"], all_characters_and_line_numbers

def source_code(filename_path):
	data = []
	with open (filename_path, "r") as myfile:
		for line in myfile:
			data.append(line)
	return data

def findbbblock(filename_path, line_no):
	hexcode_lines = []
	hexcode = []
	lineList = list()
	with open(filename_path) as f:
		for line in f:
			lineList.append(line)

	for i in range(0, len(line_no)):
		hexcode_lines.append(lineList[line_no[i]])

	# print(hexcode_lines[0])
	for i in range(0, len(hexcode_lines)):
		print("1")
		if(hexcode_lines[i].find('(') is not -1):
			temp = hexcode_lines[i].split('(')[1]
			print(temp)
			print("2")
			temp = temp.split(')')[0]
			print(temp)
			if(temp.find("x") is -1):
				hexcode.append(temp)
			else:
				hexcode.append(temp.split('x')[1])
	return hexcode
