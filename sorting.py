import json

def sorting(data):
	def sortminy(val): 
	    return val[1][1]  

	def sortmaxy(val): 
	    return val[3][1]  
	  
	# # open output file for reading
	# with open('positions.txt', 'r') as filehandle:
	#     basicList = json.load(filehandle)

	copy_of_data_for_miny = data
	copy_of_data_for_maxy = data

	# Sorting positions in ascending order for miny --> Coordinate_b of each rectangle
	# copy_of_data_for_miny.sort(key = sortminy) 

	# Sorting positions in ascending order for maxy --> Coordinate_d of each rectangle
	# copy_of_data_for_maxy.sort(key = sortmaxy)

	return copy_of_data_for_miny, copy_of_data_for_maxy


def get_values_in_bounding_box(miny, bb_a, bb_b, bb_c, bb_d, rect_data):
	res = []
	rectangle_data = []
	for i in range(0, len(miny)):
		if(miny[i][1][1]>=bb_b[1] and miny[i][3][1]<=bb_d[1]):
			res.append(miny[i])
			rectangle_data.append(rect_data[i])
		if(miny[i][3][1]>=bb_b[1] and miny[i][3][1]<=bb_d[1] and miny[i][1][1]<=bb_b[1]):
			res.append(miny[i])
			rectangle_data.append(rect_data[i])
		if(miny[i][1][1]<=bb_d[1] and miny[i][3][1]>=bb_d[1] and miny[i][1][1]>=bb_b[1]):
			res.append(miny[i])
			rectangle_data.append(rect_data[i])
		if(miny[i][1][1]<=bb_b[1] and miny[i][3][1]>=bb_d[1]):
			res.append(miny[i])
			rectangle_data.append(rect_data[i])
	return res, rectangle_data;
		
		
