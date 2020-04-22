import json

def getvalues(filename):
	with open(filename) as json_file:
	    data = json.load(json_file)

	nodes = []
	for i in range(len(data["Nodes"])):
		temp_val = {}
		nodes_val = {}
		temp_val["id"] = data["Nodes"][i]["ID"]
		temp_val["name"] = data["Nodes"][i]["functionFound"].split("(")[0]
		if(data["Nodes"][i]["parent"] != -1):
			temp_val["parent"] = data["Nodes"][i]["parent"]
		temp_val["link"] = data["Nodes"][i]["link"]
		nodes_val["data"] = temp_val
		nodes.append(nodes_val)


	edges = []
	for i in range(len(data["Edges"])):
		for j in range(len(data["Edges"][i]["Destination"])):
			temp_val = {}
			nodes_val = {}
			temp_val["source"] = data["Edges"][i]["Source"]
			temp_val["target"] = data["Edges"][i]["Destination"][j]
			temp_val["weight"] = data["Edges"][i]["Handler"]
			nodes_val["data"] = temp_val
			edges.append(nodes_val)
	
	return nodes, edges