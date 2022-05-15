# stand 15.05.2022 live
import mysql.connector  # V8.0.28
import time  # bereits implementiert
import pyowm  # V2.10.0
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import variables as v  # eigene
import zugang as integration  # eigene

x = 1
schutzsleep = 60
zeit_idle = 10
wind_speed = 1
intervall = 5
rain = ""
username = v.username
password = v.password
mail_from = v.mail_from
mail_to = v.mail_to
mail_subject_rain = v.mail_subject_rain
mail_subject_wind = v.mail_subject_wind

ort = 'home'
database = 'Wetter'

mydb = mysql.connector.connect(
    host=integration.host(ort),
    user=integration.user(ort),
    passwd=integration.passwd(ort),
    database=integration.database(database),
    auth_plugin='mysql_native_password')

my_cursor = mydb.cursor()

städte = v.städte  # hier kannst du eine einfache Liste einfügen, wo die in str Type die
# Städte angibst im Format "'Berlin, DE'"
owm = pyowm.OWM(v.api_id)

"""""""""
Main Functions Definition
"""""


def fetching():
    for city in städte:
        sf = owm.weather_at_place(city)
        weather = sf.get_weather()
        clouds = weather.get_clouds()  # Cloud coverage
        rainatl = weather.get_rain()  # Rain volume
        rainalt2 = str(rainatl)
        rain = rainalt2.replace("{", "").replace("'1h': ", "").replace("}", "")
        snowalt = weather.get_snow()  # Snow volume
        snowalt2 = str(snowalt)
        snow = snowalt2.replace("{", "").replace("'1h': ", "").replace("}", "")
        wind_speedalt = 3.6 * weather.get_wind()['speed']  # Wind direction and speed
        wind_speed = wind_speedalt.__round__(2)
        wind = weather.get_wind()['deg']
        humidity = weather.get_humidity()  # Humidity percentage
        pressure = weather.get_pressure()['press']  # Atmospheric pressure
        temp = weather.get_temperature('celsius')['temp']
        temp_max = weather.get_temperature('celsius')['temp_max']
        temp_min = weather.get_temperature('celsius')['temp_min']
        time_sql = time.strftime("%Y-%m-%d %H:%M:%S")
        general = weather.get_detailed_status()  # Get general status of weather
        record1 = (temp, time_sql, humidity, wind_speed, clouds, rain, snow, pressure, wind, general)  # SQL insert
        # time_mail = time.strftime("%d %m %H:%M")
        # sunrise = weather.get_sunrise_time() #Sunrise time (GMT UNIXtime or ISO 8601)
        # sunset = weather.get_sunset_time() #Sunset time (GMT UNIXtime or ISO 8601)
        # visibility = weather.get_lastupdate()

        if city == 'Berlin, DE':
            wetterid = 1
            sqlStuff = "INSERT INTO `Wetter`.`Berlin` (`Temperatur`,`Zeit`,`Luftfeuchtigkeit`," \
                       "`Windgeschwindigkeit`,`Wolken`, `Regen`, `Schnee`, `Luftdruck`,`Windrichtung`," \
                       "`Zusammenfassung`) VALUES (%s, %s, %s, %s, %s, " \
                       "%s, %s, %s, %s, %s); "
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()
            sqlMain = "INSERT INTO `Wetter`.`Gesammt` (`Temperatur`,`Zeit`,`Luftfeuchtigkeit`," \
                      "`Windgeschwindigkeit`,`Wolken`, `Regen`, `Schnee`, `Luftdruck`,`Windrichtung`," \
                      " `Zusammenfassung`, `Wetter_Orte_Id`) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s); "
            record2 = (temp, time_sql, humidity, wind_speed, clouds, rain, snow, pressure, wind, general, wetterid)
            my_cursor.execute(sqlMain, record2)
            mydb.commit()
            print(f'Erfolg in der SQL Eingabe für {city}')

        elif city == 'London, GB':
            wetterid = 2
            sqlStuff = "INSERT INTO `Wetter`.`London` (`Temperatur`,`Zeit`,`Luftfeuchtigkeit`," \
                       "`Windgeschwindigkeit`,`Wolken`, `Regen`, `Schnee`, `Luftdruck`,`Windrichtung`," \
                       "`Zusammenfassung`) VALUES (%s, %s, %s, %s, %s, " \
                       "%s, %s, %s, %s, %s); "
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()
            sqlMain = "INSERT INTO `Wetter`.`Gesammt` (`Temperatur`,`Zeit`,`Luftfeuchtigkeit`," \
                      "`Windgeschwindigkeit`,`Wolken`, `Regen`, `Schnee`, `Luftdruck`,`Windrichtung`," \
                      " `Zusammenfassung`, `Wetter_Orte_Id`) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s); "
            record2 = (temp, time_sql, humidity, wind_speed, clouds, rain, snow, pressure, wind, general, wetterid)
            my_cursor.execute(sqlMain, record2)
            mydb.commit()
            print(f'Erfolg in der SQL Eingabe für {city}')

        elif city == 'Hamburg, DE':
            wetterid = 3
            sqlStuff = "INSERT INTO `Wetter`.`Hamburg` (`Temperatur`,`Zeit`,`Luftfeuchtigkeit`," \
                       "`Windgeschwindigkeit`,`Wolken`, `Regen`, `Schnee`, `Luftdruck`,`Windrichtung`," \
                       "`Zusammenfassung`) VALUES (%s, %s, %s, %s, %s, " \
                       "%s, %s, %s, %s, %s); "
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()
            sqlMain = "INSERT INTO `Wetter`.`Gesammt` (`Temperatur`,`Zeit`,`Luftfeuchtigkeit`," \
                      "`Windgeschwindigkeit`,`Wolken`, `Regen`, `Schnee`, `Luftdruck`,`Windrichtung`," \
                      " `Zusammenfassung`, `Wetter_Orte_Id`) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s); "
            record2 = (temp, time_sql, humidity, wind_speed, clouds, rain, snow, pressure, wind, general, wetterid)
            my_cursor.execute(sqlMain, record2)
            mydb.commit()
            print(f'Erfolg in der SQL Eingabe für {city}')

        elif city == 'Kiel, DE':
            wetterid = 4
            sqlStuff = "INSERT INTO `Wetter`.`Kiel` (`Temperatur`,`Zeit`,`Luftfeuchtigkeit`," \
                       "`Windgeschwindigkeit`,`Wolken`, `Regen`, `Schnee`, `Luftdruck`,`Windrichtung`," \
                       "`Zusammenfassung`) VALUES (%s, %s, %s, %s, %s, " \
                       "%s, %s, %s, %s, %s); "
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()
            sqlMain = "INSERT INTO `Wetter`.`Gesammt` (`Temperatur`,`Zeit`,`Luftfeuchtigkeit`," \
                      "`Windgeschwindigkeit`,`Wolken`, `Regen`, `Schnee`, `Luftdruck`,`Windrichtung`," \
                      " `Zusammenfassung`, `Wetter_Orte_Id`) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s); "
            record2 = (temp, time_sql, humidity, wind_speed, clouds, rain, snow, pressure, wind, general, wetterid)
            my_cursor.execute(sqlMain, record2)
            mydb.commit()
            print(f'Erfolg in der SQL Eingabe für {city}')

        elif city == 'Stuttgart, DE':
            wetterid = 5
            sqlStuff = "INSERT INTO `Wetter`.`Stuttgart` (`Temperatur`,`Zeit`,`Luftfeuchtigkeit`," \
                       "`Windgeschwindigkeit`,`Wolken`, `Regen`, `Schnee`, `Luftdruck`,`Windrichtung`," \
                       "`Zusammenfassung`) VALUES (%s, %s, %s, %s, %s, " \
                       "%s, %s, %s, %s, %s); "
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()
            sqlMain = "INSERT INTO `Wetter`.`Gesammt` (`Temperatur`,`Zeit`,`Luftfeuchtigkeit`," \
                      "`Windgeschwindigkeit`,`Wolken`, `Regen`, `Schnee`, `Luftdruck`,`Windrichtung`," \
                      " `Zusammenfassung`, `Wetter_Orte_Id`) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s); "
            record2 = (temp, time_sql, humidity, wind_speed, clouds, rain, snow, pressure, wind, general, wetterid)
            my_cursor.execute(sqlMain, record2)
            mydb.commit()
            print(f'Erfolg in der SQL Eingabe für {city}')

        elif city == 'Paris, FR':
            wetterid = 6
            sqlStuff = "INSERT INTO `Wetter`.`Paris` (`Temperatur`,`Zeit`,`Luftfeuchtigkeit`," \
                       "`Windgeschwindigkeit`,`Wolken`, `Regen`, `Schnee`, `Luftdruck`,`Windrichtung`," \
                       "`Zusammenfassung`) VALUES (%s, %s, %s, %s, %s, " \
                       "%s, %s, %s, %s, %s); "
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()
            sqlMain = "INSERT INTO `Wetter`.`Gesammt` (`Temperatur`,`Zeit`,`Luftfeuchtigkeit`," \
                      "`Windgeschwindigkeit`,`Wolken`, `Regen`, `Schnee`, `Luftdruck`,`Windrichtung`," \
                      " `Zusammenfassung`, `Wetter_Orte_Id`) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s); "
            record2 = (temp, time_sql, humidity, wind_speed, clouds, rain, snow, pressure, wind, general, wetterid)
            my_cursor.execute(sqlMain, record2)
            mydb.commit()
            print(f'Erfolg in der SQL Eingabe für {city}')

        elif city == 'Prag, CZ':
            wetterid = 7
            sqlStuff = "INSERT INTO `Wetter`.`Prag` (`Temperatur`,`Zeit`,`Luftfeuchtigkeit`," \
                       "`Windgeschwindigkeit`,`Wolken`, `Regen`, `Schnee`, `Luftdruck`,`Windrichtung`," \
                       "`Zusammenfassung`) VALUES (%s, %s, %s, %s, %s, " \
                       "%s, %s, %s, %s, %s); "
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()
            sqlMain = "INSERT INTO `Wetter`.`Gesammt` (`Temperatur`,`Zeit`,`Luftfeuchtigkeit`," \
                      "`Windgeschwindigkeit`,`Wolken`, `Regen`, `Schnee`, `Luftdruck`,`Windrichtung`," \
                      " `Zusammenfassung`, `Wetter_Orte_Id`) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s); "
            record2 = (temp, time_sql, humidity, wind_speed, clouds, rain, snow, pressure, wind, general, wetterid)
            my_cursor.execute(sqlMain, record2)
            mydb.commit()
            print(f'Erfolg in der SQL Eingabe für {city}')

        elif city == 'Amsterdam, NLD':
            wetterid = 8
            sqlStuff = "INSERT INTO `Wetter`.`Amsterdam` (`Temperatur`,`Zeit`,`Luftfeuchtigkeit`," \
                       "`Windgeschwindigkeit`,`Wolken`, `Regen`, `Schnee`, `Luftdruck`,`Windrichtung`," \
                       "`Zusammenfassung`) VALUES (%s, %s, %s, %s, %s, " \
                       "%s, %s, %s, %s, %s); "
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()
            sqlMain = "INSERT INTO `Wetter`.`Gesammt` (`Temperatur`,`Zeit`,`Luftfeuchtigkeit`," \
                      "`Windgeschwindigkeit`,`Wolken`, `Regen`, `Schnee`, `Luftdruck`,`Windrichtung`," \
                      " `Zusammenfassung`, `Wetter_Orte_Id`) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s); "
            record2 = (temp, time_sql, humidity, wind_speed, clouds, rain, snow, pressure, wind, general, wetterid)
            my_cursor.execute(sqlMain, record2)
            mydb.commit()
            print(f'Erfolg in der SQL Eingabe für {city}')

        elif city == 'Gent, BEL':
            wetterid = 9
            sqlStuff = "INSERT INTO `Wetter`.`Brüssel` (`Temperatur`,`Zeit`,`Luftfeuchtigkeit`," \
                       "`Windgeschwindigkeit`,`Wolken`, `Regen`, `Schnee`, `Luftdruck`,`Windrichtung`," \
                       "`Zusammenfassung`) VALUES (%s, %s, %s, %s, %s, " \
                       "%s, %s, %s, %s, %s); "
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()
            sqlMain = "INSERT INTO `Wetter`.`Gesammt` (`Temperatur`,`Zeit`,`Luftfeuchtigkeit`," \
                      "`Windgeschwindigkeit`,`Wolken`, `Regen`, `Schnee`, `Luftdruck`,`Windrichtung`," \
                      " `Zusammenfassung`, `Wetter_Orte_Id`) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s); "
            record2 = (temp, time_sql, humidity, wind_speed, clouds, rain, snow, pressure, wind, general, wetterid)
            my_cursor.execute(sqlMain, record2)
            mydb.commit()
            print(f'Erfolg in der SQL Eingabe für {city}')

        elif city == v.städte[0]:
            wetterid = 10
            sqlStuff = v.sqlStuff  # nichts besonderes nur meine Heimat
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()
            sqlMain = "INSERT INTO `Wetter`.`Gesammt` (`Temperatur`,`Zeit`,`Luftfeuchtigkeit`," \
                      "`Windgeschwindigkeit`,`Wolken`, `Regen`, `Schnee`, `Luftdruck`,`Windrichtung`," \
                      " `Zusammenfassung`, `Wetter_Orte_Id`) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s); "
            record2 = (temp, time_sql, humidity, wind_speed, clouds, rain, snow, pressure, wind, general, wetterid)
            my_cursor.execute(sqlMain, record2)
            mydb.commit()
            print(record1)
            print(record2)
            print(f'Erfolg in der SQL Eingabe für {city}')
            mail_body_wind = "Der wind beträgt: " + str(wind_speed) + "km/h " + "es ist " + time.strftime(
                "%H:%M") + "Uhr am " + time.strftime("%d:%m")
            mail_body_rain = "Der Regen beträgt: " + str(rain) + "mm/h " + "es ist " + time.strftime(
                "%H:%M") + "Uhr am " + time.strftime("%d:%m")
        else:
            break


