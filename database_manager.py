import pyodbc, datetime, sys

class Database:

    def __init__(self, conn_str, database):
        self.conn_str = conn_str
        self.database = database

    def create_sql_database(self):

        conn = pyodbc.connect(self.conn_str, autocommit=True)
        cursor = conn.cursor()

        db_creation_str = f'''
        IF NOT EXISTS(SELECT * FROM sys.databases WHERE name = '{self.database}')
        CREATE DATABASE {self.database};
        '''

        cursor.execute(db_creation_str)
        message = f'''{str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f'))}: Database {self.database} created. [IF IT WAS NOT ALREADY]'''
        print(message)

        conn.close()

    def get_active_connetions(self):
        active_connections = {}
        conn = pyodbc.connect(self.conn_str, autocommit=True)
        cursor = conn.cursor()

        check_conn_str = 'sp_who2'
        count = 0
        cursor.execute(check_conn_str)
        for row in cursor.fetchall():
            if str(row[5]) == str(self.database):
                count += 1
                active_connections[count] = {'SPID': row[0]
                                            , 'Status': row[1]
                                            , 'Login': row[2]
                                            , 'HostName': row[3]
                                            , 'DBName': row[5]
                                            , 'Command': row[6]
                                            , 'CPUTime': row[7]
                                            , 'ProgramName': row[10]
                                            }
        conn.close()

        return active_connections

    def kill_connections(self, active_connections):
        if active_connections != {}:
            conn = pyodbc.connect(self.conn_str, autocommit=True)
            cursor = conn.cursor()
            for connection in active_connections:
                statement = f'''
                KILL {str(active_connections[connection]['SPID'])}
                '''
                
                cursor.execute(statement)
            conn.close()
        else:
            pass

    def drop_database(self):

        conn = pyodbc.connect(self.conn_str, autocommit=True)
        cursor = conn.cursor()

        db_drop_str = f'''
        DROP DATABASE {self.database}
        '''

        try:
            cursor.execute(db_drop_str)
            message = f'''{str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f'))}: Database {self.database} deleted.'''
            print(message)

        except:
            message = f'''{str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f'))}: Deletion of database {self.database} failed. [Maybe DB does not exists]'''
            print(message, file= sys.stderr)

        conn.close()

    def create_schema(self, name):

        conn = pyodbc.connect(self.conn_str, autocommit=True)
        cursor = conn.cursor()

        schema_creation_str = f'''
        IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = '{name}' )
        EXEC('CREATE SCHEMA {name}')
        '''
        cursor.execute(schema_creation_str)
        conn.close()

        message = f'''Schema "{name}" created in database "{self.database}"'''
        print(message)

    def drop_schema(self, name):
        conn = pyodbc.connect(self.conn_str, autocommit=True)
        cursor = conn.cursor()
        schema_drop_str = f'''
        IF EXISTS (SELECT * FROM sys.schemas WHERE name = '{name}' )
        DECLARE @sql NVARCHAR(max)

        SELECT @sql = stuff((
                    SELECT ', ' + quotename(table_schema) + '.' + quotename(table_name)
                    FROM INFORMATION_SCHEMA.Tables
                    WHERE table_schema = '{name}'
        AND TABLE_TYPE = 'BASE TABLE'
                    ORDER BY table_name
                    FOR XML path('')
                    ), 1, 2, '')

        SET @sql = 'DROP TABLE ' + @sql

        PRINT(@SQL)
        EXEC (@SQL);
        EXEC ('DROP SCHEMA {name}')
        '''
        cursor.execute(schema_drop_str)
        conn.close()

        message = f'''Schema "{name}" dropped from the database "{self.database}"'''
        print(message)