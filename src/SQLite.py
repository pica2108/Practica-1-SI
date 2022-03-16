import sqlite3


def connectBD():
    con = sqlite3.connect('./bbdd/auditoria.db')
    return con

def insertTable(con,table,tableName):
    table.to_sql(tableName, con, index=False)  # se crea la tabla en la bd y se anade la var tabla, y se quita el indice

