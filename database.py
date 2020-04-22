import psycopg2
import config
import filter_method_calls
import json
import math
from decimal import *

db_config = config.config()
drop_table_sql = "DROP TABLE IF EXISTS log";

create_table_sql = """CREATE TABLE IF NOT EXISTS log(Line_no integer PRIMARY KEY, Type varchar(7) NOT NULL, Thread_ID integer NOT NULL, Direction char(1), BB_ID varchar(20), Method varchar(200), Args varchar(1000), Function CHAR(1));"""
insert_many_tuple_placeholder = """INSERT INTO log VALUES"""
insert_tuple_placeholder = """INSERT INTO log (Line_no, Type, Thread_ID, Direction, BB_ID, Method, Args, Function) VALUES (%s, %s, %s, %s, %s, %s, %s, 0)"""

distinct_thread_id_sql = """SELECT DISTINCT thread_id FROM log"""

distinct_thread_data_sql = """SELECT * FROM log WHERE Thread_ID = """

all_threads_data_sql = """SELECT * FROM log"""

string_match = """UPDATE log SET Function = '1' WHERE Method LIKE """

get_starting = """SELECT * FROM log WHERE thread_id = {st} AND type = 'Method' ORDER BY line_no LIMIT 1;"""
get_ending = """SELECT * FROM log WHERE thread_id = {ed} AND type = 'Method' ORDER BY line_no DESC LIMIT 1;"""

def get_connection(config) :
    conn = psycopg2.connect(**config)
    return conn

def create_database() :
    # get connection & cursor
    conn = get_connection(db_config)
    cursor = conn.cursor()

    # drop table if exists
    cursor.execute(drop_table_sql)
    cursor.close()
    conn.commit()
    conn.close()

    conn = get_connection(db_config)
    cursor = conn.cursor()
    # create table
    cursor.execute(create_table_sql)

    cursor.close()
    conn.commit()
    conn.close()

# def insert_rows(rows):
# 	conn = get_connection(db_config)
# 	cursor = conn.cursor()
# 	args_str = ','.join(cursor.mogrify("(%s,%s,%s,%s,%s,%s,%s, '0')", (
# 		row['Line_no'],
# 		row['Type'],
# 		row['Thread_ID'],
# 		row.get('Direction', None),
# 		row.get('BB_ID', None),
# 		row.get('Method', None),
# 		row.get('Args', None)
# 		)).decode('utf-8') for row in rows)
# 	cursor.execute(insert_many_tuple_placeholder + args_str)

# 	cursor.close()
# 	conn.commit()
# 	conn.close()
def insert_rows(rows):
	conn = get_connection(db_config)
	cursor = conn.cursor()
	args_str = ','.join(cursor.mogrify("(%s,%s,%s,%s,%s,%s,%s, '0')", (
		row['Line_no'],
		row['Type'],
		row['Thread_ID'],
		row['Direction'],
		row['BB_ID'],
		row['Method'],
		row['Args']
		)).decode('utf-8') for row in rows)
	cursor.execute(insert_many_tuple_placeholder + args_str)

	cursor.close()
	conn.commit()
	conn.close()

def select_all():
	conn = get_connection(db_config)
	cursor = conn.cursor()
	cursor.execute("""SELECT * FROM log;""")
	results = []
	columns = ('Line_no', 'Type', 'Thread_ID', 'Direction', 'BB_ID', 'Method', 'Args', 'Function')
	for row in cursor.fetchall():
		results.append(dict(zip(columns, row)))
	cursor.close()
	conn.close()
	return results

def select_direction():
	conn = get_connection(db_config)
	cursor = conn.cursor()
	cursor.execute(all_threads_data_sql)
	direction = []
	column_name = ('Line_no', 'Type', 'Thread_ID', 'Direction', 'Method', 'Args', 'Function')
	for row in cursor.fetchall():
		temp = dict(zip(column_name, row))
		if(temp['Direction']):
			direction.append(dict(zip(column_name, row)))	
	cursor.close()
	conn.close()
	return direction

def get_distinct_thread():
	conn = get_connection(db_config)
	cursor = conn.cursor()
	cursor.execute(distinct_thread_id_sql)
	thread_id = []
	for row in cursor.fetchall():
		for item in row:
			thread_id.append(item)
	cursor.close()
	conn.close()
	return thread_id

