#Connect With mmsql database from this python3 script


import pyodbc
import os 

banner = '''
\u001b[34m==============================================================================
 __  __ ____ ____	___  _	   
|  \/  / ___/ ___| / _ \| |    
| |\/| \___ \___ \| | | | |    
| |  | |___) |__) | |_| | |___ 
|_|  |_|____/____/ \__\_\_____|
							   
  ____ ___	_	_ _   _ _____ ____ _____ ___  ____	
 / ___/ _ \| \ | | \ | | ____/ ___|_   _/ _ \|	_ \
| |  | | | |  \| |	\| |  _|| |		| || | | | |_) |
| |__| |_| | |\  | |\  | |__| |___	| || |_| |	_ < 
 \____\___/|_| \_|_| \_|_____\____| |_| \___/|_| \_\
													
version : 1.0
==============================================================================
'''

def print_help():
	print("-for Bash Command type !the_command example : !whoami" )
	print("-quit with quit ")
	print("-clear screen with clear")
	print("-help with help")

def connect_to_db(connection_string):
	try :
		cnx = pyodbc.connect(connection_string);
	except Exception as e:
		print (e, e.args)
		return
	return cnx

def command(conx ,query):
	cursor = conx.cursor();
	try:
		cursor.execute(query);
		data = cursor.fetchall()
		return data
	except Exception as e:
		if(e):
			conx.commit()
			print("done !")
		return
	
	
def print_table_loop(list_of_tuples):

	if(not list_of_tuples) :
		print("Output nothing")
		return
	for i in list_of_tuples:
		print(i)
	

def main():
	os.system('clear')
	print(banner)
	print_help()
	
	#server info for data base connection 
	server =   #server 
	database = #database name
	username = #username
	password = #password 
	con_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password
	print(con_string)
	cnx = connect_to_db(con_string)
	#program loop 
	while(1):
		#print(, end="")
		bash = " >>> "

		print('\u001b[32m'+database ,'\033[92m'+bash, end = "")
		
		commands = str(input('\033[96m'))
		if(commands == 'quit') :
			cnx.close()
			exit(0)
		elif (commands == 'banner'):
			print(banner)
		elif (commands =='clear') :
			os.system('clear');
		elif (commands == ''):
			pass
		elif (commands[0] == '!'):
			try:		
				os.system(commands[1:])
			except Exception as e :
				print(e)
		elif (commands == "help"):
			print_help()
		else :
			print_table_loop(command(cnx , commands))


if __name__ == '__main__':
	main();
