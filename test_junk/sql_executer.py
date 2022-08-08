import mysql.connector
from package import variables as v


ort = "home"
database = "Main"

mydb = mysql.connector.connect(
    host=v.host(ort),
    user=v.user(ort),
    passwd=v.passwd(ort),
    database=v.database(database),
    auth_plugin='mysql_native_password')

my_cursor = mydb.cursor()
my_cursor.execute(f"Delete FROM `Main`.`Park` WHERE (`Frei` = '-1');")
zug = my_cursor.fetchone()
my_cursor.close()