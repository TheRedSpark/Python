import requests
from package import variables as v
import json
from pprint import pprint
import mysql.connector
import time
import marshmallow

res = requests.get(
    'https://creativecommons.tankerkoenig.de/json/list.php?lat=52.521&lng=13.438&rad=25&sort=dist&type=all&apikey=' + v.tanke_api)
data = json.loads(res.content.decode())
pprint(data)
print(data["stations"][0]["brand"])
print(data["stations"][1]["brand"])
print(type(data["stations"][2]["isOpen"]))
ort = "home"
database = "Tankdaten"


def data_uploader(brand, diesel, e10, e5, id, isopen, lat, lng,name,postcode) -> None:
    zeit = time.strftime("%Y-%m-%d %H:%M:%S")
    with mysql.connector.connect(
            host=v.host(ort),
            user=v.user(ort),
            passwd=v.passwd(ort),
            database=v.database(database),
            auth_plugin='mysql_native_password') as mydb:
        my_cursor = mydb.cursor()
        sql_stuff = (f"INSERT INTO `Tankdaten`.`Data` (`Zeit`,`brand`,`diesel`,`e10`,`e5`,`id`,`isOpen`,`lat`,`lng`,"
                     f"`name`,`postCode`) VALUES (%s, %s ,%s, %s, %s, %s, %s, %s, %s, %s, %s);")
        record = (zeit, brand, diesel,e10,e5,id,isopen,lat,lng,name,postcode)
        my_cursor.execute(sql_stuff, record)
        mydb.commit()


for tanke in data["stations"]:
    data_uploader(tanke["brand"], tanke["diesel"], tanke["e10"], tanke["e5"], tanke["id"], tanke["isOpen"],
                  tanke["lat"], tanke["lng"], tanke["name"],tanke["postCode"])


