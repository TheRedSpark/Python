import sys

import mysql.connector
from package import variables as v
import xml.etree.ElementTree as ET
import time
from pyinstrument import Profiler

profiler = Profiler()
profiler.start()
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
PM10_HVS_l = []
PM10_eCT_l = []
PM10_oCT_l = []
PM2_5_l = []
RUSSPM10_l = []
RUSS_PM1_l = []
TOL_l = []
XYL_l = []
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
    sql_stuff = "INSERT INTO `Air`.`Dresden-Nord` (`Zeit`,`Windrichtung`) VALUES (%s, %s);"
    record1 = (time, windricchtung)
    my_cursor.execute(sql_stuff, record1)


def prim_getter(time, type):
    # print(f'Das ist zeit {time}')
    my_cursor.execute(f"SELECT id FROM `Air`.`Dresden-Nord` WHERE (`Zeit` = '{time}'); ")
    id = my_cursor.fetchone()
    id = int(str(id).replace("(", "").replace(",)", ""))
    return id


def data_updater_single(time, data, type):
    # print(time)
    try:
        # id_t = prim_getter(time, time_xml)
        my_cursor.execute(f"UPDATE `Air`.`Dresden-Nord` SET `{type}` = {data} WHERE (`Zeit` = '{time}');")
        # if id_t % 2000 == 0:
        #     print(f'Für {type} bei id:{id_t}')
    except ValueError:
        pass

    except SyntaxError:
        print("Syntax error")
        pass


def data_updater_many(data, type):
    # print(time)
    for x in data:
        if x[0] == "NaN":
            x[0] = -1
        x[1] = x[1].replace(":30:00", ":00:00")

    try:
        # id_t = prim_getter(time, time_xml)
        sql_stuff = (f"UPDATE `Air`.`Dresden-Nord` SET `{type}` = %s WHERE (`Zeit` = %s);")
        # record = (data[1], data[0])
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
    Windrichtung_l.append(data)
print(f'{myroot[0].attrib} 0')

for x in myroot[1]:  # Temperatur
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
    Temperatur_l.append(data)
print(f'{myroot[1].attrib} 1')

for x in myroot[2]:  # Feuchtigkeit
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
    Feuchtigkeit_l.append(data)
print(f'{myroot[2].attrib} 2')

for x in myroot[3]:  # Strahlung
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
    Strahlung_l.append(data)
print(f'{myroot[3].attrib} 3')

for x in myroot[4]:  # Druck
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
    Druck_l.append(data)
print(f'{myroot[4].attrib} 4')

for x in myroot[5]:  # Windgeschwindigkeit
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
    Windgeschwindigkeit_l.append(data)
print(f'{myroot[5].attrib} 5')

for x in myroot[6]:  # PM10_As
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
    PM10_As_l.append(data)
print(f'{myroot[6].attrib} 6')

for x in myroot[7]:  # PM10_BaP
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
    PM10_BaP_l.append(data)
print(f'{myroot[7].attrib} 7')

for x in myroot[8]:  # PM10_Cd
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
    PM10_Cd_l.append(data)
print(f'{myroot[8].attrib} 8')

for x in myroot[9]:  # PM10_Ni
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
    PM10_Ni_l.append(data)
print(f'{myroot[9].attrib} 9')

for x in myroot[10]:  # PM10_Pb
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
    PM10_Pb_l.append(data)
print(f'{myroot[10].attrib} 10')

for x in myroot[11]:  # BEN
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
    BEN_l.append(data)
print(f'{myroot[11].attrib} 11')

for x in myroot[12]:  # NO
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
    NO_l.append(data)
print(f'{myroot[12].attrib} 12')

for x in myroot[13]:  # NO2
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
    NO2_l.append(data)
print(f'{myroot[13].attrib} 13')

for x in myroot[14]:  # O3
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
    O3_l.append(data)
print(f'{myroot[14].attrib} 14')

for x in myroot[15]:  # PM10_TEOM
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
    PM10_TEOM_l.append(data)
print(f'{myroot[15].attrib} 15')

