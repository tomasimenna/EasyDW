import pyodbc, datetime

def drop_sql_table(conn_str, schema, table, database):

    def write_sql_statement(table):

        statement = f'''
        DROP TABLE IF EXISTS {schema}.{table}
        '''

        return statement

    def run_sql_statement(statement):
        conn = pyodbc.connect(conn_str, autocommit=True)
        cursor = conn.cursor()
        cursor.execute(statement)
        conn.close()

    sql_statement = write_sql_statement(table = table)
    run_sql_statement(statement = sql_statement)
    message = f'''{str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f'))}: Table "{table}" dropped from the schema "{schema}", database "{database}"'''
    print(message)