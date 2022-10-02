import requests
from package import variables as v
import json
from pprint import pprint
import mysql.connector
import marshmallow
res = requests.get('https://creativecommons.tankerkoenig.de/json/list.php?lat=52.521&lng=13.438&rad=25&sort=dist&type=all&apikey='+v.tanke_api)
data = json.loads(res.content.decode())
pprint(data)
print(data["stations"][0]["brand"])
print(data["stations"][1]["brand"])
print(data["stations"][2]["brand"])
ort = "home"
database = "Tankdaten"
with mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password') as mydb:
    my_cursor = mydb.cursor()
    my_cursor.execute(f'')