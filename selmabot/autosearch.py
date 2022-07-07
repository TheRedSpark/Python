import time
import webgetting
import mysql.connector
from package import variables as v
day = 0
ort = "home"
database = "Selma"
results_clean = []
while True:
    zeit = time.strftime("%Y-%m-%d %H:%M:%S")
    trigger = time.gmtime()
    if trigger.tm_mday != day:
        day = trigger.tm_mday
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    my_cursor.execute(f"SELECT User_Id FROM `Selma`.`Users` ")
    results_raw = my_cursor.fetchall()
    my_cursor.close()
    for raw in results_raw:
        clen = int(str(raw).replace("(", "").replace(",)", "").strip())
        results_clean.append(clen)
    print(results_clean)
    for person in results_clean:
        data = webgetting.exam_updater(person)
        print(data)
        if data is False:
            # print(exam_data)
            print("fehler bei zugang")
        elif data == 0:
            print("keine updates")
        elif data == 1:
            print("updates")
        else:
            print("grober fehler")
    break