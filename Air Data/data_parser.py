import mysql.connector
from package import variables as v

ort = 'home'
database = 'Air'


def data_uploader():
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
                "`Windgeschwindigkeit`,`Windrichtung`) VALUES (%s, %s);"
    record1 = (zeit)
    my_cursor.execute(sql_stuff, record1)
    mydb.commit()