def get_distinct_thread_data(id):
	conn = get_connection(db_config)
	cursor = conn.cursor()
	if(id == " " or id == None):
		cursor.execute(all_threads_data_sql)
		data = []
		column_name = ('Line_no', 'Type', 'Thread_ID', 'Direction', 'Method', 'Args', 'Function')
		for row in cursor.fetchall():
			temp = dict(zip(column_name, row))
			if(temp['Direction']):
				data.append(dict(zip(column_name, row)))	
		cursor.close()
		conn.close()
		return data
	cursor.execute(distinct_thread_data_sql + str(id))
	data = []
	column_name = ('Line_no', 'Type', 'Thread_ID', 'Direction', 'Method', 'Args', 'Function')
	for row in cursor.fetchall():
		temp = dict(zip(column_name, row))
		if(temp['Direction']):
			data.append(dict(zip(column_name, row)))	
	cursor.close()
	conn.close()
	return data

def get_function_name(function_name):
	conn = get_connection(db_config)
	cursor = conn.cursor()
	cursor.execute("""UPDATE log SET Function = '0' """)
	if(function_name == " " or function_name == None):
		cursor.execute(all_threads_data_sql)
		data = []
		column_name = ('Line_no', 'Type', 'Thread_ID', 'Direction', 'Method', 'Args', 'Function')
		for row in cursor.fetchall():
			temp = dict(zip(column_name, row))
			if(temp['Direction']):
				data.append(dict(zip(column_name, row)))	
		cursor.close()
		conn.close()
		return data
	fun = "'%" + function_name + "%'"
	fun1 = "'%" + function_name
	fun2 = function_name + "%'"
	cursor.execute(string_match + fun + " OR Method LIKE " + fun1 + " OR Method LIKE " + fun2)
	column_name = ('Line_no', 'Type', 'Thread_ID', 'Direction', 'Method', 'Args', 'Function')
	data = []
	cursor.execute("""SELECT Line_no, Type, Thread_ID, Direction, Method, Args, Function FROM log""")
	for row in cursor.fetchall():
		temp = dict(zip(column_name, row))
		data.append(dict(zip(column_name, row)))
	cursor.close()
	conn.close()
	return data