def email_rain():
    mimemsg = MIMEMultipart()
    mimemsg['From'] = mail_from
    mimemsg['To'] = mail_to
    mimemsg['Subject'] = mail_subject_rain
    mimemsg.attach(MIMEText(mail_body_rain, 'plain'))
    connection = smtplib.SMTP(host='mail.gmx.net', port=587)
    connection.starttls()
    connection.login(username, password)
    connection.send_message(mimemsg)
    connection.quit()
    print('Emain regen erfolg')


def email_wind():
    mimemsg = MIMEMultipart()
    mimemsg['From'] = mail_from
    mimemsg['To'] = mail_to
    mimemsg['Subject'] = mail_subject_wind
    mimemsg.attach(MIMEText(mail_body_wind, 'plain'))
    connection = smtplib.SMTP(host='mail.gmx.net', port=587)
    connection.starttls()
    connection.login(username, password)
    connection.send_message(mimemsg)
    connection.quit()
    print('Email wind erfolg')


def emailservice():
    if wind_speed > 40:
        print(email_wind())
        print("Starker Wind")
    else:
        print("Kein Starker Wind")
        print(wind_speed)

    if float(rain.strip()) > 1:
        print(email_rain())
        print("Regen in Sicht")
    else:
        print("Kein Regen in Sicht")
        print(rain)


"""""""""
Zeit Abruf 
"""

while x == 1:
    zeit = time.strftime("%Y-%m-%d %H:%M:%S")
    trigger = time.gmtime()
    print(f'{trigger.tm_hour}:{trigger.tm_min} Uhr')
    if trigger.tm_min % intervall == 0:
        fetching()
        if trigger.tm_min <= 15:         # vereinfachung der Ausdrücke ;-)
            print("Erste Virtelstunde")
        elif 30 >= trigger.tm_min >= 15: # elif trigger.tm_min <= 30 and trigger.tm_min >= 15:
            print("Zweite Virtelstunde")
        elif 45 >= trigger.tm_min >= 30: # elif trigger.tm_min <= 45 and trigger.tm_min >= 30:
            print("Dritte Virtelstunde")
        elif 59 >= trigger.tm_min >= 45: # elif trigger.tm_min <= 59 and trigger.tm_min >= 45:
            print("Letzte Virtelstunde")
        else:
            print("Fehler bei der Zeitbestimmung")
            break
        print(f'Jetzt in der Schutzsleepphase von {schutzsleep} s')
        time.sleep(schutzsleep)
    else:
        print(f'Warten auf nächtes Zeitintervall von {intervall} min')

    time.sleep(zeit_idle)

