import os
from table_creator import create_sql_table
from table_dropper import drop_sql_table
from database_manager import Database

class DatabaseManager:

    def __init__(self, event, task, server_to_connect, hasschema = False):
        self.mpath = event.src_path
        self.hasschema = hasschema
        
        if task == 'create table' or task == 'drop table':   #make the difference if the file is in schema or is not
            self.filname = os.path.splitext(os.path.basename(self.mpath))[0]
            self.filext = os.path.splitext(os.path.basename(self.mpath))[1]
            if self.hasschema == 'dbo':
                self.folname = os.path.basename(os.path.dirname(self.mpath))
                self.conn_level = self.folname
            else:
                self.folname = os.path.basename(os.path.dirname(os.path.dirname(self.mpath)))
                self.conn_level = self.folname

        elif task == 'create schema' or task == 'drop schema':
            self.schema_name = os.path.basename(self.mpath)
            self.folname = os.path.basename(os.path.dirname(self.mpath))
            self.conn_level = self.folname

        elif task == 'create database' or task == 'drop database':
            self.folname = os.path.splitext(os.path.basename(self.mpath))[0]
            self.conn_level = 'master'

        self.conn_str = 'Driver={ODBC Driver 17 for SQL Server};' f'Server={server_to_connect};' f'Database={self.conn_level};' 'Trusted_Connection=yes;' 'ColumnEncryption=Enabled'

    def create_table(self):
        table = ''.join(e for e in self.filname if e.isalnum())
        create_sql_table(csv_path = self.mpath, conn_str = self.conn_str, schema = self.hasschema, table = table, database = self.conn_level)

    def drop_table(self):
        table = ''.join(e for e in self.filname if e.isalnum())
        drop_sql_table(conn_str = self.conn_str, schema = self.hasschema, table = table, database = self.conn_level)

    def create_database(self):
        db = Database(conn_str = self.conn_str, database = self.folname)
        db.create_sql_database()

    def drop_database(self):
        db = Database(conn_str = self.conn_str, database = self.folname)
        active_connections = db.get_active_connetions()
        db.kill_connections(active_connections = active_connections)
        db.drop_database()

    def append_to_table(self):
        pass

    def create_schema(self):
        db = Database(conn_str = self.conn_str, database = self.folname)
        db.create_schema(name = self.schema_name)

    def drop_schema(self):
        db = Database(conn_str = self.conn_str, database = self.folname)
        db.drop_schema(name = self.schema_name)

