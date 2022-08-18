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
init_data = []
test_l = []
exitFlag = 0
liste_datensatze = ['Annaberg-Buchholz.xml', 'Bautzen.xml', 'Borna.xml', 'Carlsfeld.xml',
                    'Chemnitz-Hans-Link-Straße.xml', 'Collmberg.xml', 'Dresden-Bergmanstraße.xml', 'Dresden-Nord.xml',
                    'Dresden-Winckelmann.xml', 'Fichtelberg.xml', 'Freiberg.xml', 'Glauchau.xml', 'Goerlitz.xml',
                    'Klingentahl.xml', 'Leiptzig-Mitte.xml', 'Leiptzig-West.xml',
                    'Liebschutzberg.xml', 'Niesky.xml', 'Plauen-Sued.xml', 'Radebeul-Wahnsdorf.xml', 'Schkeuditz.xml',
                    'Zinnwald.xml', 'Zittau-Ost.xml']
liste_datensatze = ['Radebeul-Wahnsdorf.xml', 'Schkeuditz.xml', 'Zinnwald.xml', 'Zittau-Ost.xml']
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
        my_cursor.execute(f'DROP Table `Air`.`Dresden-Nord`')
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


def data_uploader(time, windricchtung, list, air_table):
    while True:
        try:
            with mysql.connector.connect(
                    host=v.host(ort),
                    user=v.user(ort),
                    passwd=v.passwd(ort),
                    database=v.database(database),
                    auth_plugin='mysql_native_password') as mydb:
                my_cursor = mydb.cursor()
                sql_stuff = (f"INSERT INTO `Air`.`{air_table}` (`Zeit`,`{list}`) VALUES (%s, %s);")
                record1 = (time, windricchtung)
                my_cursor.execute(sql_stuff, record1)
                mydb.commit()
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


def thread_worker(thread_name, ort_data):
    mytree = ET.parse(ort_data)
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

    for a in range(0, 24):
        try:
            list_nnn = myroot[a].attrib.get('name').split(" ")
        except:
            break
        print(f'Thread:{thread_name} macht {list_nnn}')
        for x in myroot[a]:
            data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(
                ",")
            time_xml = data[0].split(" ")
            date = time_xml[0].split(".")
            data = [data[1], f'20{date[2]}-{date[1]}-{date[0]} {time_xml[1]}:00']
            data_temp.append(data)
        data_updater_many(data_temp, list_nnn[1], list_nnn[0])
        data_temp.clear()
    init_data.clear()


class myThread(threading.Thread):
    def __init__(self, threadID, name, counter, data_ort):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.data_ort = data_ort

    def run(self):
        profiler.start()
        print("Starting " + self.name)
        thread_worker(self.name, self.data_ort)
        print("Exiting " + self.name)
        session = profiler.stop()
        profile_renderer = ConsoleRenderer(unicode=True, color=True, show_all=False)
        print(profile_renderer.render(session))


# Create new threads
thread1 = myThread(1, "Thread-1", 1, liste_datensatze.pop())
thread2 = myThread(2, "Thread-2", 2, liste_datensatze.pop())
thread3 = myThread(3, "Thread-3", 4, liste_datensatze.pop())
thread4 = myThread(4, "Thread-4", 4, liste_datensatze.pop())
thread_test = myThread(5,"Testthread",5,"test_dd.xml")
# Start new Threads
#thread1.start()
#thread2.start()
#thread3.start()
#thread4.start()
thread_test.start()

# thread_worker("1", "Radebeul-Wahnsdorf.xml")


