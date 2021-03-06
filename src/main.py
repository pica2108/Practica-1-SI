import altair as alt
import numpy as np
import pandas as pd
from src.SQLite import connectBD, insertTable, queryOne, queryAll, sql_remove_all_tables, close_connection
from src.legal import parseLegalJson
from src.users import parseUsersInfo, parseUsersDatesIps
import matplotlib.pyplot as plt

# LECTURA DE LOS JSON Y CREACION DE TABLAS

con = connectBD()
sql_remove_all_tables(con)

legal_table = parseLegalJson()
insertTable(con, legal_table, "legal")

users_table_info = parseUsersInfo()
users_table_ips_dates = parseUsersDatesIps()

insertTable(con, users_table_info, "users_info")
insertTable(con, users_table_ips_dates, "users_ips_dates")

print("EJERCICIO 2.MUESTRAS")

telefonos = queryOne(con, "SELECT COUNT(telefono) FROM users_info WHERE telefono!='None'")
contrasena = queryOne(con, "SELECT COUNT(contrasena) FROM users_info WHERE contrasena!='None'")
provincia = queryOne(con, "SELECT COUNT(provincia) FROM users_info WHERE provincia!='None'")
permisos = queryOne(con, "SELECT COUNT(permisos) FROM users_info WHERE permisos!='None'")
emailsTotal = queryOne(con, "SELECT COUNT(emailsTotal) FROM users_info WHERE emailsTotal!='None'")
emailsPhishing = queryOne(con, "SELECT COUNT(emailsPhishing) FROM users_info WHERE emailsPhishing!='None'")
emailsCliclados = queryOne(con, "SELECT COUNT(emailsCliclados) FROM users_info WHERE emailsCliclados!='None'")
fechas = queryOne(con, "SELECT COUNT(DISTINCT username) FROM users_ips_dates WHERE dates != 'None'")
ips = queryOne(con, "SELECT COUNT(DISTINCT username) FROM users_ips_dates WHERE ips!='None'")

aux = {
    "telefonos": telefonos,
    "provincia": provincia,
    "contrasena": contrasena,
    "permisos": permisos,
    "emailTotal": emailsTotal,
    "emailsPhishing": emailsPhishing,
    "emailsCliclados": emailsCliclados,
    'fechas': fechas,
    'ips': ips
}
df_aux = pd.DataFrame(aux)
print("EJERCICIO 2 ")
print("NUMERO DE MUESTRAS (Por clave):")
print(df_aux)
print("NUMERO DE MUESTRAS (Por usuario completo):")
non_missing_users = queryOne(con, "SELECT COUNT(*) FROM users_info WHERE isMissing=0")
print(non_missing_users)

print("EJERCICIO 2.MEDIA Y DS DE LAS FECHAS")

numFechas = queryAll(con, "SELECT username, COUNT(dates) FROM users_ips_dates WHERE isMissing=0 GROUP BY username")
df_numFechas = pd.DataFrame(numFechas, columns=['username', 'numDates'])
print("Media: ")
print(df_numFechas['numDates'].mean())
print("Desviaci??n Estandar:")
print(df_numFechas['numDates'].std())

print("EJERCICIO 2.MEDIA Y DS DE LAS IPS")

numIps = queryAll(con, "SELECT username, COUNT(ips) FROM users_ips_dates WHERE isMissing=0 GROUP BY username")
df_numIps = pd.DataFrame(numIps, columns=['username', 'numIps'])
print("Media: ")
print(df_numIps['numIps'].mean())
print("Desvici??n Estandar: ")
print(df_numIps['numIps'].std())

print("EJERCICIO 2.MEDIA Y DS DE LOS EMAILS TOTALES")

numEmailsTotal = queryAll(con, "SELECT emailsTotal FROM users_info WHERE isMissing=0")
df_numEmailsTotal=pd.DataFrame(numEmailsTotal, columns=['numEmails'])
print("Media: ")
print(df_numEmailsTotal['numEmails'].mean())
print("Desvici??n Estandar: ")
print(df_numEmailsTotal['numEmails'].std())


print("EJERCICIO 2.VALORES MAXIMOS Y MINIMOS DEL TOTAL DE FECHAS")

numDates = queryAll(con, "SELECT username, COUNT(dates) FROM users_ips_dates WHERE isMissing=0 GROUP BY username")
df_numDates = pd.DataFrame(numDates, columns=['username', 'dates'])
print("Fechas m??nimos")
print(df_numDates['dates'].min())
print("Fechas m??ximos")
print(df_numDates['dates'].max())

print("EJERCICIO 2.VALORES MAXIMOS Y MINIMOS DEL NUMERO DE EMAILS RECIBIDOS")

emails_recibidos = queryAll(con, "SELECT emailsTotal FROM users_info WHERE isMissing=0")
df_emails_recibidos = pd.DataFrame(emails_recibidos, columns=['emails'])
print("Correos m??nimos")
print(df_emails_recibidos['emails'].min())
print("Correos m??ximos")
print(df_emails_recibidos['emails'].max())

