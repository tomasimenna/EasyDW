from action_compiler import DatabaseManager
import datetime

def dbm_handler(event, task, server_to_connect, hasschema = False):
    dbm = DatabaseManager(event = event, task = task, server_to_connect = server_to_connect, hasschema = hasschema)

    if task == 'create table':
        print(f'''{str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f'))}: Creating table {dbm.filname}''')
        dbm.create_table()
    elif task == 'append to table':
        dbm.append_to_table()
    elif task == 'drop table':
        dbm.drop_table()
    elif task == 'create database':
        dbm.create_database()
    elif task == 'drop database':
        dbm.drop_database()
    elif task == 'create schema':
        dbm.create_schema()
    elif task == 'drop schema':
        dbm.drop_schema()
    else:
        pass

    
