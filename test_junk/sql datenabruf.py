import mysql.connector
from package import zugang as anbin

ort = "home"
database = "numbeo"

mydb = mysql.connector.connect(
    host=anbin.host(ort),
    user=anbin.user(ort),
    passwd=anbin.passwd(ort),
    database=anbin.database(database),
    auth_plugin='mysql_native_password')

my_cursor = mydb.cursor()
my_cursor.execute("SELECT Zeit FROM numbeo.dresden order by Zeit desc limit 1")
inhalt = my_cursor.fetchall()
my_cursor.close()
print(inhalt[0])
print(type(inhalt[0]))
timeserver = str(inhalt[0]).replace("datetime.datetime(","").replace("),)","").replace("(","").replace(", ","-").split("-")
print(timeserver[2])