import sys

import mysql.connector
from package import variables as v
import xml.etree.ElementTree as ET
import time

ort = 'home'
database = 'Air'

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

mydb = mysql.connector.connect(
    host=v.host(ort),
    user=v.user(ort),
    passwd=v.passwd(ort),
    database=v.database(database),
    auth_plugin='mysql_native_password')

my_cursor = mydb.cursor()

my_cursor.execute(f"TRUNCATE `Air`.`Dresden-Nord`;")


# def data_uploader_alt(zeit, BEN, DRUCK, FEUCHT, NO, NO2, O3, PM10_As, PM10_BaP, PM10_Cd, PM10_eCT, PM10_HVS, PM10_Ni,
#                       PM10_oCT, PM10_Pb,
#                       PM10_TEOM, PM25, RUSS_PM1, SO2, STRAHL, TEMP, WINDGE, WINDRI):
#     mydb = mysql.connector.connect(
#         host=v.host(ort),
#         user=v.user(ort),
#         passwd=v.passwd(ort),
#         database=v.database(database),
#         auth_plugin='mysql_native_password')
#
#     my_cursor = mydb.cursor()
#     sql_stuff = "INSERT INTO `Air`.`Dresden-Nord` (`Zeit`,`Benzol`,`Luftdruck`,`relative_Feuchte`,`Stickstoffmonoxid`," \
#                 "`Stickstoffdioxid`,`Ozon`,`Arsen_im_Feinstaub_PM10`,`Benzo(a)pyren_im_Feinstaub_PM10`," \
#                 "`Cadmium im_Feinstaub_PM10`,`elementarer_Kohlenstoff_im_Feinstaub_PM10`," \
#                 "`Feinstaub_PM10_gravimetrisch_bestimmt`,`Nickel_im_Feinstaub_PM10`," \
#                 "`organischer_Kohlenstoff_im_Feinstaub_PM10`,`Blei_im_Feinstaub_PM10`," \
#                 "`Feinstaub_PM10_mit_kontinuierlichem_Messverfahren_bestimmt`," \
#                 "`Feinstaub_PM2.5_gravimetrisch_bestimmt`,`Russ`,`Schwefeldioxid`,`Globalstrahlung`,`Temperatur`," \
#                 "`Windgeschwindigkeit`,`Windrichtung`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
#                 " %s, %s, %s, %s, %s, %s, %s);"
#     record1 = (
#         zeit, BEN, DRUCK, FEUCHT, NO, NO2, O3, PM10_As, PM10_BaP, PM10_Cd, PM10_eCT, PM10_HVS, PM10_Ni, PM10_oCT,
#         PM10_Pb,
#         PM10_TEOM, PM25, RUSS_PM1, SO2, STRAHL, TEMP, WINDGE, WINDRI)
#     my_cursor.execute(sql_stuff, record1)
#     mydb.commit()


def data_uploader(time, windricchtung):
    sql_stuff = "INSERT INTO `Air`.`Dresden-Nord` (`Zeit`,`Windrichtung`) VALUES (%s, %s);"
    record1 = (time, windricchtung)
    my_cursor.execute(sql_stuff, record1)


def prim_getter(time, type):
    # print(f'Das ist zeit {time}')
    my_cursor.execute(f"SELECT id FROM `Air`.`Dresden-Nord` WHERE (`Zeit` = '{time}'); ")
    id = my_cursor.fetchone()
    id = int(str(id).replace("(", "").replace(",)", ""))
    return id



def data_updater(time, data, type):
    # print(time)
    try:
        id_t = prim_getter(time, time_xml)
        my_cursor.execute(f"UPDATE `Air`.`Dresden-Nord` SET `{type}` = {data} WHERE (`id` = {id_t});")
        if id_t % 500 == 0:
            print(f'Für {type} bei id:{id_t}')
    except ValueError:
        pass



# mytree = ET.parse('Dresden-Nord.xml')
mytree = ET.parse('test_dd.xml')
myroot = mytree.getroot()
for x in myroot[0]:  # Windrichtung
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    Windrichtung_l.append(data)

for x in myroot[1]:  # Temperatur
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    Temperatur_l.append(data)

for x in myroot[2]:  # Feuchtigkeit
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    Feuchtigkeit_l.append(data)

for x in myroot[3]:  # Strahlung
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    Strahlung_l.append(data)

for x in myroot[4]:  # Druck
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    Druck_l.append(data)

for x in myroot[5]:  # Windgeschwindigkeit
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    Windgeschwindigkeit_l.append(data)

for x in myroot[6]:  # PM10_As
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    PM10_As_l.append(data)

for x in myroot[7]:  # Druck
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    Druck_l.append(data)

for x in myroot[8]:  # PM10_BaP
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    PM10_BaP_l.append(data)

for x in myroot[9]:  # PM10_Cd
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    PM10_Cd_l.append(data)

for x in myroot[10]:  # PM10_Ni
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    PM10_Ni_l.append(data)

for x in myroot[11]:  # PM10_Pb
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    PM10_Pb_l.append(data)

for x in myroot[12]:  # BEN
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    BEN_l.append(data)

for x in myroot[13]:  # NO
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    NO_l.append(data)

for x in myroot[14]:  # NO2
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    NO2_l.append(data)

for x in myroot[15]:  # O3
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    O3_l.append(data)

# print(myroot[0].attrib)

# print(GRAD_l)
# print(GRADC_l)
# fehlschlag = []
#
print("Start Windrichtung")
start = time.strftime("%Y-%m-%d %H:%M:%S")
print(start)
for data in Windrichtung_l:
    if not data[1] == "NaN":
        data_uploader(data[0], data[1])
        # print(f'Fertig für {data[0]}')
    else:
        # print("Ausnahme")
        data_uploader(data[0], -1)
    # print(f'Fehlschlag für {data[0]}')
ende = time.strftime("%Y-%m-%d %H:%M:%S")
print(ende)
# print(f'Das Delta ist : {(ende - start)}')
mydb.commit()
print("Übergabe Temperatur")
# time.sleep(10)
start = time.strftime("%Y-%m-%d %H:%M:%S")
print(start)
for data in Temperatur_l:
    if not data[1] == "NaN":
        data_updater(data[0], data[1], "Temperatur")
        # print(f'Fertig für {data[0]}')
    else:
        data_updater(data[0], -1, "Temperatur")
        # print(f'Fehlschlag für {data[0]}')

ende = time.strftime("%Y-%m-%d %H:%M:%S")
print(ende)

mydb.commit()
print("Übergabe Strahlung")
for data in Strahlung_l:
    if not data[1] == "NaN":
        data_updater(data[0], data[1], "Globalstrahlung")
        # print(f'Fertig für {data[0]}')
    else:
        data_updater(data[0], -1, "Globalstrahlung")
        # print(f'Fehlschlag für {data[0]}')

mydb.commit()
print("Übergabe Druck")
for data in Druck_l:
    if not data[1] == "NaN":
        print(f'Versuch für {data[0]}')
        data_updater(data[0], data[1], "Luftdruck")
        print(f'Fertig für {data[0]}')
    else:
        data_updater(data[0], -1, "Luftdruck")
        print(f'Fehlschlag für {data[0]}')

    mydb.commit()
mydb.close()
