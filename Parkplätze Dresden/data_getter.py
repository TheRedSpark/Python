from bs4 import BeautifulSoup  # V4.10.0
import requests  # V2.27.1
import time
import mysql.connector  # V8.0.28
from package import variables as v

ort = "home"
database = "Main"
url = "https://www.dresden.de/apps_ext/ParkplatzApp/index"
stunde = 100
zeit_idle = 30


def upload(data, ident, time_sql):
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    if len(data) <= 5:
        data.append(-1)
    sql_maske = "INSERT INTO `Main`.`Park` (`Zeit`,`Ident_Park`,`Place`,`Anzahl`,`Frei`) VALUES (%s, %s, %s, %s, %s);"
    data_n = (
        time_sql, ident, data[0], data[2], data[4])
    my_cursor.execute(sql_maske, data_n)
    mydb.commit()
    mydb.close()


def fetching():
    i = 0
    a = 0
    index = ""
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all('div', attrs={'class': 'element element_table responsiveTable'})
    time_sql = time.strftime("%Y-%m-%d %H:%M:%S")
    for orte in table:
        rows = table[i].find_all('tr')
        i = i + 1
        for platze in rows:
            simple_rows = rows[a].text.split("\n")
            place = [feld for feld in simple_rows if feld != '']
            if a == 0:
                index = place[0]
            else:
                upload(place, index, time_sql)
            a = a + 1
        a = 0


while True:
    zeit = time.strftime("%Y-%m-%d %H:%M:%S")
    trigger = time.gmtime()
    if trigger.tm_hour != stunde:
        stunde = trigger.tm_hour
        fetching()
        continue
    else:
        # print(f'Daten bereits für den heutigen Tag den {day} eingetragen!')
        pass

    time.sleep(zeit_idle)
