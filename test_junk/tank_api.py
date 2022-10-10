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
cords = [
         # ('52.506', '13.284', "Berlin", "Berlin"),
         # ('53.120', '8.596', "Bremen", "Bremen"),
         # ('53.558', '9.787', "Hamburg", "Hamburg"),
         # ('51.076', '13.632', "Dresden", "Sachsen"),
         # ('51.184', '14.373', "Bautzen", "Sachsen"),
         # ('50.985', '10.945', "Erfurt", "Türingen"),
         # ('51.224', '10.324', "Mühlhausen", "Türingen"),
         # ('48.155', '11.471', "München", "Bayern"),
         # ('48.719', '10.733', "Donauwörth", "Bayern"),
         # ('48.779', '9.107', "Stuttgart", "BadenW"),
         ('48.270', '8.787', "Balingen", "BadenW"),
         ('50.135', '8.802', "Hanau", "Hessen"),
         ('50.486', '9.011', "Schotten", "Hessen"),
         ('49.965', '8.172', "Mainz", "Reinland"),
         ('49.701', '7.349', "Idar-Oberstein", "Reinland"),
         ('49.247', '6.912', "Saarbrücken", "Saarland"),
         ('51.238', '6.674', "Düsseldorf", "NRW"),
         ('51.313', '7.946', "Sundern", "NRW"),
         ('52.379', '9.691', "Hannover", "Niedersachsen"),
         ('53.003', '9.774', "Soltau", "Niedersachsen"),
         ('52.126', '11.501', "Magdeburg", "Sachsen-Anhalt"),
         ('51.639', '11.486', "Hettstedt", "Sachsen-Anhalt"),
         ('52.428', '12.957', "Potsdam", "Brandenbrug"),
         ('51.967', '13.561', "Golßen", "Brandenburg"),
         ('53.615', '11.330', "Schwerin", "Mecpomm"),
         ('53.434', '11.130', "Hagenow", "Mecpomm"),
         ('54.341', '10.055', "Kiel", "Schleswig"),
         ('54.375', '9.085', "Friedrichstadt", "Schleswig")
         ]


def data_uploader(datalist):
    with mysql.connector.connect(
            host=v.host(ort),
            user=v.user(ort),
            passwd=v.passwd(ort),
            database=v.database(database),
            auth_plugin='mysql_native_password') as mydb:
        my_cursor = mydb.cursor()
        sql_stuff = (f"INSERT INTO `Tankdaten`.`Data` (`Zeit`,`brand`,`diesel`,`e10`,`e5`,`id`,`isOpen`,`lat`,`lng`,"
                     f"`name`,`postCode`,`ort`,`bundesland`) VALUES (%s, %s ,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s);")
        my_cursor.executemany(sql_stuff, datalist)
        mydb.commit()


for rad in cords:
    while True:
        try:
            print(f"Jetzt {rad[2]}")
            berlin_res = requests.get(
                f'https://creativecommons.tankerkoenig.de/json/list.php?lat={rad[0]}&lng={rad[1]}&rad=25&sort=dist&type=all&apikey=' + v.tanke_api)
            data = json.loads(berlin_res.content.decode())
            print(data["stations"])
            for tanke in data["stations"]:
                zeit = time.strftime("%Y-%m-%d %H:%M:%S")
                list.append((zeit, tanke["brand"], tanke["diesel"], tanke["e10"], tanke["e5"], tanke["id"], tanke["isOpen"],
                             tanke["lat"], tanke["lng"], tanke["name"], tanke["postCode"], rad[2], rad[3]))
            data_uploader(list)
            list.clear()
            print(f"Erfolg für {rad[2]}")
            break
        except:
            print(f"Fehler für {rad[2]}")
            time.sleep(5)
            continue


profiler.stop()

profiler.print(color=True, show_all=False)