for x in myroot[16]:  # PM10_HVS
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
    PM10_HVS_l.append(data)
print(f'{myroot[16].attrib} 16')

for x in myroot[17]:  # PM10_eCT
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
    PM10_eCT_l.append(data)
print(f'{myroot[17].attrib} 17')

for x in myroot[18]:  # PM10_oCT
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
    PM10_oCT_l.append(data)
print(f'{myroot[18].attrib} 18')

for x in myroot[19]:  # PM2_5
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
    PM2_5_l.append(data)
print(f'{myroot[19].attrib} 19')

for x in myroot[20]:  # RUSSPM10
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
    RUSSPM10_l.append(data)
print(f'{myroot[20].attrib} 20')

for x in myroot[21]:  # RUSS_PM1
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
    RUSS_PM1_l.append(data)
print(f'{myroot[21].attrib} 21')

for x in myroot[22]:  # TOL
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
    TOL_l.append(data)
print(f'{myroot[22].attrib} 22')

for x in myroot[21]:  # XYL
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time_xml = data[0].split(" ")
    date = time_xml[0].split(".")
    data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
    XYL_l.append(data)
print(f'{myroot[23].attrib} 23')

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
data_updater_many(Temperatur_l, "Temperatur")
mydb.commit()
print(f'Ende Temperatur: {time.strftime("%Y-%m-%d %H:%M:%S")}')
print()

print(f'Start Globalstrahlung: {time.strftime("%Y-%m-%d %H:%M:%S")}')
data_updater_many(Strahlung_l, "Globalstrahlung")
mydb.commit()
print(f'Ende Globalstrahlung: {time.strftime("%Y-%m-%d %H:%M:%S")}')
print()

print(f'Start Luftdruck: {time.strftime("%Y-%m-%d %H:%M:%S")}')
data_updater_many(Druck_l, "Luftdruck")
mydb.commit()
print(f'Ende Luftdruck: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')


