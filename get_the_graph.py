import psycopg2
import config
import json
import math
import os
import pickle
from decimal import *
from operator import itemgetter

db_config = config.config()

def get_connection(config):
    conn = psycopg2.connect(**config)
    return conn

def getThread(method_selected):
	conn = get_connection(db_config)
	cursor = conn.cursor()

	# Find the tuple uptil which data is required
	cursor.execute("SELECT thread_id FROM log WHERE method = '{}' LIMIT 1".format(method_selected))
	line_found = []
	columns = ('Thread_ID')
	for row in cursor.fetchall():
		line_found.append(dict(zip(columns, row)))

	print(line_found)
	interested_thread_id = line_found[0]['T']
	return interested_thread_id

# Actually makes the graph
def forming(method_of_interest):
	# Makes the parts, that is, the nodes and edges of the actual data structure to be passed to the flowchart() function
	Nodes = []
	Edges = []

	def make_edges(source, destination):
		children = []
		for i in range(0, len(destination)):
			if(children.count(destination[i]["ID"]) == 0):
				children.append(destination[i]["ID"])
		edges_key = {"Source", "Destination", "Handler"}
		edges_data = {key: None for key in edges_key}
		edges_data["Source"] = source["ID"]
		edges_data["Destination"] = children
		edges_data["Handler"] = source["handlerName"]
		Edges.append(edges_data)


	# Adds individual nodes
	def add_node_for_nodes(id, method, handler):
		key_node = {"ID", "functionFound", "handlerName", "parent"}
		individual_node = {key: None for key in key_node}
		individual_node["ID"] = id
		individual_node["functionFound"] = method
		individual_node["parent"] = -1
		if(handler == None):
			individual_node["handlerName"] = ""
		else:
			individual_node["handlerName"] = handler.split("@")[0]
		return individual_node

	# Look for immediate method above the interested API
	def look_for_method(line_no, type_of_function, direction, method, args):
		i = len(method) - 1
		if(i == 0):
			return line_no[i], method[i], args[i]
		while(type_of_function[i] == 'API'):
			line_no.pop()
			type_of_function.pop()
			direction.pop()
			method.pop()
			args.pop()
			i = i - 1
		temporary = []
		while(i >= 0):
			if(direction[i] == '>' and type_of_function[i] == 'Method'):
				if(temporary.count(method[i]) > 0):
					temporary.remove(method[i])
					line_no.pop()
					type_of_function.pop()
					direction.pop()
					method.pop()
					args.pop()
					i = i - 1
				else:
					return line_no[i], method[i], args[i]
			while(type_of_function[i] == 'API'):
				line_no.pop()
				type_of_function.pop()
				direction.pop()
				method.pop()
				args.pop()
				i = i - 1
			if(direction[i] == '<' and type_of_function[i] == 'Method'):
				temporary.append(method[i])
				line_no.pop()
				type_of_function.pop()
				direction.pop()
				method.pop()
				args.pop()
				i = i - 1

	# Look for all API's having particular handler of interest 
	def look_for_api(line_no, type_of_function, direction, method, args, interested_handler):
		i = len(method) - 2
		node_for_nodes = []
		node_for_queue = []
		# Get only the first argument of the method
		print("Interested Handler")
		print(interested_handler)
		if(interested_handler is not None and interested_handler.find(',')):
			interested_handler = interested_handler.split(',')[0]
		while(i >= 0):
			if(type_of_function[i] == "API" and args[i] != None and interested_handler != None):
				if(args[i].find(interested_handler) >= 0):
					node_for_queue.append({"Line_no": line_no[i], "Handler": interested_handler})
					if(direction[i] == "<"):
						i = i - 1
			i = i - 1
		return node_for_queue


	conn = get_connection(db_config)
	cursor = conn.cursor()

	# Find the tuple uptil which data is required
	cursor.execute("SELECT line_no, thread_id FROM log WHERE method = '{}'".format(method_of_interest))
	line_found = []
	columns = ('Line_no', 'Thread_ID')
	for row in cursor.fetchall():
		line_found.append(dict(zip(columns, row)))

	interested_line_number = line_found[0]['Line_no']
	interested_thread_id = line_found[0]['Thread_ID']


	# Get all this data and store in data
	cursor.execute("SELECT line_no, type, thread_id, direction, method, args FROM log LIMIT {}".format(interested_line_number + 1))
	data = []
	columns = ('Line_no', 'Type', 'Thread_ID', 'Direction', 'Method', 'Args')
	for row in cursor.fetchall():
		data.append(dict(zip(columns, row)))
	
	cursor.close()
	conn.close()


	# Put everything into stacks
	line_no = []
	type_of_function = []
	direction = []
	method = []
	args = []

	p = 1
	for i in range(0, len(data)):
		if(data[i]['Thread_ID'] == interested_thread_id):
			line_no.append(p)
			type_of_function.append(data[i]['Type'])
			direction.append(data[i]['Direction'])
			method.append(data[i]['Method'])
			args.append(data[i]['Args'])
			p = p + 1

	# Initialize an empty queue
	queue = []

	if(type_of_function[-1] == 'API'):
		line_no = line_no[:-1]
		type_of_function = type_of_function[:-1]
		direction = direction[:-1]
		method = method[:-1]
		args = args[:-1]
		handler_of_interest = args[-1]
	else:
		handler_of_interest = args[-1]
		line_no = line_no[:-1]
		type_of_function = type_of_function[:-1]
		direction = direction[:-1]
		method = method[:-1]
		args = args[:-1]

	destination_node = []

	back_from_method = look_for_method(line_no, type_of_function, direction, method, args)

	Nodes.append(add_node_for_nodes(back_from_method[0], back_from_method[1], handler_of_interest))
	source_node = Nodes[-1]
	# Edges

	line_no = line_no[:back_from_method[0]]
	type_of_function = type_of_function[:back_from_method[0]]
	direction = direction[:back_from_method[0]]
	method = method[:back_from_method[0]]
	args = args[:back_from_method[0]]

	# I just added this
	handler_of_interest = args[-1]

	api_for_queue = look_for_api(line_no, type_of_function, direction, method, args, handler_of_interest)

	# Find correspondind methods of these, add to nodes and add to queue
	for i in range(0, len(api_for_queue)):
		back_from_method = look_for_method(line_no[:api_for_queue[i]["Line_no"]], type_of_function[:api_for_queue[i]["Line_no"]], direction[:api_for_queue[i]["Line_no"]], method[:api_for_queue[i]["Line_no"]], args[:api_for_queue[i]["Line_no"]])
		Nodes.append(add_node_for_nodes(back_from_method[0], back_from_method[1], handler_of_interest))
		destination_node.append(add_node_for_nodes(back_from_method[0], back_from_method[1], handler_of_interest))
		queue.append(back_from_method[0])
	
	# Make Edges
	make_edges(source_node, destination_node)

	while(len(queue) > 0):
		queue_top = queue.pop(0)
		line_no = line_no[:queue_top]
		type_of_function = type_of_function[:queue_top]
		direction = direction[:queue_top]
		method = method[:queue_top]
		args = args[:queue_top]

		handler_of_interest = args[-1]
		destination_node = []
		source_node = add_node_for_nodes(line_no[-1], method[-1], handler_of_interest)

		api_for_queue = look_for_api(line_no, type_of_function, direction, method, args, handler_of_interest)

		# Find correspondind methods of these, add to nodes and add to queue
		for i in range(0, len(api_for_queue)):
			back_from_method = look_for_method(line_no[:api_for_queue[i]["Line_no"]], type_of_function[:api_for_queue[i]["Line_no"]], direction[:api_for_queue[i]["Line_no"]], method[:api_for_queue[i]["Line_no"]], args[:api_for_queue[i]["Line_no"]])
			Nodes.append(add_node_for_nodes(back_from_method[0], back_from_method[1], handler_of_interest))
			destination_node.append(add_node_for_nodes(back_from_method[0], back_from_method[1], handler_of_interest))
			queue.append(back_from_method[0])

		# Make Edges
		if(len(destination_node) > 0):
			make_edges(source_node, destination_node)

	Nodes = dict((v['ID'],v) for v in Nodes).values()
	Edges = dict((w['Source'],w) for w in Edges).values()

	# Make the compund nodes
	# Make the compound node changes for all the nodes
	def changed_node_for_nodes(id, method, handler, parent, link):
		key_node = {"ID", "functionFound", "handlerName", "parent"}
		individual_node = {key: None for key in key_node}
		individual_node["ID"] = id
		individual_node["functionFound"] = method
		individual_node["parent"] = parent
		individual_node["handlerName"] = handler
		individual_node["link"] = link
		return individual_node


	new_Nodes = []
	Nodes = sorted(Nodes, key = itemgetter('handlerName'))
	if(len(Nodes) == 1):
		split_names = Nodes[0]["functionFound"].split(".")
		temp_first_two = split_names[0] + "." + split_names[1]
		remaining_size = len(split_names[2:])
		i_remaining_size = 2

		remaining = ""
		while(remaining_size > 0):
			remaining = remaining + split_names[i_remaining_size] + "."
			i_remaining_size += 1
			remaining_size -= 1
		new_Nodes.append(changed_node_for_nodes(1, temp_first_two, Nodes[0]["handlerName"], -1, ""))
		new_Nodes.append(changed_node_for_nodes(Nodes[0]["ID"], remaining, Nodes[0]["handlerName"], 1, Nodes[0]["functionFound"]))
	else:
		len_Nodes = len(Nodes)
		i_len_Nodes = 0
		i = 0
		parent_node_id = 1
		while(i_len_Nodes < len_Nodes):
			stack_order = []

			split_names = Nodes[i]["functionFound"].split(".")
			temp_first_two = split_names[0] + "." + split_names[1]
			stack_order.append(Nodes[i])
			i += 1
			flag = 0

			if(i == len(Nodes)):
				break

			while(flag == 0):
				if(i >= len(Nodes)):
					break
				split_names = Nodes[i]["functionFound"].split(".")
				first_two = split_names[0] + "." + split_names[1]
				if(temp_first_two == first_two):
					stack_order.append(Nodes[i])
					i += 1
				else:
					flag = 1
			j = i - 1
			split_names = Nodes[j]["functionFound"].split(".")
			first_two = split_names[0] + "." + split_names[1]
			remaining_size = len(split_names[2:])
			i_remaining_size = 2

			remaining = ""
			while(remaining_size > 0):
				remaining = remaining + split_names[i_remaining_size] + "."
				i_remaining_size += 1
				remaining_size -= 1

			# remaining = remaining[:-1]
			new_Nodes.append(changed_node_for_nodes(parent_node_id, first_two, Nodes[j]["handlerName"], -1, ""))

			temp_stack_len = len(stack_order)

			while(len(stack_order) > 0):
				temporary = stack_order.pop()
				split_names = temporary["functionFound"].split(".")
				first_two = split_names[0] + "." + split_names[1]
				remaining_size = len(split_names[2:])
				i_remaining_size = 2

				remaining = ""
				while(remaining_size > 0):
					remaining = remaining + split_names[i_remaining_size] + "."
					i_remaining_size += 1
					remaining_size -= 1

				# remaining = remaining[:-1]
				new_Nodes.append(changed_node_for_nodes(temporary["ID"], remaining, temporary["handlerName"], parent_node_id, temporary["functionFound"]))

			parent_node_id += 1
			len_Nodes -= temp_stack_len

			if(i == len(Nodes)):
				break


	# Finally put all the data in a dictionary to be passed to the flowchart() function
	flowchart_data = []
	flowchart_data_key = {"Nodes", "Edges"}
	flowchart_data = {key: None for key in flowchart_data_key}
	flowchart_data["Nodes"] = list(new_Nodes)
	flowchart_data["Edges"] = list(Edges)

	# Writing it to a raw_data file
	if os.path.exists("raw_data.json"):
		os.remove("raw_data.json")

	with open("raw_data.json", "w") as write_file:
		json.dump(flowchart_data, write_file, sort_keys = True, indent = 4)

	# with open('raw_data.txt', 'w') as f:
	# 	f.write(str(flowchart_data))