# Actually sending the data in the form of dictionary to the server
def get_interactions(id, function_name, thread):
	conn = get_connection(db_config)
	cursor = conn.cursor()
	cursor.execute("""UPDATE log SET Function = '0' """)
	cursor.close()
	conn.close()
	conn = get_connection(db_config)
	cursor = conn.cursor()

	print(id)
	print(function_name)
	print(thread)

	# Filters such that "All" Threads and no function searched
	if((id == " " or id == None or id == "All") and (function_name == "" or function_name == None)):
		print("HERE 1")
		conn = get_connection(db_config)
		cursor = conn.cursor()
		cursor.execute("""SELECT * FROM log WHERE thread_id='1' ORDER BY line_no;""")
		data = []
		column_name = ('Line_no', 'Type', 'Thread_ID', 'Direction', 'BB_ID', 'Method', 'Args', 'Function')
		for row in cursor.fetchall():
			temp = dict(zip(column_name, row))
			data.append(dict(zip(column_name, row)))	
		cursor.close()
		conn.close()
		# print(data)
		return data

	# Filters such that some option of Threads and no function searched
	if((id != " " or id != None) and (function_name == "" or function_name == None)):
		print("HERE 2")
		conn = get_connection(db_config)
		cursor = conn.cursor()
		# SELECT * FROM log WHERE Thread_ID = 
		cc = """SELECT * FROM log WHERE Thread_ID = {t1} ORDER BY line_no;"""
		cursor.execute(cc.format(t1=id))
		data = []
		column_name = ('Line_no', 'Type', 'Thread_ID', 'Direction', 'BB_ID', 'Method', 'Args', 'Function')
		for row in cursor.fetchall():
			temp = dict(zip(column_name, row))
			if(temp['Direction']):
				data.append(dict(zip(column_name, row)))	
		cursor.close()
		conn.close()
		return data

	# Filters such that "All" Threads and some function searched
	if((id == " " or id == None) and (function_name != "" or function_name != None)):
		print("HERE 3")
		fun = "'%" + function_name + "%'"
		fun1 = "'%" + function_name
		fun2 = function_name + "%'"
		string_match_query = """WITH subquery AS (SELECT line_no FROM log WHERE method LIKE {f1} OR Method LIKE {f2} OR Method LIKE {f3}) UPDATE log SET function = '1' FROM subquery WHERE log.line_no = subquery.line_no;"""
		conn = get_connection(db_config)
		cursor = conn.cursor()
		cursor.execute(string_match_query.format(f1 = fun, f2 = fun1, f3 = fun2))
		cursor.execute(all_threads_data_sql + " ORDER BY line_no")
		data = []
		column_name = ('Line_no', 'Type', 'Thread_ID', 'Direction', 'BB_ID', 'Method', 'Args', 'Function')
		for row in cursor.fetchall():
			temp = dict(zip(column_name, row))
			if(temp['Direction']):
				data.append(dict(zip(column_name, row)))
		cursor.close()
		conn.close()
		return data

	# Filters such that some Thread option and some function searched
	if((id != " " or id != None) and (function_name != "" or function_name != None)):
		print("HERE 4")
		fun = "'%" + function_name + "%'"
		fun1 = "'%" + function_name
		fun2 = function_name + "%'"

		string_match_query = """WITH subquery AS (SELECT line_no FROM log WHERE method LIKE {f1} OR Method LIKE {f2} OR Method LIKE {f3}) UPDATE log SET function = '1' FROM subquery WHERE log.line_no = subquery.line_no;"""
		distinct_thread_data_with_string_match = """SELECT * FROM log WHERE thread_id = {t1} ORDER BY line_no;"""
		print("INNNN")
		print(id)
		if(id == 'All'):
			cursor.execute(string_match_query.format(f1 = fun, f2 = fun1, f3 = fun2))
			cursor.execute(all_threads_data_sql + " ORDER BY line_no")
		else:
			cursor.execute(string_match_query.format(f1 = fun, f2 = fun1, f3 = fun2))
			cursor.execute(distinct_thread_data_with_string_match.format(t1 = str(id)))
			
		data = []
		column_name = ('Line_no', 'Type', 'Thread_ID', 'Direction', 'BB_ID', 'Method', 'Args', 'Function')
		for row in cursor.fetchall():
			temp = dict(zip(column_name, row))
			if(temp['Direction']):
				data.append(dict(zip(column_name, row)))
		cursor.close()
		conn.close()
		return data

	cursor.close()
	conn.close()
	return data

def get_top_5_most_called_methods():
	conn = get_connection(db_config)
	cursor = conn.cursor()
	cursor.execute("""SELECT method, COUNT(method) AS temp FROM log GROUP BY method ORDER BY COUNT(method) DESC LIMIT 5;""")
	data = []
	column_name = ('MethodName', 'FrequencyofCalling')
	for row in cursor.fetchall():
		temp = dict(zip(column_name, row))
		data.append(dict(zip(column_name, row)))	
	cursor.close()
	conn.close()
	return data

def get_thread_line_nos(thread_id):
	conn = get_connection(db_config)
	cursor = conn.cursor()
	starting = []
	ending = []
	timeline_data = []

	cursor.execute("""SELECT * FROM log WHERE type = 'Method' ORDER BY line_no LIMIT 1;""")
	for row in cursor.fetchall():
		starting.append(row[0])
	cursor.execute("""SELECT * FROM log WHERE type = 'Method' ORDER BY line_no DESC LIMIT 1;""")
	for row in cursor.fetchall():
		ending.append(row[0])

	for i in range(0, len(thread_id)-1):
		# First line
		st_query = get_starting.format(st = thread_id[i])
		cursor.execute(st_query)
		for row in cursor.fetchall():
			starting.append(row[0])
		# Last line
		end_query = get_ending.format(ed = thread_id[i])
		cursor.execute(end_query)
		for row in cursor.fetchall():
			ending.append(row[0])

	for i in range(0, len(thread_id)):
		temp = {}
		temp["Thread"] = thread_id[i]
		temp["Starting"] = starting[i]
		temp["Value"] = ending[i] - starting[i]
		timeline_data.append(temp)

	cursor.close()
	conn.close()
	timeline_data = timeline_data[:-1]
	return starting, ending, timeline_data
# OLD VERSION
# def get_particular_selected(line):
# 	conn = get_connection(db_config)
# 	cursor = conn.cursor()
# 	cursor.execute("""UPDATE log SET Function = '0' """)
# 	cursor.close()
# 	conn.close()
# 	conn = get_connection(db_config)
# 	cursor = conn.cursor()

