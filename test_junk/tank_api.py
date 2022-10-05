import requests
from package import variables as v
import json
import mysql.connector
import time
from pyinstrument import Profiler
ort = "home"
database = "Tankdaten"
list = []
profiler = Profiler()
profiler.start()
lat = '52.506'
lng = '13.284'
cords = [('52.506','13.284',"berlin"), #berlin
          ('51.076','13.632',"dresden"), #dresden
          ('48.779','9.107',"stuttgart")] #stuttgart




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





for rad in cords:
    print(f"Jetzt {rad[2]}")
    berlin_res = requests.get(
        f'https://creativecommons.tankerkoenig.de/json/list.php?lat={rad[0]}&lng={rad[1]}8&rad=25&sort=dist&type=all&apikey=' + v.tanke_api)
    data = json.loads(berlin_res.content.decode())
    for tanke in data["stations"]:
        zeit = time.strftime("%Y-%m-%d %H:%M:%S")
        list.append((zeit, tanke["brand"], tanke["diesel"], tanke["e10"], tanke["e5"], tanke["id"], tanke["isOpen"],
                     tanke["lat"], tanke["lng"], tanke["name"], tanke["postCode"]))

data_uploader(list)

profiler.stop()

profiler.print(color=True, show_all=False)
