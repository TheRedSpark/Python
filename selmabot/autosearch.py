import time
import mysql.connector  # 8.0.28
import webgetting  # own
from package import variables as v  # own

# A global variable.
stunde = 0
ort = "home"
database = "Selma"
results_clean = []


def error_counter(error, user):
    if error:
        mydb = mysql.connector.connect(
            host=v.host(ort),
            user=v.user(ort),
            passwd=v.passwd(ort),
            database=v.database(database),
            auth_plugin='mysql_native_password')

        my_cursor = mydb.cursor()
        my_cursor.execute(
            f"SELECT Error_Anmeldung FROM `Selma`.`Users` WHERE User_Id = {user}")
        fehleranzahl = my_cursor.fetchone()
        print(fehleranzahl)
        fehleranzahl = int(str(fehleranzahl).replace("(", "").replace(",)", "")) + 1
        print(fehleranzahl)
        my_cursor.execute(
            f"UPDATE `Selma`.`Users` SET `Error_Anmeldung` = {fehleranzahl} WHERE (`User_Id` = {user});")
        mydb.commit()
        my_cursor.close()

    if not error:
        mydb = mysql.connector.connect(
            host=v.host(ort),
            user=v.user(ort),
            passwd=v.passwd(ort),
            database=v.database(database),
            auth_plugin='mysql_native_password')

        my_cursor = mydb.cursor()
        my_cursor.execute(
            f"UPDATE `Selma`.`Users` SET `Error_Anmeldung` = '0' WHERE (`User_Id` = {user});")
        mydb.commit()
        my_cursor.close()
    else:
        pass


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

def main():
    while True:
        zeit = time.strftime("%Y-%m-%d %H:%M:%S")
        trigger = time.gmtime()
        if trigger.tm_hour + 2 != stunde:
            stunde = trigger.tm_hour + 2
            if 7 < stunde < 18:
                print(trigger)
                mydb = mysql.connector.connect(
                    host=v.host(ort),
                    user=v.user(ort),
                    passwd=v.passwd(ort),
                    database=v.database(database),
                    auth_plugin='mysql_native_password')

                my_cursor = mydb.cursor()
                my_cursor.execute(
                    f"SELECT User_Id FROM `Selma`.`Users` WHERE Zugelassen = 1 and Push_Toggle = 1 and Error_Anmeldung <= 20")
                results_raw = my_cursor.fetchall()
                my_cursor.close()
                for raw in results_raw:
                    clen = int(str(raw).replace("(", "").replace(",)", "").strip())
                    results_clean.append(clen)
                print(results_clean)
                for person in results_clean:
                    print(person)
                    data = webgetting.exam_updater(person)
                    print(data)
                    if data is False:
                        print("Fehler beim Zugang")
                        error_counter(True, person)
                        continue
                    elif data == 0:
                        print("keine Updates")
                        error_counter(False, person)
                        push(False, person)
                    elif data == 1:
                        print("Updates")
                        error_counter(False, person)
                        push(True, person)
                    else:
                        print("grober Fehler")
            else:
                pass
            results_raw = []
            results_clean = []
        time.sleep(10)