print(f'Start Windgeschwindigkeit: {time.strftime("%Y-%m-%d %H:%M:%S")}')
data_updater_many(Windgeschwindigkeit_l, "Windgeschwindigkeit")
mydb.commit()
print(f'Ende Windgeschwindigkeit: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

print(f'Start PM10_As: {time.strftime("%Y-%m-%d %H:%M:%S")}')
data_updater_many(PM10_As_l, "Arsen_im_Feinstaub_PM10")
mydb.commit()
print(f'Ende PM10_As: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

print(f'Start PM10_BaP: {time.strftime("%Y-%m-%d %H:%M:%S")}')
data_updater_many(PM10_BaP_l, "Benzo(a)pyren_im_Feinstaub_PM10")
mydb.commit()
print(f'Ende PM10_BaP: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

print(f'Start PM10_Cd: {time.strftime("%Y-%m-%d %H:%M:%S")}')
data_updater_many(PM10_Cd_l, "Cadmium im_Feinstaub_PM10")
mydb.commit()
print(f'Ende PM10_Cd: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

print(f'Start PM10_Ni: {time.strftime("%Y-%m-%d %H:%M:%S")}')
data_updater_many(PM10_Ni_l, "Nickel_im_Feinstaub_PM10")
mydb.commit()
print(f'Ende PM10_Ni: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

print(f'Start PM10_Pb: {time.strftime("%Y-%m-%d %H:%M:%S")}')
data_updater_many(PM10_Pb_l, "Blei_im_Feinstaub_PM10")
mydb.commit()
print(f'Ende PM10_Pb: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

print(f'Start BEN: {time.strftime("%Y-%m-%d %H:%M:%S")}')
data_updater_many(BEN_l, "Benzol")
mydb.commit()
print(f'Ende BEN: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

print(f'Start NO: {time.strftime("%Y-%m-%d %H:%M:%S")}')
data_updater_many(NO_l, "Stickstoffmonoxid")
mydb.commit()
print(f'Ende NO: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

print(f'Start NO2: {time.strftime("%Y-%m-%d %H:%M:%S")}')
data_updater_many(NO2_l, "Stickstoffdioxid")
mydb.commit()
print(f'Ende NO2: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

print(f'Start O3: {time.strftime("%Y-%m-%d %H:%M:%S")}')
data_updater_many(O3_l, "Ozon")
mydb.commit()
print(f'Ende O3: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

print(f'Start PM10_TEOM: {time.strftime("%Y-%m-%d %H:%M:%S")}')
data_updater_many(PM10_TEOM_l, "Feinstaub_PM10_mit_kontinuierlichem_Messverfahren_bestimmt")
mydb.commit()
print(f'Ende PM10_TEOM: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

print(f'Start PM10_HVS: {time.strftime("%Y-%m-%d %H:%M:%S")}')
data_updater_many(PM10_HVS_l, "Feinstaub_PM2.5_gravimetrisch_bestimmt")
mydb.commit()
print(f'Ende PM10_HVS: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

print(f'Start PM10_eCT: {time.strftime("%Y-%m-%d %H:%M:%S")}')
data_updater_many(PM10_eCT_l, "elementarer_Kohlenstoff_im_Feinstaub_PM10")
mydb.commit()
print(f'Ende PM10_eCT: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

print(f'Start PM10_oCT: {time.strftime("%Y-%m-%d %H:%M:%S")}')
data_updater_many(PM10_oCT_l, "organischer_Kohlenstoff_im_Feinstaub_PM10")
mydb.commit()
print(f'Ende PM10_oCT: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

print(f'Start PM2.5: {time.strftime("%Y-%m-%d %H:%M:%S")}')
data_updater_many(PM2_5_l, "Feinstaub_PM10_gravimetrisch_bestimmt")
mydb.commit()
print(f'Ende PM2.5: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

# print(f'Start RUSSPM10: {time.strftime("%Y-%m-%d %H:%M:%S")}')
# for data in RUSSPM10_l:
#     if not data[1] == "NaN":
#         # print(f'Versuch für {data[0]}')
#         data_updater(data[0].replace(":30:00", ":00:00"), data[1],
#                      "Feinstaub_PM10_gravimetrisch_bestimmt")
#         # print(f'Fertig für {data[0]}')
#     else:
#         data_updater(data[0].replace(":30:00", ":00:00"), -1,
#                      "Feinstaub_PM10_gravimetrisch_bestimmt")
#         # print(f'Fehlschlag für {data[0]}')
#
# mydb.commit()
# print(f'Ende RUSSPM10: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

print(f'Start RUSS_PM1: {time.strftime("%Y-%m-%d %H:%M:%S")}')
data_updater_many(RUSS_PM1_l, "Russ")
mydb.commit()
print(f'Ende RUSS_PM1: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

# print(f'Start TOL: {time.strftime("%Y-%m-%d %H:%M:%S")}')
# for data in TOL_l:
#     if not data[1] == "NaN":
#         # print(f'Versuch für {data[0]}')
#         data_updater(data[0].replace(":30:00", ":00:00"), data[1],
#                      "Russ")
#         # print(f'Fertig für {data[0]}')
#     else:
#         data_updater(data[0].replace(":30:00", ":00:00"), -1,
#                      "Russ")
#         # print(f'Fehlschlag für {data[0]}')
#
# mydb.commit()
# print(f'Ende TOL: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

# print(f'Start XYL: {time.strftime("%Y-%m-%d %H:%M:%S")}')
# for data in XYL_L:
#     if not data[1] == "NaN":
#         # print(f'Versuch für {data[0]}')
#         data_updater(data[0].replace(":30:00", ":00:00"), data[1],
#                      "Russ")
#         # print(f'Fertig für {data[0]}')
#     else:
#         data_updater(data[0].replace(":30:00", ":00:00"), -1,
#                      "Russ")
#         # print(f'Fehlschlag für {data[0]}')
#
# mydb.commit()
# print(f'Ende XLY: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

mydb.close()
ende = time.strftime("%Y-%m-%d %H:%M:%S")

print()
print()
print(start)
print(ende)

profiler.stop()

profiler.print()
