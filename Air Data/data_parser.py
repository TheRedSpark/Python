import sys

import mysql.connector
from package import variables as v
import xml.etree.ElementTree as ET
import time

ort = 'home'
database = 'Air'
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
        if id_t % 2000 == 0:
            print(f'Für {type} bei id:{id_t}')
    except ValueError:
        pass

    except SyntaxError:
        print("Syntax error")
        pass


#mytree = ET.parse('Dresden-Nord.xml')
mytree = ET.parse('test_dd.xml')
myroot = mytree.getroot()
for x in myroot[0]:  # Windrichtung
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    Windrichtung_l.append(data)
print(f'{myroot[0].attrib} 0')

for x in myroot[1]:  # Temperatur
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    Temperatur_l.append(data)
print(f'{myroot[1].attrib} 1')

for x in myroot[2]:  # Feuchtigkeit
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    Feuchtigkeit_l.append(data)
print(f'{myroot[2].attrib} 2')

for x in myroot[3]:  # Strahlung
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    Strahlung_l.append(data)
print(f'{myroot[3].attrib} 3')

for x in myroot[4]:  # Druck
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    Druck_l.append(data)
print(f'{myroot[4].attrib} 4')

for x in myroot[5]:  # Windgeschwindigkeit
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    Windgeschwindigkeit_l.append(data)
print(f'{myroot[5].attrib} 5')

for x in myroot[6]:  # PM10_As
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    PM10_As_l.append(data)
print(f'{myroot[6].attrib} 6')

for x in myroot[7]:  # PM10_BaP
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    PM10_BaP_l.append(data)
print(f'{myroot[7].attrib} 7')

for x in myroot[8]:  # PM10_Cd
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    PM10_Cd_l.append(data)
print(f'{myroot[8].attrib} 8')

for x in myroot[9]:  # PM10_Ni
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    PM10_Ni_l.append(data)
print(f'{myroot[9].attrib} 9')

for x in myroot[10]:  # PM10_Pb
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    PM10_Pb_l.append(data)
print(f'{myroot[10].attrib} 10')

for x in myroot[11]:  # BEN
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    BEN_l.append(data)
print(f'{myroot[11].attrib} 11')

for x in myroot[12]:  # NO
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    NO_l.append(data)
print(f'{myroot[12].attrib} 12')

for x in myroot[13]:  # NO2
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    NO2_l.append(data)
print(f'{myroot[13].attrib} 13')

for x in myroot[14]:  # O3
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    O3_l.append(data)
print(f'{myroot[14].attrib} 14')

for x in myroot[15]:  # PM10_TEOM
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    PM10_TEOM_l.append(data)
print(f'{myroot[15].attrib} 15')

for x in myroot[15]:  # PM10_TEOM
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00', data[1]]
    test_l.append(data)
print(f'{myroot[15].attrib} 15')












time.sleep(40)
print(f'Start Windrichtung: {time.strftime("%Y-%m-%d %H:%M:%S")}')
for data in Windrichtung_l:
    if not data[1] == "NaN":
        data_uploader(data[0], data[1])
        # print(f'Fertig für {data[0]}')
    else:
        # print("Ausnahme")
        data_uploader(data[0], -1)
    # print(f'Fehlschlag für {data[0]}')
print(f'Ende Windrichtung: {time.strftime("%Y-%m-%d %H:%M:%S")}')
mydb.commit()
print()

print(f'Start Temperatur: {time.strftime("%Y-%m-%d %H:%M:%S")}')
for data in Temperatur_l:
    if not data[1] == "NaN":
        data_updater(data[0], data[1], "Temperatur")
        # print(f'Fertig für {data[0]}')
    else:
        data_updater(data[0], -1, "Temperatur")
        # print(f'Fehlschlag für {data[0]}')

mydb.commit()
print(f'Ende Temperatur: {time.strftime("%Y-%m-%d %H:%M:%S")}')
print()

print(f'Start Globalstrahlung: {time.strftime("%Y-%m-%d %H:%M:%S")}')
for data in Strahlung_l:
    if not data[1] == "NaN":
        data_updater(data[0], data[1], "Globalstrahlung")
        # print(f'Fertig für {data[0]}')
    else:
        data_updater(data[0], -1, "Globalstrahlung")
        # print(f'Fehlschlag für {data[0]}')

mydb.commit()
print(f'Ende Globalstrahlung: {time.strftime("%Y-%m-%d %H:%M:%S")}')
print()

print(f'Start Luftdruck: {time.strftime("%Y-%m-%d %H:%M:%S")}')
for data in Druck_l:
    if not data[1] == "NaN":
        # print(f'Versuch für {data[0]}')
        data_updater(data[0], data[1], "Luftdruck")
        # print(f'Fertig für {data[0]}')
    else:
        data_updater(data[0], -1, "Luftdruck")
        # print(f'Fehlschlag für {data[0]}')

