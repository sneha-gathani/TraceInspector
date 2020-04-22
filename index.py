from flask import Flask, Response
from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify
import os
import time
import json
import psycopg2
from os.path import exists
from os import makedirs
import json, os, signal
import sys

import database
import filter_method_calls
import file_path
import precalc
import sorting
import security_calls
import run_remove_non_start
import input_json
import get_the_graph
import calcColPos_py
import getTheGraph
import letstryworking

app = Flask(__name__)
app.debug = True
precomputed_pos = []
rect_data = []
miny = 0
maxy = 0

@app.route("/interactions" , methods=['GET', 'POST'])
def interactions():
	# Selects the dataset you want to seee
	dataset = request.form.get('dataset')
	dataset = "Test"
	if(dataset == "Actual"):
		filter_method_calls.filter("new_trial.txt")
	else:
		filter_method_calls.filter("callblocker_new_trial.txt")
		# filter_method_calls.filter("roughrough_new_trial.txt")
		# filter_method_calls.filter("r4.txt")
	
	# file_name = "roughrough_only_method_calls.txt"
	if(dataset == "Actual"):
		file_name = 'only_method_calls.txt'
	else:
		file_name = 'callblocker_only_method_calls.txt'
		# file_name = "roughrough_only_method_calls.txt"
	thread_id = []

	if(len(file_name) > 0):
		if(dataset == "Actual"):
			run_remove_non_start.remove_non_start('only_method_calls.txt')
		else:
			run_remove_non_start.remove_non_start('callblocker_only_method_calls.txt')
			# run_remove_non_start.remove_non_start('roughrough_only_method_calls.txt')
		run_remove_non_start.removeAPI('hello.txt')
		data = filter_method_calls.parse()
		database.create_database()
		database.insert_rows(data)
		after_insertion_data = database.select_all()

	# Get all the methods in the log without init
	all_methods = database.get_all_methods()

	#Get the security calls in the log
	full_lines, only_methods, counts_interesting_methods = security_calls.get_all_common_security_methods()
	counts = []

	a = zip(counts_interesting_methods, only_methods)
	a = sorted(a, key = lambda x: x[0]) 	
	a.reverse()
	b = list(zip(*a))

	interesting_security_methods = []
	for i in range(0, len(only_methods)):
		temp = b[1][i] + ' (' + str(b[0][i][0][0]) + ')'
		interesting_security_methods.append(temp)

	thread = database.get_distinct_thread()

	for i in range(0, len(thread)):
		thread_id.append(thread[i])

	thread_id.reverse()
	thread_id.append("All")

	starting, ending, timeline_data = database.get_thread_line_nos(thread_id)

	startEnds = []
	for i in range(0, len(starting)):
		temp = []
		temp.append(starting[i])
		temp.append(ending[i])
		startEnds.append(temp)

	threadIDForThreadView = thread_id[:-1]
	threadIDForThreadView.insert(0, 'All')

	timeline_data = calcColPos_py.computeColumnPositions(startEnds, threadIDForThreadView)

	# Selects the thread you want to view
	select = request.form.get('comp_select')
	# Selects which function to view
	function = request.form.get('functionarea')

	data = database.get_interactions(select, function, thread_id)

	precomputed_pos, rect_data, maximum_height, maximum_width = letstryworking.precalc(after_insertion_data)

	maximum_width = maximum_width + 15
	maximum_height = maximum_height + 15

	# maximum_height = 700
	# maximum_width = 700
	
	first_selected = next((sub for sub in rect_data if sub['Function'] == '1'), None) 
	autoscroll_position_index = -1
	if(first_selected!=None):
		temp = first_selected['Line_no']
		i = 0
		for p in range(0, len(precomputed_pos)):
			if(precomputed_pos[p][0] == temp):
				i = p
				break
		autoscroll_position_index = i

	for i in range(0, len(precomputed_pos)):
		precomputed_pos[i].pop(0)
	
	# Flowchart without click
	elem = []
	theThread = "-1"
	nameApp = 0
	if(dataset == "Actual"):
		nameApp = 1
	return render_template('trial.html', thread = thread_id, precomputed_pos = precomputed_pos, rectangle_data = rect_data, maximum_height = maximum_height, maximum_width = maximum_width, top_5 = interesting_security_methods, elem = elem, timeline_data = timeline_data, autoscroll_position_index = autoscroll_position_index, all_methods = all_methods, theThread = theThread, dataset = nameApp)


