import sys

import mysql.connector
from package import variables as v
import xml.etree.ElementTree as ET
import time
from pyinstrument import Profiler
from pyinstrument.renderers import ConsoleRenderer
import threading

profiler = Profiler(interval=0.001)

ort = 'home'
database = 'Air'
test_l = []
exitFlag = 0
liste_datensatze = ['Annaberg-Buchholz.xml', 'Bautzen.xml', 'Borna.xml', 'Carlsfeld.xml',
                    'Chemnitz-Hans-Link-Straße.xml', 'Collmberg.xml', 'Dresden-Bergmanstraße.xml', 'Dresden-Nord.xml',
                    'Dresden-Winckelmann.xml', 'Fichtelberg.xml', 'Freiberg.xml', 'Glauchau.xml', 'Goerlitz.xml',
                    'Klingentahl.xml', 'Leiptzig-Mitte.xml', 'Leiptzig-West.xml',
                    'Liebschutzberg.xml', 'Niesky.xml', 'Plauen-Sued.xml', 'Radebeul-Wahnsdorf.xml', 'Schkeuditz.xml',
                    'Zinnwald.xml', 'Zittau-Ost.xml']
# liste_datensatze = ['Radebeul-Wahnsdorf.xml', 'Schkeuditz.xml', 'Zinnwald.xml', 'Zittau-Ost.xml']
liste_datensatze.sort()
# liste_datensatze = ['test_dd.xml']
data_temp = []
try:
    with mysql.connector.connect(
            host=v.host(ort),
            user=v.user(ort),
            passwd=v.passwd(ort),
            database=v.database(database),
            auth_plugin='mysql_native_password') as mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute(f'DROP DATABASE `Air`;')
        my_cursor.execute(f'CREATE SCHEMA `Air` ;')
except:
    pass


def table_create(ort_l):
    with mysql.connector.connect(
            host=v.host(ort),
            user=v.user(ort),
            passwd=v.passwd(ort),
            database=v.database(database),
            auth_plugin='mysql_native_password') as mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute(f"CREATE TABLE `Air`.`{ort_l}` (`Zeit` DATETIME UNIQUE NOT NULL,`WINDRI` FLOAT NULL,"
                          f"`TEMP` FLOAT NULL,`FEUCHT` FLOAT NULL,`STRAHL` FLOAT NULL,`DRUCK` FLOAT NULL,"
                          f"`WINDGE` FLOAT NULL,`PM10_As` FLOAT NULL,`PM10_BaP` FLOAT NULL,`PM10_Cd` FLOAT NULL,"
                          f"`PM10_Ni` FLOAT NULL,`PM10_Pb` FLOAT NULL,`BEN` FLOAT NULL,`NO` FLOAT NULL,`NO2` FLOAT NULL,"
                          f"`O3` FLOAT NULL,`SO2` FLOAT NULL,`PM10_TEOM` FLOAT NULL,`PM10_HVS` FLOAT NULL,`PM10_eCT` FLOAT NULL,"
                          f"`PM10_oCT` FLOAT NULL,`R_Menge` FLOAT NULL,`PM2.5` FLOAT NULL,`RUSSPM10` FLOAT NULL,`RUSS_PM1` FLOAT NULL,"
                          f"`TOL` FLOAT NULL,`XYL` FLOAT NULL,PRIMARY KEY (`Zeit`),"
                          f"UNIQUE INDEX `Zeit_UNIQUE` (`Zeit` ASC) VISIBLE);")


def data_inserter_many(data, type, air_table, thread_name):
    for x in data:
        if x[0] == "NaN":
            x[0] = -1
        x[1] = x[1].replace(":30:00", ":00:00")
    while True:
        try:
            with mysql.connector.connect(
                    host=v.host(ort),
                    user=v.user(ort),
                    passwd=v.passwd(ort),
                    database=v.database(database),
                    auth_plugin='mysql_native_password') as mydb:

                my_cursor = mydb.cursor()
                sql_stuff = (f"INSERT INTO `Air`.`{air_table}` (`WINDRI`,`Zeit`) VALUES (%s, %s);")
                my_cursor.executemany(sql_stuff, data)
                mydb.commit()
                break
        except:
            print(f'{thread_name}: Erstellt Table für {air_table}')
            table_create(air_table)
            continue


