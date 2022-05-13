import mysql.connector # V8.0.28
import time # bereits implementiert

from SQL_Daten import zugang as anbin
ort = 'lap'
database = 'numbeo'
mydb = mysql.connector.connect(
        host=anbin.host(ort),
        user=anbin.user(ort),
        passwd=anbin.passwd(ort),
        database=anbin.database(database),
        auth_plugin='mysql_native_password')

my_cursor = mydb.cursor()

time = time.strftime("%Y-%m-%d %H:%M:%S")
time2 = None
print(time)
#dresden = '`numbeo`.`dresden`'
bank = 'numbeo'
table = 'dresden'
print(table)

#sqlStuff = "INSERT INTO `numbeo`.`dresden` (`time`) VALUES (%s); "
#sqlStuff = "INSERT INTO (%s.%s) (`time`,`satum`) VALUES (%s, %s); "
sqlStuff = "INSERT INTO `numbeo`.`dresden` (`Zeit`,`Snack`) VALUES (%s, %s);"
record1 = (time, time2)
#record1 = (bank.replace("'",""), table.replace("'",""), time2, time)
my_cursor.execute(sqlStuff,record1)
mydb.commit()
print("Erfolg")

