import os
import psycopg2
import config

def get_all_common_security_methods():
	security_file = "android_calls_private_calls.txt"
	only_calls = []
	from_log = []
	common = []
	line_no = []

	def get_data():
		f = open(security_file)
		i = 1
		for line in f:
		    temp = line.split()
		    val = temp[0].split('(')
		    only_calls.append((i, val[0]))
		    i += 1
		return only_calls
	# def get_data():
	# 	f = open(security_file)
	# 	i = 1
	# 	for line in f:
	# 	    temp = line.split()
	# 	    val = temp[0].split('(')
	# 	    only_calls.append((val[0]+'('))
	# 	    i += 1
	# 	return only_calls

	def get_connection(config) :
	    conn = psycopg2.connect(**config)
	    return conn

	def insert_into_table(values):
		# Insert into table
		insert_many_tuple_placeholder = """INSERT INTO securitycalls VALUES(%s)"""

	def insert_into_db(only_calls):
		query = "INSERT INTO securitycalls(Line_no, Call) " \
	            "VALUES(%s,%s)"

		db_config = config.config()
		conn = get_connection(db_config)
		cursor = conn.cursor()
		cursor.execute("""DELETE FROM securitycalls;""")
		# Create securitycalls table
		cursor.execute("""CREATE TABLE IF NOT EXISTS securitycalls(Line_no integer PRIMARY KEY, Call varchar(500) NOT NULL);""")

		cursor.executemany(query, only_calls)
		cursor.close()
		conn.commit()
		conn.close()

	# def get_from_log():
	# 	db_config = config.config()
	# 	conn = get_connection(db_config)
	# 	cursor = conn.cursor()
	# 	cursor.execute("""SELECT line_no, method FROM log;""")
	# 	columns = ('Line_no', 'Method')
	# 	rcount = int(cursor.rowcount)
	# 	print(rcount)
	# 	for r in range(rcount):
	# 		row = cursor.fetchone()
	# 		temp = (row[0], row[1]+'(')
	# 		temp = (row[1]+'(')
	# 		from_log.append(temp)

	# 	cursor.close()
	# 	conn.close()
	# 	return from_log

	# def compare():
	# 	return set(only_calls).intersection(from_log)

	full_lines = []
	only_methods = []
	def get_common_from_db():
		db_config = config.config()
		conn = get_connection(db_config)
		cursor = conn.cursor()

		cursor.execute("""SELECT method FROM log INTERSECT SELECT call FROM securitycalls;""")
		for row in cursor.fetchall():
			only_methods.append(row[0])

		cursor.execute("""SELECT log.* FROM log INNER JOIN securitycalls ON log.method=securitycalls.call;""")
		column_name = ('Line_no', 'Type', 'Thread_ID', 'Direction', 'BB_ID', 'Method', 'Args', 'Function')
		for row in cursor.fetchall():
			temp = dict(zip(column_name, row))
			if(temp['Direction']):
				full_lines.append(dict(zip(column_name, row)))	

		cursor.close()
		conn.close()

		return full_lines, only_methods


	def get_counts(methods):
		counts = []
		print(methods)
		db_config = config.config()
		conn = get_connection(db_config)
		cursor = conn.cursor()
		query = """SELECT COUNT(*) FROM log WHERE Method = '{m1}' AND Direction = '>';"""
		for i in range(0, len(methods)):
			cursor.execute(query.format(m1 = methods[i]))
			counts.append(cursor.fetchall())
			# column_name = ('Count')
			# for row in cursor.fetchall():
			# 	temp = dict(zip(column_name, row))
			# 	if(temp['Direction']):
			# 		counts.append(dict(zip(column_name, row)))	

		cursor.close()
		conn.close()
		return counts



	only_calls = get_data()
	insert_into_db(only_calls)

	full_lines, only_methods = get_common_from_db()
	counts = get_counts(only_methods)
	return full_lines, only_methods, counts