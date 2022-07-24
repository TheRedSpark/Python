from package import variables as v
import mysql.connector  # 8.0.28
import time

ort = "home"
database = "Main"
live = False


def fragen_getter():
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    my_cursor.execute(f"SELECT * FROM Main.Zoll order by rand() limit 1")
    results_raw = my_cursor.fetchone()
    return results_raw


while True:
    frage = fragen_getter()
    print(f'{frage[3]}\n\n'
          f'a) {frage[4]}\n'
          f'b) {frage[5]}\n'
          f'c) {frage[6]}\n'
          f'd) {frage[7]}\n'
          f'Antwort {frage[8]}')
    antwort = input("Welche Antwort möchtest du geben?\n")
    if antwort == frage[8]:
        print("Richtiges Ergebniss\n\n\n")
    else:
        print("leider Falsch\n\n\n")
