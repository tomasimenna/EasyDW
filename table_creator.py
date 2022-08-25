import pyodbc, datetime, sys
from csv_analyzer import csvFile

def create_sql_table(csv_path, conn_str, schema, table, database):

    csv_file = csvFile(csv_path = csv_path)
    is_error = False

    def read_tables_to_increase(conn_str, database):
        conn_str = conn_str.replace(f'Database={database};', 'Database=basic_settings;')
        incr_list = []
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        d = cursor.execute(F'''SELECT table_name FROM dbo.increasing_tables''')
        for data in d:
            incr_list.append(data[0])

        return incr_list

    def write_sql_statement(data, schema, table, csv_path, database, conn_str):
        select_var = [f'''{str(key)} {data[key][0]} ({data[key][1]})''' for key in data]
        select_var = ', '.join([str(item) for item in select_var]).replace('(None)', '')

        if table in read_tables_to_increase(conn_str = conn_str, database = database):
            statement = f'''
            IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'{schema}.{table}') AND type in (N'U'))
            CREATE TABLE {schema}.{table} ({select_var});
            BULK INSERT {schema}.{table}
            FROM '{csv_path}'
            WITH (FIELDTERMINATOR = ',' ,ROWTERMINATOR = '\\n', FIRSTROW = 2, KEEPNULLS)
            '''
            action = 'increase'

        else:
            statement = f'''
            DROP TABLE IF EXISTS {schema}.{table}; CREATE TABLE {schema}.{table} ({select_var});
            BULK INSERT {schema}.{table}
            FROM '{csv_path}'
            WITH (FIELDTERMINATOR = ',' ,ROWTERMINATOR = '\\n', FIRSTROW = 2, KEEPNULLS)
            '''
            action = 'replace'

        return [statement, action]

    def run_sql_statement(statement):
        conn = pyodbc.connect(conn_str, autocommit=True)
        cursor = conn.cursor()
        try:
            cursor.execute(statement)
        except Exception as e:
            global is_error
            is_error = True
            message = f'''{str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f'))}: {e}'''
            print(message, file = sys.stderr)
        conn.close()

    sql_statement = write_sql_statement(data = csv_file.structure, schema = schema, table = table, csv_path = csv_path, database = database, conn_str = conn_str)
    run_sql_statement(statement = sql_statement[0])
    action = sql_statement[1]
    if is_error == False and action == 'replace':
        message = f'''{str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f'))}: Table "{table}" created in schema "{schema}", database "{database}"'''
    elif is_error == False and action == 'increase':
        message = f'''{str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f'))}: Table "{table}" appended in schema "{schema}", database "{database}"'''
    else:
        message = f'''{str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f'))}: There was an error when trying to create the table {table} in the schema {schema}, database {database}'''
    print(message)