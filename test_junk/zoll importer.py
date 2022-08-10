from package import variables as v
import mysql.connector

ort = "home"
database = "Main"


def upload(fach_id, fach_name, frage, antwort_a, antwort_b, antwort_c, antwort_d, antwort_r):
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    sql_maske = "INSERT INTO `Main`.`Zoll` (`Fachbereich_Id`,`Fachbereich`,`Frage`,`Antwort_A`,`Antwort_B`,`Antwort_C`," \
                "`Antwort_D`,`Richtige_Antwort`) VALUES (%s, %s, %s, %s,%s,%s,%s,%s); "
    data_n = (fach_id, fach_name, frage, antwort_a, antwort_b, antwort_c, antwort_d, antwort_r)
    my_cursor.execute(sql_maske, data_n)
    mydb.commit()
    mydb.close()


fach_id = 1
fach_name = 'Fachspezifische Aufgaben zum Zoll'
while True:
    frage = input("Welche Frage? ")
    antwort_a = input("Antwort A ")
    antwort_b = input("Antwort B ")
    antwort_c = input("Antwort C ")
    antwort_d = input("Antwort D ")
    antwort_r = input("Richtige Antwort ")

    print(f'Frage : {frage}\n'
          f'Antwort A:{antwort_a}\n'
          f'Antwort B:{antwort_b}\n'
          f'Antwort C:{antwort_c}\n'
          f'Antwort D:{antwort_d}\n'
          f'Richtige Antwort: {antwort_r}')

    if input("War das richtig?").strip().lower() == "y" or "j":
        upload(fach_id, fach_name, frage, antwort_a, antwort_b, antwort_c, antwort_d, antwort_r)
    else:
        continue
