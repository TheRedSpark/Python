import datetime
from datetime import date

import dvb
import mysql.connector  # 8.0.28
from package import variables as v
import time
from datetime import timedelta

stop = 'Helmholzstraße'
time_offset = 20  # how many minutes in the future, 0 for now
num_results = 1
city = 'Dresden'
ort = "home"
database = "Selma"


def setter(stop, line, direction, arrival):
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    time_sql = time.strftime("%Y-%m-%d %H:%M:%S")
    sql_maske = "INSERT INTO `DVB`.`Arrival` (`Stop`,`Line`,`Direction`,`Arrival`) VALUES (%s, %s, %s, %s); "
    data_n = (stop, line, direction, arrival)
    my_cursor.execute(sql_maske, data_n)
    mydb.commit()
    mydb.close()


results = dvb.monitor(stop, time_offset, num_results, city, raw=True)
print(results)
print(len(results))
time_sql = date.today()
print(time_sql.strftime("%Y-%m-%d %H:%M:%S"))
time_sql = time_sql.strftime("%H:%M:%S %d.%m.%Y")
print(time_sql)
print(datetime.datetime)
#d1 = timedelta(hours=20, minutes=50)
#time_sql = time_sql + d1
print(time_sql)
for stops in results:
    print(stops[0])
    print(type(int(stops[0])))
    print(stops[1])
    print(type(stops[1]))
    print(int(stops[2]))
    print(type(int(stops[2])))
