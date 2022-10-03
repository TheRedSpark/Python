import requests
from package import variables as v
import json
import mysql.connector
import time
from pyinstrument import Profiler

profiler = Profiler()
profiler.start()
res = requests.get(
    'https://creativecommons.tankerkoenig.de/json/list.php?lat=52.521&lng=13.438&rad=25&sort=dist&type=all&apikey=' + v.tanke_api)
data = json.loads(res.content.decode())
ort = "home"
database = "Tankdaten"
list = []


def data_uploader(datalist):
    with mysql.connector.connect(
            host=v.host(ort),
            user=v.user(ort),
            passwd=v.passwd(ort),
            database=v.database(database),
            auth_plugin='mysql_native_password') as mydb:
        my_cursor = mydb.cursor()
        sql_stuff = (f"INSERT INTO `Tankdaten`.`Data` (`Zeit`,`brand`,`diesel`,`e10`,`e5`,`id`,`isOpen`,`lat`,`lng`,"
                     f"`name`,`postCode`) VALUES (%s, %s ,%s, %s, %s, %s, %s, %s, %s, %s, %s);")
        my_cursor.executemany(sql_stuff, datalist)
        mydb.commit()


for tanke in data["stations"]:
    zeit = time.strftime("%Y-%m-%d %H:%M:%S")
    list.append((zeit, tanke["brand"], tanke["diesel"], tanke["e10"], tanke["e5"], tanke["id"], tanke["isOpen"],
                 tanke["lat"], tanke["lng"], tanke["name"], tanke["postCode"]))

data_uploader(list)

profiler.stop()

profiler.print(color=True, show_all=False)
