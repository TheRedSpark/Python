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
Windrichtung_l = []
Temperatur_l = []
Feuchtigkeit_l = []
Strahlung_l = []
Druck_l = []
Windgeschwindigkeit_l = []
PM10_As_l = []
PM10_BaP_l = []
PM10_Cd_l = []
PM10_Ni_l = []
PM10_Pb_l = []
BEN_l = []
NO_l = []
NO2_l = []
O3_l = []
PM10_TEOM_l = []
PM10_HVS_l = []
PM10_eCT_l = []
PM10_oCT_l = []
PM2_5_l = []
RUSSPM10_l = []
RUSS_PM1_l = []
TOL_l = []
XYL_l = []
data_temp = []
start = time.strftime("%Y-%m-%d %H:%M:%S")
mydb = mysql.connector.connect(
    host=v.host(ort),
    user=v.user(ort),
    passwd=v.passwd(ort),
    database=v.database(database),
    auth_plugin='mysql_native_password')

my_cursor = mydb.cursor()

my_cursor.execute(f"TRUNCATE `Air`.`Dresden-Nord`;")


def data_uploader(time, windricchtung):
    sql_stuff = "INSERT INTO `Air`.`Dresden-Nord` (`Zeit`,`WINDRI`) VALUES (%s, %s);" #todo: FIX type
    record1 = (time, windricchtung)
    my_cursor.execute(sql_stuff, record1)


def prim_getter(time, type):
    # print(f'Das ist zeit {time}')
    my_cursor.execute(f"SELECT id FROM `Air`.`Dresden-Nord` WHERE (`Zeit` = '{time}'); ")
    id = my_cursor.fetchone()
    id = int(str(id).replace("(", "").replace(",)", ""))
    return id


def data_updater_single(time, data, type):
    try:
        my_cursor.execute(f"UPDATE `Air`.`Dresden-Nord` SET `{type}` = {data} WHERE (`Zeit` = '{time}');")
    except ValueError:
        pass

    except SyntaxError:
        print("Syntax error")
        pass


def data_updater_many(data, type):
    for x in data:
        if x[0] == "NaN":
            x[0] = -1
        x[1] = x[1].replace(":30:00", ":00:00")

    try:
        sql_stuff = (f"UPDATE `Air`.`Dresden-Nord` SET `{type}` = %s WHERE (`Zeit` = %s);")
        my_cursor.executemany(sql_stuff, data)
    except ValueError:
        pass

    except SyntaxError:
        print("Syntax error")
        pass


mytree = ET.parse('Dresden-Nord.xml')
#mytree = ET.parse('test_dd.xml')


myroot = mytree.getroot()

for x in myroot[0]:  # Windrichtung
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    init_data.append(data)

for data in init_data:
    if not data[1] == "NaN":
        data_uploader(data[0], data[1])
    else:
        data_uploader(data[0], -1)
mydb.commit()
print("init")

for a in range(0, 24):
    list_nnn = myroot[a].attrib.get('name').split(" ")
    print(list_nnn)
    for x in myroot[a]:  # Temperatur
        data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
        time_xml = data[0].split(" ")
        date = time_xml[0].split(".")
        data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
        data_temp.append(data)
    data_updater_many(data_temp, list_nnn[1])
    mydb.commit()
    data_temp.clear()

mydb.close()
ende = time.strftime("%Y-%m-%d %H:%M:%S")

print()
print()
print(start)
print(ende)

session = profiler.stop()
profile_renderer = ConsoleRenderer(unicode=True, color=True, show_all=True)
print(profile_renderer.render(session))