mydb.commit()
print(f'Ende Luftdruck: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

print(f'Start Windgeschwindigkeit: {time.strftime("%Y-%m-%d %H:%M:%S")}')
for data in Windgeschwindigkeit_l:
    if not data[1] == "NaN":
        # print(f'Versuch für {data[0]}')
        data_updater(data[0], data[1], "Windgeschwindigkeit")
        # print(f'Fertig für {data[0]}')
    else:
        data_updater(data[0], -1, "Windgeschwindigkeit")
        # print(f'Fehlschlag für {data[0]}')

mydb.commit()
#print(Windgeschwindigkeit_l)
print(f'Ende Windgeschwindigkeit: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

print(f'Start PM10_As: {time.strftime("%Y-%m-%d %H:%M:%S")}')
for data in PM10_As_l:
    if not data[1] == "NaN":
        # print(f'Versuch für {data[0]}')
        data_updater(data[0].replace(":30:00",":00:00"), data[1], "Arsen_im_Feinstaub_PM10")
        # print(f'Fertig für {data[0]}')
    else:
        data_updater(data[0].replace(":30:00",":00:00"), -1, "Arsen_im_Feinstaub_PM10")
        #print(f'Fehlschlag für {data[0]}')


mydb.commit()
print(f'Ende PM10_As: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

print(f'Start PM10_BaP: {time.strftime("%Y-%m-%d %H:%M:%S")}')
for data in PM10_BaP_l:
    if not data[1] == "NaN":
        # print(f'Versuch für {data[0]}')
        data_updater(data[0].replace(":30:00",":00:00"), data[1], "Benzo(a)pyren_im_Feinstaub_PM10")
        # print(f'Fertig für {data[0]}')
    else:
        data_updater(data[0].replace(":30:00",":00:00"), -1, "Benzo(a)pyren_im_Feinstaub_PM10")
        #print(f'Fehlschlag für {data[0]}')


mydb.commit()
print(f'Ende PM10_BaP: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')


print(f'Start PM10_Cd: {time.strftime("%Y-%m-%d %H:%M:%S")}')
for data in PM10_Cd_l:
    if not data[1] == "NaN":
        # print(f'Versuch für {data[0]}')
        data_updater(data[0].replace(":30:00",":00:00"), data[1], "Cadmium im_Feinstaub_PM10")
        # print(f'Fertig für {data[0]}')
    else:
        data_updater(data[0].replace(":30:00",":00:00"), -1, "Cadmium im_Feinstaub_PM10")
        #print(f'Fehlschlag für {data[0]}')


mydb.commit()
print(f'Ende PM10_Cd: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

print(f'Start PM10_Ni: {time.strftime("%Y-%m-%d %H:%M:%S")}')
for data in PM10_Ni_l:
    if not data[1] == "NaN":
        # print(f'Versuch für {data[0]}')
        data_updater(data[0].replace(":30:00",":00:00"), data[1], "Nickel_im_Feinstaub_PM10")
        # print(f'Fertig für {data[0]}')
    else:
        data_updater(data[0].replace(":30:00",":00:00"), -1, "Nickel_im_Feinstaub_PM10")
        #print(f'Fehlschlag für {data[0]}')


mydb.commit()
print(f'Ende PM10_Ni: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')


print(f'Start PM10_Pb: {time.strftime("%Y-%m-%d %H:%M:%S")}')
for data in PM10_Pb_l:
    if not data[1] == "NaN":
        # print(f'Versuch für {data[0]}')
        data_updater(data[0].replace(":30:00",":00:00"), data[1], "Blei_im_Feinstaub_PM10")
        # print(f'Fertig für {data[0]}')
    else:
        data_updater(data[0].replace(":30:00",":00:00"), -1, "Blei_im_Feinstaub_PM10")
        #print(f'Fehlschlag für {data[0]}')


mydb.commit()
print(f'Ende PM10_Pb: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

print(f'Start BEN: {time.strftime("%Y-%m-%d %H:%M:%S")}')
for data in BEN_l:
    if not data[1] == "NaN":
        # print(f'Versuch für {data[0]}')
        data_updater(data[0], data[1], "Benzol")
        # print(f'Fertig für {data[0]}')
    else:
        data_updater(data[0], -1, "Benzol")
        #print(f'Fehlschlag für {data[0]}')


mydb.commit()
print(f'Ende BEN: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

print(f'Start NO: {time.strftime("%Y-%m-%d %H:%M:%S")}')
for data in NO_l:
    if not data[1] == "NaN":
        # print(f'Versuch für {data[0]}')
        data_updater(data[0], data[1], "Stickstoffmonoxid")
        # print(f'Fertig für {data[0]}')
    else:
        data_updater(data[0], -1, "Stickstoffmonoxid")
        #print(f'Fehlschlag für {data[0]}')


mydb.commit()
print(f'Ende NO: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

print(f'Start NO2: {time.strftime("%Y-%m-%d %H:%M:%S")}')
for data in NO2_l:
    if not data[1] == "NaN":
        # print(f'Versuch für {data[0]}')
        data_updater(data[0], data[1], "Stickstoffdioxid")
        # print(f'Fertig für {data[0]}')
    else:
        data_updater(data[0], -1, "Stickstoffdioxid")
        #print(f'Fehlschlag für {data[0]}')


mydb.commit()
print(f'Ende NO2: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

print(f'Start O3: {time.strftime("%Y-%m-%d %H:%M:%S")}')
for data in O3_l:
    if not data[1] == "NaN":
        # print(f'Versuch für {data[0]}')
        data_updater(data[0], data[1], "Ozon")
        # print(f'Fertig für {data[0]}')
    else:
        data_updater(data[0], -1, "Ozon")
        #print(f'Fehlschlag für {data[0]}')


mydb.commit()
print(f'Ende O3: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')
#print(O3_l)

print(f'Start PM10_TEOM: {time.strftime("%Y-%m-%d %H:%M:%S")}')
for data in PM10_TEOM_l:
    if not data[1] == "NaN":
        # print(f'Versuch für {data[0]}')
        data_updater(data[0].replace(":30:00",":00:00"), data[1], "Feinstaub_PM10_mit_kontinuierlichem_Messverfahren_bestimmt")
        # print(f'Fertig für {data[0]}')
    else:
        data_updater(data[0].replace(":30:00",":00:00"), -1, "Feinstaub_PM10_mit_kontinuierlichem_Messverfahren_bestimmt")
        #print(f'Fehlschlag für {data[0]}')


mydb.commit()
print(f'Ende PM10_TEOM: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

#print(PM10_TEOM_l)




mydb.close()