print("EJERCICIO 3")

def groupByEmailNumber(emails):
    df_emails = pd.DataFrame(emails, columns=['emailsPhishing', 'emails'])
    bins = [0,199,np.inf]
    labels = ['menos de 200', 'mas de 200']
    cut = pd.cut(df_emails['emails'], bins=bins, labels=labels)
    return df_emails.groupby(cut)['emailsPhishing']

emails_permiso_usuario = queryAll(con, "SELECT emailsPhishing, emailsTotal FROM users_info WHERE permisos=0")
emails_permiso_admin = queryAll(con, "SELECT emailsPhishing, emailsTotal FROM users_info WHERE permisos=1")

print("Numero de observaciones usuarios: ")
print(groupByEmailNumber(emails_permiso_usuario).count())
print("Numero de observaciones administradores: ")
print(groupByEmailNumber(emails_permiso_admin).count())

emails_permiso_usuario_missing = queryAll(con, "SELECT emailsPhishing, emailsTotal FROM users_info WHERE permisos=0 AND emailsPhishing = -1")
emails_permiso_admin_missing = queryAll(con, "SELECT emailsPhishing, emailsTotal FROM users_info WHERE permisos=1 AND emailsPhishing = -1")

print("Numero de valores ausentes (missing) usuarios: ")
print(groupByEmailNumber(emails_permiso_usuario_missing).count())
print("Numero de valores ausentes (missing) administradores: ")
print(groupByEmailNumber(emails_permiso_admin_missing).count())

emails_permiso_usuario_non_missing = queryAll(con, "SELECT emailsPhishing, emailsTotal FROM users_info WHERE permisos=0 AND emailsPhishing != -1")
emails_permiso_admin_non_missing = queryAll(con, "SELECT emailsPhishing, emailsTotal FROM users_info WHERE permisos=1 AND emailsPhishing != -1")

group_usuarios = groupByEmailNumber(emails_permiso_usuario_non_missing)
group_admins = groupByEmailNumber(emails_permiso_admin_non_missing)
print("Mediana usuarios: ")
print(group_usuarios.median())
print("Mediana administradores: ")
print(group_admins.median())

print("Media usuarios: ")
print(group_usuarios.mean())
print("Media administradores: ")
print(group_admins.mean())

print("Varianza usuarios: ")
print(group_usuarios.var())
print("Varianza administradores: ")
print(group_admins.var())

print("Max usuarios: ")
print(group_usuarios.max())
print("Max administradores: ")
print(group_admins.max())
print("Min usuarios: ")
print(group_usuarios.min())
print("Min administradores: ")
print(group_admins.min())


print("EJERCICIO 4")
users_criticos = queryAll(con, "SELECT emailsPhishing, emailsCliclados, username FROM users_info WHERE emailsPhishing > 0")
df_users_criticos = pd.DataFrame(users_criticos, columns=['emailsPhishing', 'emailsCliclados', 'username'])
df_users_criticos['criticidad'] = df_users_criticos['emailsCliclados']/df_users_criticos['emailsPhishing']
df_users_criticos = df_users_criticos.sort_values(by=['criticidad'], ascending=False, ignore_index=True).loc[:9]
#df_users_criticos.plot(kind='bar', x='username', y='criticidad')

webs_politicas = queryAll(con, "SELECT cookies, aviso, proteccion_de_datos, web FROM legal")
df_webs_politicas = pd.DataFrame(webs_politicas, columns=['cookies', 'aviso', 'proteccion_de_datos', 'web'])
df_webs_politicas = df_webs_politicas.sort_values(by=['cookies', 'aviso', 'proteccion_de_datos'], ignore_index=True).loc[:4]
#df_webs_politicas.plot(kind='bar', x='web')

webs_politica_anio = queryAll(con, "SELECT cookies, aviso, proteccion_de_datos, web, creacion FROM legal")
df_webs_politica_anio = pd.DataFrame(webs_politica_anio, columns=['cookies', 'aviso', 'proteccion_de_datos', 'web', 'creacion'])
df_webs_politica_anio['cumple'] = df_webs_politica_anio['cookies'] * df_webs_politica_anio['aviso'] * df_webs_politica_anio['proteccion_de_datos']

cumplen = df_webs_politica_anio.loc[df_webs_politica_anio['cumple'] == 1].groupby(['creacion'])['web'].count()
no_cumplen = df_webs_politica_anio.loc[df_webs_politica_anio['cumple'] == 0].groupby(['creacion'])['web'].count()

ax = plt.gca()
cumplen.plot(kind='line',x='creacion', y='cumple')
no_cumplen.plot(kind='line',x='creacion',y='cumple', color='red')


plt.show()

close_connection(con)