# Only the stacked_diagram
@app.route("/stacked_diagram", methods = ['GET', 'POST'])
def stacked_diagram():

	thread = database.get_distinct_thread()
	thread_id = []
	for i in range(0, len(thread)):
		thread_id.append(thread[i])

	thread_id.reverse()
	thread_id.append("All")

	# Gets the selected thread
	if(request.method == 'POST'):
		gotdata = json.loads(request.data)

	if(type(gotdata) == int):
		t = []
		t.append(gotdata)
		t.append(None)
		gotdata = t

	# Selects which thread to view
	if(gotdata[0] == None):
		select = None
	else:
		if(gotdata == "All"):
			select = "All"
			function = None
		else:
			select = gotdata[0]

	# Selects which function to view
	if(gotdata != "All"):
		if(gotdata[1] == None):
			function = None
		else:
			function = gotdata[1]

	data = database.get_interactions(select, function, thread_id)

	precomputed_pos, rect_data, maximum_height, maximum_width = precalc.precalc(data)
	first_selected = next((sub for sub in rect_data if sub['Function'] == '1'), None) 
	autoscroll_position_index = -1
	if(first_selected!=None):
		temp = first_selected['Line_no']
		i = 0
		for p in range(0, len(precomputed_pos)):
			if(precomputed_pos[p][0] == temp):
				i = p
				break
		autoscroll_position_index = i

	for i in range(0, len(precomputed_pos)):
		precomputed_pos[i].pop(0)
	
	# Flowchart without click
	elem = []
	if(select == None):
		theThread = "1"
	else:
		theThread = select
	return jsonify(precomputed_pos, rect_data, maximum_height, maximum_width, autoscroll_position_index, theThread)


# Only source code
@app.route("/source_code" , methods=['GET', 'POST'])
def source_code():
	if(request.method == 'POST'):
		content1 = json.loads(request.data)
		print("Source code")
		content = content1.split('!')[0]
		nameApp = content1.split('!')[1]
	
		print("nameApp: ", nameApp)
		if(content == ""):
			method = "com.helpshift.util.HelpshiftContext.b()"
		method_name = content

		method_name = content.split(',')[0]
		# The BBID in the log
		d = database.getline(method_name.split('(')[0])
		log_bbid = d[0]['BB_ID']

		data_structure = []
		# filename = "/Users/snehagathani/Desktop/Sem 2/IR/projectcopy2/sourceCode"
		filename_path, method_found, args = file_path.find_file(method_name, nameApp)

		l, c = file_path.find_line_no(filename_path, method_name, args, method_found, log_bbid)
		# bbblock_line_no = file_path.findbbblock(filename_path, line_no)

		line_no = []
		character = []
		line_no.append(l)
		character.append(c)

		# Figure out the relation between BB_ID and hexcode and then send only that line number underneath so that only that gets highlighted
		code = file_path.source_code(filename_path)
		
		clean_code = []
		for i in range(0, len(code)):
			temp = code[i].split("\n")
			clean_code.append(temp[0])

		clean_code.append("Line_nos")
		to_send = clean_code + line_no

		character.insert(0, "Character_nos")
		to_send = to_send + character

		to_send.append(method_found)
		return jsonify(to_send)

# Selects both in stack and gets the source code
@app.route("/select_in_stack" , methods=['GET', 'POST'])
def select_in_stack():
	if(request.method == 'POST'):
		content1 = json.loads(request.data)
		content = content1.split('!')[0]
		nameApp = content1.split('!')[1]
		print("SelectInStackNameApp: ", nameApp)
		nodes, edges = input_json.getvalues('raw_data.json')

		# Get the thread of the method
		thread = database.get_thread(content)

		# Get all the data of this thread with 'Function: 1' for method_selected
		data = database.get_particular_selected(content, thread)

		print(data)

		# data = database.get_particular_selected(content)

		d = database.getline(content)

		precomputed_pos, rect_data, maximum_height, maximum_width = precalc.precalc(data)

		# line_it = None
		# for j in range(0, len(d)):
		# 	for i in range(0, len(rect_data)):
		# 		if(rect_data[i]['Method'].split('(')[0] == content):
		# 			line_it = i
		# 			break

		line_it = None
		for j in range(0, len(rect_data)):
			if(rect_data[j]['Method'].split('(')[0] == content):
				line_it = j
				break

		
		autoscroll_position_index = -1

		if(line_it != None):
			autoscroll_position_index = line_it

		for i in range(0, len(precomputed_pos)):
			precomputed_pos[i].pop(0)

		to_send1 = []
		to_send1.append(precomputed_pos)
		to_send1.append(rect_data)
		to_send1.append(maximum_height)
		to_send1.append(maximum_width)
		to_send1.append(autoscroll_position_index)

		if(content == ""):
			method = "com.helpshift.util.HelpshiftContext.b()"
		method_name = content

		method_name = content.split(',')[0]
		
		log_bbid = d[0]['BB_ID']

		filename_path, method_found, args = file_path.find_file(method_name, nameApp)
		
		l, c = file_path.find_line_no(filename_path, method_name, args, method_found, log_bbid)
		# bbblock_line_no = file_path.findbbblock(filename_path, line_no)

		line_no = []
		character = []
		line_no.append(l)
		character.append(c)

		# Figure out the relation between BB_ID and hexcode and then send only that line number underneath so that only that gets highlighted
		code = file_path.source_code(filename_path)

		clean_code = []
		for i in range(0, len(code)):
			temp = code[i].split("\n")
			clean_code.append(temp[0])

		clean_code.append("Line_nos")
		to_send2 = clean_code + line_no

		character.insert(0, "Character_nos")
		to_send2 = to_send2 + character

		to_send2.append(method_found)

		to_send = []
		to_send.append(to_send1)
		to_send.append(to_send2)
		
		return jsonify(to_send)

