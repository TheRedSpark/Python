import matplotlib.pyplot as plt # V3.5.2
import pandas as pd # V1.4.2
import mysql.connector # V8.0.28
from SQL_Daten import zugang as anbin #Own Library
ort = 'lap'
database = 'Wetter'
mydb = mysql.connector.connect(
        host=anbin.host(ort),
        user=anbin.user(ort),
        passwd=anbin.passwd(ort),
        database=anbin.database(database),
        auth_plugin='mysql_native_password')

my_cursor = mydb.cursor()
my_cursor.execute("SELECT Temperatur FROM Wetter.Gesammt where Wetter_Orte_Id = 7 order by Zeit desc limit 1000")
inhalt = my_cursor.fetchall()
plt.xlabel('Zeitraum')
plt.ylabel('Temperatur')
data = []
print(data)
for points in inhalt:
        v = str(points)
        ve = v.replace(",", "").replace("(", "").replace(")", "")
        ver = float(ve)
        data.append(ver)
        print(ver)
        #print(type(ver))
a = len(data) + 1
print("feritig")
print(a)
#plt.axis([0, 150, 0, 0.6])
#xmin, xmax, ymin, ymax = 0, 0, 50, 50
s = pd.Series(data, index=range(1, a))
#d = pd.Series(data2, index=range(1, b))
#d.plot.bar()
s.plot()
#plt.axhline(y=0, color='r', linestyle='-')
plt.show()
print(data)