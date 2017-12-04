import os
from datetime import datetime
import sys
import pymysql.cursors
import shutil

def sqlQuery(sql):
	connection = pymysql.connect(host='127.0.0.1', user='root', password='Snappy123', db='filewatch', charset= 'utf8mb4', cursorclass=pymysql.cursors.DictCursor)
	rows = []
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			for row in cursor:
				rows.append(row)
	finally:
		connection.close()
	return rows

def sqlExecute(sql):
	connection = pymysql.connect(host='127.0.0.1', user='root', password='Snappy123', db='filewatch', charset= 'utf8mb4', cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			connection.commit()
	finally:
		connection.close()
	
def getCurrentDate():
	return str(datetime.now().date().year) + '-' + str(datetime.now().date().month) + "-" + str(datetime.now().date().day)

def deleteItem(path):
	try:
		if os.path.isfile(path):
			os.unlink(path)
		else:
			shutil.rmtree(path)
	except Exception as e:
		print(e)

if len(sys.argv) == 4: 
	if sys.argv[1] == 'add':
		sqlExecute("insert into file values(0, '" + os.path.expanduser('~') + sys.argv[2] + "', '" + sys.argv[3] + "')")
		print('I will delete', os.path.expanduser('~') + sys.argv[2], 'on', sys.argv[3])
	elif sys.argv[1] == 'addr':
		sqlExecute("insert into file values(0, '" + os.getcwd() + sys.argv[2] + "', '" + sys.argv[3] + "')")
		print('I will delete', os.getcwd() + sys.argv[2], 'on', sys.argv[3])

elif len(sys.argv) == 3:
	if sys.argv[1] == 'ignore':
		sqlExecute("delete from file where path = '" + os.path.expanduser('~') + sys.argv[2] + "'")
		print('I will not delete', os.path.expanduser('~') + sys.argv[2])
	elif sys.argv[1] == 'ignorer':
		sqlExecute("delete from file where path = '" + os.getcwd() + sys.argv[2] + "'")
		print('I will not delete', os.getcwd() + sys.argv[2])
	elif sys.argv[1] == 'addclean':
		sqlExecute("insert into clean values(0, '" + os.path.expanduser('~') + sys.argv[2] + "')")
		print('I will now start cleaning', os.path.expanduser('~') + sys.argv[2])
	elif sys.argv[1] == 'addcleanr':
		sqlExecute("insert into clean values(0, '" + os.getcwd() + sys.argv[2] + "')")
		print('I will now start cleaning', os.getcwd() + sys.argv[2])
elif len(sys.argv) == 2:
	if sys.argv[1] == 'print':
		rows = sqlQuery("select * from file order by removeDate")
		for row in rows:
			print(row['path'], row['removeDate'])
	elif sys.argv[1] == 'clear':
		sqlExecute("delete from file;")
		print('I cleared the deletion table')
	elif sys.argv[1] == 'clean':	
		rows = sqlQuery("select * from clean")
		for row in rows:
			folder = row['path']
			print(folder)
			for the_file in os.listdir(folder):
				file_path = os.path.join(folder, the_file)
				deleteItem(file_path)
	elif sys.argv[1] == 'printclean':
		rows = sqlQuery("select * from clean")
		for row in rows:
			print(row['path'])
	elif sys.argv[1] == 'clearclean':
		sqlExecute("delete from clean;")
		print("I cleared the clean table")
	elif sys.argv[1] == 'help':
		print('TASK\t\t\tCOMMAND')
		print('Run sched. deletions\twatch')
		print('Schedule a deletion\twatch add [path from home] [remove date]')
		print('Schedule a deletion\twatch addr [path from cwd] [remove date]')
		print('Ignore a deletion\twatch ignore [path from home]')
		print('Ignore a deletion\twatch ignorer [path from cwd]')
		print('Watch for cleaning\twatch addclean [path from home]')
		print('Watch for cleaning\twatch addcleanr [path from cwd]')
		print('Print sched. deletions\twatch print')
		print('Clear sched. deletions\twatch clear')
		print('Clean spec. dirs\twatch clean')
		print('Print clean dirs\twatch printclean')
		print('Clear clean dirs\twatch clearclean')
		print('Display help menu\twatch help')		
else:
	rows = sqlQuery("select * from file where removeDate <= '" + getCurrentDate() + "';")
	for row in rows:
		deleteItem(row['path'])
		print('I deleted', row['path'])
	sqlExecute("delete from file where removeDate <= '" + getCurrentDate() + "';")
