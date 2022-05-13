from datetime import datetime

import mysql.connector
from SQL_Daten import zugang as anbin
import time
ort = 'lap'
database = 'Wetter'

def zeitabstand():
        mydb = mysql.connector.connect(
                host=anbin.host(ort),
                user=anbin.user(ort),
                passwd=anbin.passwd(ort),
                database=anbin.database(database),
                auth_plugin='mysql_native_password')

        my_cursor = mydb.cursor()
        my_cursor.execute("SELECT Zeit FROM Wetter.Neugersdorf order by Zeit desc limit 1")
        inhalt = my_cursor.fetchall()
        data = []
        for points in inhalt:
                v = str(points)
                ve = v.replace("(", "").replace(")", "").replace("datetime.datetime","").replace(" ","")
                ver = ve
                data.append(ver)
        früher = data[0].split(",")
        del früher[6]
        jahr_alt = int(früher[0])
        monat_alt = int(früher[1])
        tag_alt = int(früher[2])
        stunde_alt = int(früher[3])
        minute_alt = int(früher[4])
        sekunde_alt = int(früher[5])
        jahr_aktuell = int(time.strftime("%Y"))
        monat_aktuell = int(time.strftime("%m"))
        tag_aktuell = int(time.strftime("%d"))
        stunde_aktuell = int(time.strftime("%H"))
        minute_aktuell = int(time.strftime("%M"))
        sekunde_akutell = int(time.strftime("%S"))
        then = datetime(jahr_alt, monat_alt, tag_alt, stunde_alt, minute_alt, sekunde_alt)
        now = datetime(jahr_aktuell, monat_aktuell, tag_aktuell, stunde_aktuell, minute_aktuell, sekunde_akutell)
        delta = now - then
        mydb.close()
        return delta

print(zeitabstand())