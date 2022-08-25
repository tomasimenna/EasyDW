import pyodbc

def create_settings_db(server_to_connect):
    conn_str = 'Driver={ODBC Driver 17 for SQL Server};' f'Server={server_to_connect};' f'Database=master;' 'Trusted_Connection=yes;' 'ColumnEncryption=Enabled'
    conn = pyodbc.connect(conn_str, autocommit=True)
    cursor = conn.cursor()

    statement = f'''
    DECLARE @dbname nvarchar(128)
    SET @dbname = N'basic_settings'

    IF NOT EXISTS (SELECT * 
    FROM sys.databases 
    WHERE (name = @dbname))

    CREATE DATABASE basic_settings;

    IF NOT EXISTS (SELECT * 
    FROM basic_settings.sys.tables 
    WHERE (name = 'increasing_tables'))

    EXEC('CREATE TABLE basic_settings.dbo.increasing_tables (table_name VARCHAR(255))')
    '''

    cursor.execute(statement)
    conn.close()