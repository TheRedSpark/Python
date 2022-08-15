import sys

import mysql.connector
from package import variables as v
import xml.etree.ElementTree as ET
import time
from pyinstrument import Profiler
from pyinstrument.renderers import ConsoleRenderer

profiler = Profiler(interval=0.001)
profiler.start()
ort = 'home'
database = 'Air'
init_data = []
test_l = []
liste_datensatze = ['Annaberg-Buchholz.xml', 'Bautzen.xml', 'Borna.xml', 'Carlsfeld.xml',
                    'Chemnitz-Hans-Link-Straße.xml', 'Collmberg.xml', 'Dresden-Bergmanstraße.xml', 'Dresden-Nord.xml',
                    'Dresden-Winckelmann.xml', 'Fichtelberg.xml', 'Freiberg.xml', 'Glauchau.xml', 'Goerlitz.xml',
                    'Klingentahl.xml', 'Leiptzig-Mitte.xml', 'Leiptzig-West.xml',
                    'Liebschutzberg.xml', 'Niesky.xml', 'Plauen-Sued.xml', 'Radebeul-Wahnsdorf.xml', 'Schkeuditz.xml',
                    'Zinnwald.xml', 'Zittau-Ost.xml']
liste_datensatze.sort()
# liste_datensatze = ['test_dd.xml']
data_temp = []
mydb = mysql.connector.connect(
    host=v.host(ort),
    user=v.user(ort),
    passwd=v.passwd(ort),
    database=v.database(database),
    auth_plugin='mysql_native_password')

my_cursor = mydb.cursor()

try:
    my_cursor.execute(f"DROP `Air`.`*`;")
except:
    pass


def table_create(ort):
    my_cursor.execute(f"CREATE TABLE `Air`.`{ort}` (`Zeit` DATETIME UNIQUE NOT NULL,`WINDRI` FLOAT NULL,"
                      f"`TEMP` FLOAT NULL,`FEUCHT` FLOAT NULL,`STRAHL` FLOAT NULL,`DRUCK` FLOAT NULL,"
                      f"`WINDGE` FLOAT NULL,`PM10_As` FLOAT NULL,`PM10_BaP` FLOAT NULL,`PM10_Cd` FLOAT NULL,"
                      f"`PM10_Ni` FLOAT NULL,`PM10_Pb` FLOAT NULL,`BEN` FLOAT NULL,`NO` FLOAT NULL,`NO2` FLOAT NULL,"
                      f"`O3` FLOAT NULL,`SO2` FLOAT NULL,`PM10_TEOM` FLOAT NULL,`PM10_HVS` FLOAT NULL,`PM10_eCT` FLOAT NULL,"
                      f"`PM10_oCT` FLOAT NULL,`R_Menge` FLOAT NULL,`PM2.5` FLOAT NULL,`RUSSPM10` FLOAT NULL,`RUSS_PM1` FLOAT NULL,"
                      f"`TOL` FLOAT NULL,`XYL` FLOAT NULL,PRIMARY KEY (`Zeit`),"
                      f"UNIQUE INDEX `Zeit_UNIQUE` (`Zeit` ASC) VISIBLE);")


def data_uploader(time, windricchtung, list, air_table):
    sql_stuff = (f"INSERT INTO `Air`.`{air_table}` (`Zeit`,`{list}`) VALUES (%s, %s);")
    record1 = (time, windricchtung)
    while True:
        try:
            my_cursor.execute(sql_stuff, record1)
            break
        except:
            print(f'{time=},{windricchtung=},{list=},{air_table=}')
            table_create(air_table)
            continue


def data_updater_many(data, type, air_table):
    for x in data:
        if x[0] == "NaN":
            x[0] = -1
        x[1] = x[1].replace(":30:00", ":00:00")

    try:
        sql_stuff = (f"UPDATE `Air`.`{air_table}` SET `{type}` = %s WHERE (`Zeit` = %s);")
        my_cursor.executemany(sql_stuff, data)
    except ValueError:
        pass

    except SyntaxError:
        print("Syntax error")
        pass


def worker(dadei):
    mytree = ET.parse(dadei)
    myroot = mytree.getroot()

    for x in myroot[0]:
        data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
        time_xml = data[0].split(" ")
        date = time_xml[0].split(".")
        data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
        init_data.append(data)

    for data in init_data:
        if not data[1] == "NaN":
            data_uploader(data[0], data[1], myroot[0].attrib.get('name').split(" ")[1],
                          myroot[0].attrib.get('name').split(" ")[0])
        else:
            data_uploader(data[0], -1, myroot[0].attrib.get('name').split(" ")[1],
                          myroot[0].attrib.get('name').split(" ")[0])
    mydb.commit()

    for a in range(0, 24):
        try:
            list_nnn = myroot[a].attrib.get('name').split(" ")
        except:
            break
        print(list_nnn)
        for x in myroot[a]:
            data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(
                ",")
            time_xml = data[0].split(" ")
            date = time_xml[0].split(".")
            data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
            data_temp.append(data)
        data_updater_many(data_temp, list_nnn[1], list_nnn[0])
        mydb.commit()
        data_temp.clear()
    init_data.clear()


for place in liste_datensatze:
    worker(place)

mydb.close()
session = profiler.stop()
profile_renderer = ConsoleRenderer(unicode=True, color=True, show_all=False)
print(profile_renderer.render(session))
