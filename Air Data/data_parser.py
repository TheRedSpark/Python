import mysql.connector
from package import variables as v
import xml.etree.ElementTree as ET

ort = 'home'
database = 'Air'

GRAD_l = []
GRADC_l = []


def data_uploader_alt(zeit, BEN, DRUCK, FEUCHT, NO, NO2, O3, PM10_As, PM10_BaP, PM10_Cd, PM10_eCT, PM10_HVS, PM10_Ni,
                      PM10_oCT, PM10_Pb,
                      PM10_TEOM, PM25, RUSS_PM1, SO2, STRAHL, TEMP, WINDGE, WINDRI):
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    sql_stuff = "INSERT INTO `Air`.`Dresden-Nord` (`Zeit`,`Benzol`,`Luftdruck`,`relative_Feuchte`,`Stickstoffmonoxid`," \
                "`Stickstoffdioxid`,`Ozon`,`Arsen_im_Feinstaub_PM10`,`Benzo(a)pyren_im_Feinstaub_PM10`," \
                "`Cadmium im_Feinstaub_PM10`,`elementarer_Kohlenstoff_im_Feinstaub_PM10`," \
                "`Feinstaub_PM10_gravimetrisch_bestimmt`,`Nickel_im_Feinstaub_PM10`," \
                "`organischer_Kohlenstoff_im_Feinstaub_PM10`,`Blei_im_Feinstaub_PM10`," \
                "`Feinstaub_PM10_mit_kontinuierlichem_Messverfahren_bestimmt`," \
                "`Feinstaub_PM2.5_gravimetrisch_bestimmt`,`Russ`,`Schwefeldioxid`,`Globalstrahlung`,`Temperatur`," \
                "`Windgeschwindigkeit`,`Windrichtung`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                " %s, %s, %s, %s, %s, %s, %s);"
    record1 = (
        zeit, BEN, DRUCK, FEUCHT, NO, NO2, O3, PM10_As, PM10_BaP, PM10_Cd, PM10_eCT, PM10_HVS, PM10_Ni, PM10_oCT,
        PM10_Pb,
        PM10_TEOM, PM25, RUSS_PM1, SO2, STRAHL, TEMP, WINDGE, WINDRI)
    my_cursor.execute(sql_stuff, record1)
    mydb.commit()


def data_uploader(time, windricchtung):
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    sql_stuff = "INSERT INTO `Air`.`Dresden-Nord` (`Zeit`,`Windrichtung`) VALUES (%s, %s);"
    record1 = (time, windricchtung)
    my_cursor.execute(sql_stuff, record1)
    mydb.commit()
    mydb.close()


mytree = ET.parse('Dresden-Nord.xml')
# mytree = ET.parse('test_dd.xml')
myroot = mytree.getroot()
for x in myroot[0]:
    data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
    time = data[0].split(" ")
    date = time[0].split(".")
    data = [f'20{date[2]}-{date[1]}-{date[0]} {time[1]}:00', data[1]]
    GRAD_l.append(data)

# for x in myroot[1]:
#     data = str(x.attrib).replace("'", "").replace("{datum: ", "").replace(" wert: ", "").replace("}", "").split(",")
#     time = data[0].split(" ")
#     date = time[0].split(".")
#     data = [f'20{date[2]}-{date[1]}-{date[0]} {time[1]}:00', data[1]]
#     GRADC_l.append(data)

# print(GRAD_l)
# print(GRADC_l)
fehlschlag = []
for data in GRAD_l:
    try:
        data_uploader(data[0], data[1])
        print(f'Fertig für {data[0]}')
    except:
        data_uploader(data[0], -1)
        print(f'Fehlschlag für {data[0]}')
        fehlschlag.append(data)

print(fehlschlag)
