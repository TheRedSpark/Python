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
    my_cursor.execute("INSERT INTO Wetter.Neugersdorf order by Zeit desc limit 1")
    inhalt = my_cursor.fetchall()