def data_updater_many(thread_name, data, type, air_table):
    # print(f'start {thread_name}')
    for x in data:
        if x[0] == "NaN":
            x[0] = -1
        x[1] = x[1].replace(":30:00", ":00:00")

    try:
        with mysql.connector.connect(
                host=v.host(ort),
                user=v.user(ort),
                passwd=v.passwd(ort),
                database=v.database(database),
                auth_plugin='mysql_native_password') as mydb:

            my_cursor = mydb.cursor()
            sql_stuff = (f"UPDATE `Air`.`{air_table}` SET `{type}` = %s WHERE (`Zeit` = %s);")
            my_cursor.executemany(sql_stuff, data)
            mydb.commit()
    except ValueError:
        pass

    except SyntaxError:
        print("Syntax error")
        pass


class myThread(threading.Thread):
    def __init__(self, data, datenart, air_table):
        threading.Thread.__init__(self)
        self.air_table = air_table
        self.datenart = datenart
        self.data = data
        self.name = datenart

    def run(self):
        # profiler.start()
        print("Starting " + self.name)
        data_updater_many(self.name, self.data, self.datenart, self.air_table)
        print("Exiting " + self.name)
        # session = profiler.stop()
        # profile_renderer = ConsoleRenderer(unicode=True, color=True, show_all=False)
        # print(profile_renderer.render(session))


def thread_worker(thread_name, ort_data):
    mytree = ET.parse(ort_data)
    myroot = mytree.getroot()

    list_nnn = myroot[0].attrib.get('name').split(" ")

    for x in myroot[0]:
        data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(
            ",")
        time_xml = data[0].split(" ")
        date = time_xml[0].split(".")
        data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
        data_temp.append(data)

    for x in data_temp:
        if x[0] == "NaN":
            x[0] = -1
        x[1] = x[1].replace(":30:00", ":00:00")
    while True:
        try:
            with mysql.connector.connect(
                    host=v.host(ort),
                    user=v.user(ort),
                    passwd=v.passwd(ort),
                    database=v.database(database),
                    auth_plugin='mysql_native_password') as mydb:

                my_cursor = mydb.cursor()
                sql_stuff = (f"INSERT INTO `Air`.`{list_nnn[0]}` (`WINDRI`,`Zeit`) VALUES (%s, %s);")
                my_cursor.executemany(sql_stuff, data_temp)
                mydb.commit()
                break
        except:
            print(f'{thread_name}: Erstellt Table für {list_nnn[0]}')
            table_create(list_nnn[0])
            continue

    # data_inserter_many(data_temp, list_nnn[1], list_nnn[0], thread_name)
    data_temp.clear()

    for a in range(0, 24):
        try:
            list_nnn = myroot[a].attrib.get('name').split(" ")
        except:
            break
        # print(f'{thread_name}: Macht für Table {list_nnn[0]} die Daten {list_nnn[1]}')
        for x in myroot[a]:
            data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(
                ",")
            time_xml = data[0].split(" ")
            date = time_xml[0].split(".")
            data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
            data_temp.append(data)
        thread1 = myThread(data_temp, list_nnn[1], list_nnn[0])
        thread1.start()
        thread1.join()
        # print(data_temp[0])
        # data_updater_many(data_temp, list_nnn[1], list_nnn[0])
        data_temp.clear()


for x in liste_datensatze:
    thread_worker("Test_Temp", x)
# threadLock = threading.Lock()
# Create new threads
# thread1 = myThread(1, "Thread-1", "Radebeul-Wahnsdorf.xml")
# thread2 = myThread(2, "Thread-2", "Schkeuditz.xml")
# thread3 = myThread(3, "Thread-3", "Zinnwald.xml")
# thread4 = myThread(4, "Thread-4", "Zittau-Ost.xml")
# thread_test = myThread(5, "Test-Thread", 5, "test_dd.xml")
# thread_test = myThread(5, "Test-Thread", 5, "Dresden-Nord.xml")
# Start new Threads
# thread1.start()
# thread1.join()
# time.sleep(30)
# thread2.start()
# thread2.join()
# thread3.start()
# thread4.start()
# thread_test.start()

# thread_worker("1", "Radebeul-Wahnsdorf.xml")