# 	query = """UPDATE log SET function = '1' WHERE method = '{l1}';"""
# 	cursor.execute(query.format(l1 = line))
# 	cursor.execute(all_threads_data_sql + " ORDER BY line_no")
# 	data = []
# 	column_name = ('Line_no', 'Type', 'Thread_ID', 'Direction', 'BB_ID', 'Method', 'Args', 'Function')
# 	for row in cursor.fetchall():
# 		temp = dict(zip(column_name, row))
# 		if(temp['Direction']):
# 			data.append(dict(zip(column_name, row)))
# 	cursor.close()
# 	conn.close()
# 	return data

def get_particular_selected(method, thread):
	conn = get_connection(db_config)
	cursor = conn.cursor()
	cursor.execute("""UPDATE log SET Function = '0' """)
	cursor.close()
	conn.close()
	conn = get_connection(db_config)
	cursor = conn.cursor()

	query = """UPDATE log SET function = '1' WHERE method = '{l1}';"""
	cursor.execute(query.format(l1 = method))
	
	q2 = """SELECT * FROM log WHERE thread_id='{l3}' ORDER BY line_no"""
	cursor.execute(q2.format(l3 = thread))
	data = []
	column_name = ('Line_no', 'Type', 'Thread_ID', 'Direction', 'BB_ID', 'Method', 'Args', 'Function')
	for row in cursor.fetchall():
		data.append(dict(zip(column_name, row)))
	cursor.close()
	conn.close()
	return data

# OLD VERSION
# def getline(line):
# 	conn = get_connection(db_config)
# 	cursor = conn.cursor()
# 	q = """SELECT * FROM log WHERE method = '{}';"""
# 	cursor.execute(q.format(line))
# 	data = []
# 	column_name = ('Line_no', 'Type', 'Thread_ID', 'Direction', 'BB_ID', 'Method', 'Args', 'Function')
# 	for row in cursor.fetchall():
# 		temp = dict(zip(column_name, row))
# 		if(temp['Direction']):
# 			data.append(dict(zip(column_name, row)))
# 	cursor.close()
# 	conn.close()
# 	return data

def getline(line):
	conn = get_connection(db_config)
	cursor = conn.cursor()
	q1 = """SELECT thread_id FROM log WHERE method = '{l2}' LIMIT 1;"""
	cursor.execute(q1.format(l2 = line))
	tt = []
	col_name = ('Thread_ID')
	for row in cursor.fetchall():
		temp1 = dict(zip(col_name, row))
		tt.append(dict(zip(col_name, row)))
	thett = tt[0]
	q = """SELECT * FROM log WHERE method = '{l1}' AND thread_id = '{l2}';"""
	cursor.execute(q.format(l1=line, l2=thett['T']))
	data = []
	column_name = ('Line_no', 'Type', 'Thread_ID', 'Direction', 'BB_ID', 'Method', 'Args', 'Function')
	for row in cursor.fetchall():
		temp = dict(zip(column_name, row))
		if(temp['Direction']):
			data.append(dict(zip(column_name, row)))
	cursor.close()
	conn.close()
	return data

def get_thread(method):
	conn = get_connection(db_config)
	cursor = conn.cursor()
	q1 = """SELECT thread_id FROM log WHERE method = '{l2}' LIMIT 1;"""
	cursor.execute(q1.format(l2 = method))
	tt = []
	col_name = ('Thread_ID')
	for row in cursor.fetchall():
		temp1 = dict(zip(col_name, row))
		tt.append(dict(zip(col_name, row)))
	thett = tt[0]
	print("thread")
	print(thett)
	return thett['T']

def get_all_methods():
	conn = get_connection(db_config)
	cursor = conn.cursor()
	q = """SELECT DISTINCT method FROM log WHERE type='API' AND method NOT LIKE '%init%' AND method NOT LIKE '[L%' ORDER BY method;"""
	cursor.execute(q)
	data = []
	column_name = ('Method')
	for row in cursor.fetchall():
		data.append(row)
		# temp = dict(zip(column_name, row))
		# if(temp['Direction']):
		# 	data.append(dict(zip(column_name, row)))
	cursor.close()
	conn.close()
	return data