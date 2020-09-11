import pyodbc


def connectToSQLServer():
    servername = 'IN-00232335'
    userid = 'sa1'
    password1 = 'Suggi@218'
    databasename = 'Suggi'
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};Server=' + servername + ';UID=' + userid + ';PWD=' + password1 + ';Database=' + databasename)
    return conn