@app.route("/flowchart", methods=['GET','POST'])
def flowchart():
	elem = []
	if(request.method == 'POST'):
		if os.path.exists("raw_data.json"):
			os.remove("raw_data.json")
		# The name of the request method should go in as an arg here
		# get_the_graph.forming('android.app.Application.onCreate')
		content1 = request.get_json()
		method_selected = content1.split('!')[0]
		nameApp = content1.split('!')[1]

		# Get the thread of the method
		thread = database.get_thread(method_selected)

		# Get all the data of this thread with 'Function: 1' for method_selected
		data = database.get_particular_selected(method_selected, thread)

		print("INTERESTING")
		print(data)

		# Calculate the positions for these data
		precomputed_pos, rect_data, maximum_height, maximum_width = precalc.precalc(data)

		print("method_selected")
		print(method_selected)

		line_it = None
		for j in range(0, len(rect_data)):
			if(rect_data[j]['Method'].split('(')[0] == method_selected):
				line_it = j
				break

		print("before")
		print("line_it")
		print(line_it)

		# line_it = rect_data[line_it]['Line_no']

		# print("after")
		# print("line_it")
		# print(line_it)

		# line_it = None
		# for j in range(0, len(d)):
		# 	for i in range(0, len(rect_data)):
		# 		if(rect_data[i]['Method'].split('(')[0] == method_selected):
		# 			line_it = i
		# 			break
		
		autoscroll_position_index = -1

		if(line_it != None):
			autoscroll_position_index = line_it

		for i in range(0, len(precomputed_pos)):
			precomputed_pos[i].pop(0)

		to_send1 = []
		to_send1.append(precomputed_pos)
		to_send1.append(rect_data)
		to_send1.append(maximum_height)
		to_send1.append(maximum_width)
		to_send1.append(autoscroll_position_index)

		method_found = ""
		clean_code = []
		character = []
		line_no = []
		clean_code.append("Line_nos")
		to_send2 = clean_code + line_no

		character.insert(0, "Character_nos")
		to_send2 = to_send2 + character

		to_send2.append(method_found)

		to_send = []
		to_send.append(to_send1)
		to_send.append(to_send2)

		get_the_graph.forming(method_selected)
		selectedThread = get_the_graph.getThread(method_selected)
		# getTheGraph.forming(method_selected)
		nodes, edges = input_json.getvalues('raw_data.json')
		elem.append(nodes)
		elem.append([0])
		elem.append(edges)
		elem.append([100])
		elem.append(selectedThread)

		elem.append("separator")
		elem.append(to_send)
		return json.dumps(elem)

# OLD VERSION
# @app.route("/flowchart", methods=['GET','POST'])
# def flowchart():
# 	elem = []
# 	if(request.method == 'POST'):
# 		if os.path.exists("raw_data.json"):
# 			os.remove("raw_data.json")
# 		# The name of the request method should go in as an arg here
# 		# get_the_graph.forming('android.app.Application.onCreate')
# 		content1 = request.get_json()
# 		print("content1: ", content1)
# 		method_selected = content1.split('!')[0]
# 		nameApp = content1.split('!')[1]
# 		print("SelectInStackNameApp: ", nameApp)

# 		data = database.get_particular_selected(method_selected)

# 		d = database.getline(method_selected)

# 		precomputed_pos, rect_data, maximum_height, maximum_width = precalc.precalc(data)

# 		line_it = None
# 		for j in range(0, len(d)):
# 			for i in range(0, len(rect_data)):
# 				if(rect_data[i]['Method'].split('(')[0] == method_selected):
# 					line_it = i
# 					break
		
# 		autoscroll_position_index = -1

# 		if(line_it != None):
# 			autoscroll_position_index = line_it

# 		for i in range(0, len(precomputed_pos)):
# 			precomputed_pos[i].pop(0)

# 		to_send1 = []
# 		to_send1.append(precomputed_pos)
# 		to_send1.append(rect_data)
# 		to_send1.append(maximum_height)
# 		to_send1.append(maximum_width)
# 		to_send1.append(autoscroll_position_index)

# 		method_found = ""
# 		clean_code = []
# 		character = []
# 		line_no = []
# 		clean_code.append("Line_nos")
# 		to_send2 = clean_code + line_no

# 		character.insert(0, "Character_nos")
# 		to_send2 = to_send2 + character

# 		to_send2.append(method_found)

# 		to_send = []
# 		to_send.append(to_send1)
# 		to_send.append(to_send2)

# 		get_the_graph.forming(method_selected)
# 		selectedThread = get_the_graph.getThread(method_selected)
# 		# getTheGraph.forming(method_selected)
# 		nodes, edges = input_json.getvalues('raw_data.json')
# 		elem.append(nodes)
# 		elem.append([0])
# 		elem.append(edges)
# 		elem.append([100])
# 		elem.append(selectedThread)

# 		elem.append("separator")
# 		elem.append(to_send)
# 		return json.dumps(elem)
#	# return render_template('flowchart.html', elem = elem)

if __name__=='__main__':
    app.run(host="0.0.0.0", port=4444)