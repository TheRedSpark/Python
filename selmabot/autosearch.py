import time
import mysql.connector #8.0.28
import webgetting #own
from package import variables as v #own

# A global variable.
day = 0
ort = "home"
database = "Selma"
results_clean = []


def push(updates, user):
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    if updates:
        my_cursor.execute(
            f"UPDATE `Selma`.`Users` SET `Push` = '1' WHERE (`User_Id` = {user});")
    else:
        my_cursor.execute(
            f"UPDATE `Selma`.`Users` SET `Push` = '0' WHERE (`User_Id` = {user});")
    mydb.commit()
    my_cursor.close()


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
        my_cursor.execute(f"SELECT User_Id FROM `Selma`.`Users` WHERE Zugelassen = 1")
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
                continue
            elif data == 0:
                print("keine updates")
                push(False, person)
            elif data == 1:
                print("updates")
                push(True, person)
            else:
                print("grober fehler")
        results_raw = []
        results_clean = []
    time.sleep(10)
