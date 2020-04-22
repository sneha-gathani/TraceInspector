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
			print(i)
			if(direction[i] == '>' and type_of_function[i] == 'Method'):
				if(temporary.count(method[i]) > 0):
					temporary.remove(method[i])
					line_no.pop()
					type_of_function.pop()
					direction.pop()
					method.pop()
					args.pop()
					i = i - 1
					print("number 1")
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
				print("number 2")
				temporary.append(method[i])
				line_no.pop()
				type_of_function.pop()
				direction.pop()
				method.pop()
				args.pop()
				i = i - 1
			# if(direction[i] == '<' and type_of_function[i] == 'Method'):
			# 	tt = method[i]
			# 	line_no.pop()
			# 	type_of_function.pop()
			# 	direction.pop()
			# 	method.pop()
			# 	args.pop()
			# 	i = i - 1
			# 	if(direction[i] == '>' and type_of_function[i] == 'Method' and method[i] == tt):
			# 		line_no.pop()
			# 		type_of_function.pop()
			# 		direction.pop()
			# 		args.pop()
			# 		i = i - 1
			# elif(type_of_function[i] == 'API'):
			# 	line_no.pop()
			# 	type_of_function.pop()
			# 	direction.pop()
			# 	method.pop()
			# 	args.pop()
			# 	i = i - 1

	# Look for all API's having particular handler of interest 
	def look_for_api(line_no, type_of_function, direction, method, args, interested_handler):
		i = len(method) - 2
		node_for_nodes = []
		node_for_queue = []
		while(i >= 0 ):
			if(type_of_function[i] == "API" and args[i] != None and interested_handler != None):
				if(args[i].find(interested_handler) >= 0):
					node_for_queue.append({"Line_no": line_no[i], "Handler": interested_handler})
					if(direction[i] == "<"):
						i = i - 1
			i = i - 1
		return node_for_queue


	def process(line_no, type_of_function, direction, method, args, handler_of_interest, Nodes, Edges, back_from_method, destination_node, source_node):
		api_for_queue = look_for_api(line_no, type_of_function, direction, method, args, handler_of_interest)
		print("In process")
		print(api_for_queue)

		# Find correspondind methods of these, add to nodes and add to queue
		for i in range(0, len(api_for_queue)):
			back_from_method = look_for_method(line_no[:api_for_queue[i]["Line_no"]], type_of_function[:api_for_queue[i]["Line_no"]], direction[:api_for_queue[i]["Line_no"]], method[:api_for_queue[i]["Line_no"]], args[:api_for_queue[i]["Line_no"]])
			print(back_from_method)
			Nodes.append(add_node_for_nodes(back_from_method[0], back_from_method[1], handler_of_interest))
			destination_node.append(add_node_for_nodes(back_from_method[0], back_from_method[1], handler_of_interest))
			queue.append(back_from_method[0])
		
		# Make Edges
		make_edges(source_node, destination_node)
		print("queue")
		print(queue)
		while(len(queue) > 0):
			print("Inside the queue")
			queue_top = queue.pop(0)
			line_no1 = line_no[:queue_top]
			type_of_function1 = type_of_function[:queue_top]
			direction1 = direction[:queue_top]
			method1 = method[:queue_top]
			args1 = args[:queue_top]

			print(line_no1[-1])
			print(type_of_function1[-1])
			print(direction1[-1])
			print(method1[-1])
			print(args1[-1])

			handler_of_interest = args1[-1]
			print(handler_of_interest)
			destination_node = []
			source_node = add_node_for_nodes(line_no1[-1], method1[-1], handler_of_interest)

			api_for_queue = look_for_api(line_no1, type_of_function1, direction1, method1, args1, handler_of_interest)

			# Find correspondind methods of these, add to nodes and add to queue
			for i in range(0, len(api_for_queue)):
				back_from_method = look_for_method(line_no[:api_for_queue[i]["Line_no"]], type_of_function[:api_for_queue[i]["Line_no"]], direction[:api_for_queue[i]["Line_no"]], method[:api_for_queue[i]["Line_no"]], args[:api_for_queue[i]["Line_no"]])
				Nodes.append(add_node_for_nodes(back_from_method[0], back_from_method[1], handler_of_interest))
				destination_node.append(add_node_for_nodes(back_from_method[0], back_from_method[1], handler_of_interest))
				queue.append(back_from_method[0])

			# Make Edges
			if(len(destination_node) > 0):
				make_edges(source_node, destination_node)

		print("Nodes")
		print(Nodes)
		print("Edges")
		print(Edges)

		Nodes = dict((v['ID'],v) for v in Nodes).values()
		Edges = dict((w['Source'],w) for w in Edges).values()

		print("Nodes")
		print(Nodes)
		print("Edges")
		print(Edges)

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

		# Finally put all the data in a dictionary to be passed to the flowchart() functio
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

	print("Data size")
	print(len(data))

	print("Last data")
	print(data[-1])

	if(data[-1]['Type'] == 'API'):
		data = data[:-1]
		# Put everything into stacks
		line_no = []
		type_of_function = []
		direction = []
		method = []
		args = []

		p = 1
		for i in range(0, len(data)):
			if(data[i]['Thread_ID'] == interested_thread_id):
				# if(data[i]['Direction'] == ">"):
				line_no.append(p)
				type_of_function.append(data[i]['Type'])
				direction.append(data[i]['Direction'])
				method.append(data[i]['Method'])
				args.append(data[i]['Args'])
				p = p + 1

		# Initialize an empty queue
		queue = []
		handler_of_interest = args[-1]

		destination_node = []

		print("LAst couple of methods")
		print(method[-15:])
		print("LAst couple of type")
		print(type_of_function[-15:])
		print("LAst couple of direction")
		print(direction[-15:])

		back_from_method = look_for_method(line_no, type_of_function, direction, method, args)
		print(back_from_method)
		print("BACK FROM METHOD")
		print(back_from_method)
		Nodes.append(add_node_for_nodes(back_from_method[0], back_from_method[1], handler_of_interest))
		source_node = Nodes[-1]
		# Edges

		line_no = line_no[:back_from_method[0]]
		type_of_function = type_of_function[:back_from_method[0]]
		direction = direction[:back_from_method[0]]
		method = method[:back_from_method[0]]
		args = args[:back_from_method[0]]
		process(line_no, type_of_function, direction, method, args, handler_of_interest, Nodes, Edges, back_from_method, destination_node, source_node)
	else:
		if(data[-1]['Method'] != method_of_interest):
			data = data[:-1]

		# Put everything into stacks
		line_no = []
		type_of_function = []
		direction = []
		method = []
		args = []

		p = 1
		for i in range(0, len(data)):
			if(data[i]['Thread_ID'] == interested_thread_id):
				# if(data[i]['Direction'] == ">"):
				line_no.append(p)
				type_of_function.append(data[i]['Type'])
				direction.append(data[i]['Direction'])
				method.append(data[i]['Method'])
				args.append(data[i]['Args'])
				p = p + 1

		# Initialize an empty queue
		queue = []
	
		destination_node = []

		handlers = []
		while(1):
			if(args[-1].find(',')):
				a = args[-1].split(',')
				for i in range(0, len(a)):
					handlers.append(a[i])
				break
			else:
				handlers.append(args[-1])
				break

		for pp in range(0, len(handlers)):

			handler_of_interest = handlers[pp]
			back_from_method = (line_no[-1], method[-1], handler_of_interest)
			Nodes.append(add_node_for_nodes(back_from_method[0], back_from_method[1], handler_of_interest))

			source_node = Nodes[-1]
			# handler_of_interest = Nodes[pp][2]
			# Edges

			line_no1 = line_no[:back_from_method[0]]
			type_of_function1 = type_of_function[:back_from_method[0]]
			direction1 = direction[:back_from_method[0]]
			method1 = method[:back_from_method[0]]
			args1 = args[:back_from_method[0]]

			api_for_queue = look_for_api(line_no1, type_of_function1, direction1, method1, args1, handler_of_interest)

			# Find correspondind methods of these, add to nodes and add to queue
			for i in range(0, len(api_for_queue)):
				back_from_method = look_for_method(line_no1[:api_for_queue[i]["Line_no"]], type_of_function1[:api_for_queue[i]["Line_no"]], direction1[:api_for_queue[i]["Line_no"]], method1[:api_for_queue[i]["Line_no"]], args1[:api_for_queue[i]["Line_no"]])
				Nodes.append(add_node_for_nodes(back_from_method[0], back_from_method[1], handler_of_interest))
				destination_node.append(add_node_for_nodes(back_from_method[0], back_from_method[1], handler_of_interest))
				queue.append(back_from_method[0])
			
			# Make Edges
			if(len(destination_node) > 0):
				make_edges(source_node, destination_node)

			print("AFTER FIRST HALF")
			print("Nodes")
			print(Nodes)
			print("Edges")
			print(Edges)

		# while(len(queue) > 0):
		# 	queue_top = queue.pop(0)
		# 	line_no1 = line_no[:queue_top]
		# 	type_of_function1 = type_of_function[:queue_top]
		# 	direction1 = direction[:queue_top]
		# 	method1 = method[:queue_top]
		# 	args1 = args[:queue_top]

		# 	handler_of_interest = args1[-1]
		# 	destination_node = []
		# 	source_node = add_node_for_nodes(line_no1[-1], method1[-1], handler_of_interest)

		# 	api_for_queue = look_for_api(line_no1, type_of_function1, direction1, method1, args1, handler_of_interest)

		# 	# Find correspondind methods of these, add to nodes and add to queue
		# 	for i in range(0, len(api_for_queue)):
		# 		back_from_method = look_for_method(line_no[:api_for_queue[i]["Line_no"]], type_of_function[:api_for_queue[i]["Line_no"]], direction[:api_for_queue[i]["Line_no"]], method[:api_for_queue[i]["Line_no"]], args[:api_for_queue[i]["Line_no"]])
		# 		Nodes.append(add_node_for_nodes(back_from_method[0], back_from_method[1], handler_of_interest))
		# 		destination_node.append(add_node_for_nodes(back_from_method[0], back_from_method[1], handler_of_interest))
		# 		queue.append(back_from_method[0])

		# 	# Make Edges
		# 	if(len(destination_node) > 0):
		# 		make_edges(source_node, destination_node)

		def intersection(lst1, lst2): 
		    lst3 = [value for value in lst1 if value in lst2] 
		    return lst3 

		finalEdges = []
		i = 0
		if(len(Edges) == 1):
			finalEdges = Edges
		else:
			while(i < len(Edges) - 1):
				ei = Edges[i]
				ei1 = Edges[i+1]
				if(ei['Source'] == ei1['Source']):
					intersectedArray = intersection(ei['Destination'], ei1['Destination'])
					if(len(ei['Destination']) > len(ei1['Destination'])):
						o = i
						others = list(set(ei['Destination']) - set(intersectedArray))
					else:
						o = i + 1
						others = list(set(ei1['Destination']) - set(intersectedArray))
					finalEdges.append({'Source': ei['Source'], 'Destination': intersectedArray, 'Handler': ei['Handler'] + " " + ei1['Handler']})
					finalEdges.append({'Source': Edges[o]['Source'], 'Destination': others, 'Handler': Edges[o]['Handler']})
				i = i + 1


		print("THIS IS IMPORTANT")
		# for i in range(0, len(Edges)):
		# 	temp = []
		# 	temp.append(Edges[i]) # finalEdges = dict((v['Source'],v) for v in temp).values()
		# 	finalEdges = (v['Source'],v) for v in temp
		# 	print(i)
		# 	print(finalEdges)

		finalNodes = dict((v['ID'],v) for v in Nodes).values()
		print("Example Nodes and Edges")

		Edges = finalEdges
		Nodes = finalNodes
		print("Final Nodes")
		print(Nodes)
		print("Final Edges")
		print(Edges)

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



		#com.facebook.FacebookSdk.isDebugEnabled
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

		# Finally put all the data in a dictionary to be passed to the flowchart() functio
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