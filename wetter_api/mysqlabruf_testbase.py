import mysql.connector # V8.0.28


mydb = mysql.connector.connect(
    host="host",
    user="user",
    passwd="Passwort",
    database="Database",
    auth_plugin='mysql_native_password')

my_cursor = mydb.cursor()
my_cursor.execute("SELECT Windgeschwindigkeit from {Deine Tabelle} Order by Windgeschwindigkeit DESC LIMIT 20")
result = my_cursor.fetchall()
my_cursor.close()
for data in result:
    print (result)
