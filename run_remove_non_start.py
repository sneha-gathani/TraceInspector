import os
import json
import pandas as pd
import numpy as np
import time
import filter_method_calls
import sys

class Stack:
    def __init__(self):
        self.stack = []

    def add(self, dataval):
    # Use list append method to add element
        self.stack.append(dataval)

    # Use peek to look at the top of the stack
    def peek(self):     
        if(len(self.stack) == 0):
            return -1
        return self.stack[-1]

    # Use list pop method to remove element
    def pop(self):
        if(len(self.stack) == 0):
            return self.stack
        return self.stack.pop()

    # Use to give the size of the stack
    def size(self):
        return len(self.stack)

    # returns stack in form of array in LIFO manner
    def toArray(self):
        return self.stack[::-1]

    # returns stack in form of list
    def toNormalArray(self):
        return self.stack

    # clears the stack and returns empty stack
    def clear(self):
        return self.stack.clear()

# OLD WORKING
# def remove_non_start():
# 	start = time.time()
# 	line_number = Stack()
# 	name = Stack()
# 	iotype = Stack()

# 	df = pd.read_csv('only_method_calls.txt', sep=" ", header=None)
# 	df.columns = ["Call", "IO", "ThreadID", "Method", "BBEntry"]
# 	distinct_thread_id = df.ThreadID.unique()

# 	final_line_nums = []
# 	for i in range(0, len(distinct_thread_id)):
# 		certain_thread = df.loc[df['ThreadID'] == distinct_thread_id[i]]
# 		# certain_thread = df.loc[df['ThreadID'] == 1]
# 		certain_thread['lineno'] = certain_thread.index
# 		only_method_type = certain_thread.loc[certain_thread['Call'] == "Method"]
# 		only_method_type.reset_index(inplace = True)
# 		# only_method_type[['Method','Args']] = only_method_type.Method.str.split("(",expand=True,)
# 		only_method_type['Method'] = only_method_type.Method.str.split("(")
# 		for j in range(0, len(only_method_type)):
# 			if(line_number.size() == 0 or name.peek()!=only_method_type['Method'][j][0]):
# 				line_number.add(only_method_type['lineno'][j])
# 				name.add(only_method_type['Method'][j][0])
# 				iotype.add(only_method_type['IO'][j])
# 			elif(name.peek()==only_method_type['Method'][j][0] and only_method_type['IO'][j][0] == '<' and iotype.peek() == '>'):
# 				line_number.pop()
# 				name.pop()
# 				iotype.pop()
# 			else:
# 				final_line_nums.append(only_method_type['lineno'][j])
# 				final_line_nums.append(line_number.peek())
# 				line_number.pop()
# 				name.pop()
# 				iotype.pop()
# 	df = df.drop(final_line_nums)
# 	np.savetxt('hello.txt', df.values, fmt='%s', delimiter=" ")

def removeAPI(filename):
	file = []
	with open(filename) as f:
		for line in f:
			if(line != ''):
				file.append(line)

	finalLines = []
	i = 0
	j = 1
	while(j < len(file)):
		linei = file[i].split(" ")
		linej = file[j].split(" ")
		if(linei[1] == '>' and linei[0] == 'API'):
			if(linej[0] == 'Method'):
				i = i + 1
				j = j + 1
			elif(linej[0] == 'API' and linej[1] == '<'):
				finalLines.append(file[i])
				finalLines.append(file[j])
				i = i + 2
				j = j + 2
			else:
				i = i + 1
				j = j + 1
		elif(linei[0] == 'API' and linei[1] == '<'):
			i = i + 1
			j = j + 1
		else:	
			finalLines.append(file[i])
			i = i + 1
			j = j + 1
	
	j = j - 1
	if(j < len(file)):
		finalLines.append(file[j])

	with open('hello1.txt', 'w') as f:
		for item in finalLines:
			f.write("%s\n" % item)

# NEW
def remove_non_start(filename):
	line_number = Stack()
	name = Stack()
	iotype = Stack()

	df = pd.read_csv(filename, sep=" ", header=None)
	df.columns = ["Call", "IO", "ThreadID", "Method", "BBEntry"]
	distinct_thread_id = df.ThreadID.unique()

	final_line_nums = []
	for i in range(0, len(distinct_thread_id)):
		certain_thread = df.loc[df['ThreadID'] == distinct_thread_id[i]]
		# certain_thread = df.loc[df['ThreadID'] == 1]
		certain_thread['lineno'] = certain_thread.index
		only_method_type = certain_thread.loc[certain_thread['Call'] == "Method"]
		only_method_type.reset_index(inplace = True)
		# only_method_type[['Method','Args']] = only_method_type.Method.str.split("(",expand=True,)
		only_method_type['Method'] = only_method_type.Method.str.split("(")
		for j in range(0, len(only_method_type)):
			if(line_number.size() == 0 or name.peek()!=only_method_type['Method'][j][0]):
				line_number.add(only_method_type['lineno'][j])
				name.add(only_method_type['Method'][j][0])
				iotype.add(only_method_type['IO'][j])
			elif(name.peek()==only_method_type['Method'][j][0] and only_method_type['IO'][j][0] == '<' and iotype.peek() == '>'):
				line_number.pop()
				name.pop()
				iotype.pop()
			else:
				final_line_nums.append(only_method_type['lineno'][j])
				final_line_nums.append(line_number.peek())
				line_number.pop()
				name.pop()
				iotype.pop()
	df = df.drop(final_line_nums)
	np.savetxt('hello.txt', df.values, fmt='%s', delimiter=" ")	


# # NEW
# def remove_non_start(filename):
# 	line_number = Stack()
# 	name = Stack()
# 	iotype = Stack()

# 	df = pd.read_csv(filename, sep=" ", header=None)
# 	df.columns = ["Call", "IO", "ThreadID", "Method", "BBEntry"]
# 	distinct_thread_id = df.ThreadID.unique()

# 	final_line_nums = []
# 	for i in range(0, len(distinct_thread_id)):
# 		certain_thread = df.loc[df['ThreadID'] == distinct_thread_id[i]]
# 		# certain_thread = df.loc[df['ThreadID'] == 1]
# 		certain_thread['lineno'] = certain_thread.index
# 		only_method_type = certain_thread.loc[certain_thread['Call'] == "Method"]
# 		only_method_type.reset_index(inplace = True)
# 		# only_method_type[['Method','Args']] = only_method_type.Method.str.split("(",expand=True,)
# 		only_method_type['Method'] = only_method_type.Method.str.split("(")
# 		for j in range(0, len(only_method_type)):
# 			if(line_number.size() == 0 or name.peek()!=only_method_type['Method'][j][0]):
# 				line_number.add(only_method_type['lineno'][j])
# 				name.add(only_method_type['Method'][j][0])
# 				iotype.add(only_method_type['IO'][j])
# 			elif(name.peek()==only_method_type['Method'][j][0] and only_method_type['IO'][j][0] == '<' and iotype.peek() == '>'):
# 				line_number.pop()
# 				name.pop()
# 				iotype.pop()
# 			else:
# 				final_line_nums.append(only_method_type['lineno'][j])
# 				final_line_nums.append(line_number.peek())
# 				line_number.pop()
# 				name.pop()
# 				iotype.pop()
# 	df = df.drop(final_line_nums)
# 	np.savetxt('hello.txt', df.values, fmt='%s', delimiter=" ")