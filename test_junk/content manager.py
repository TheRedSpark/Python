import mysql.connector
from package import variables as v

ort_l = "Dresden"
database = "Air"
ort = "home"

with mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password') as mydb:
    my_cursor = mydb.cursor()
    print("Start Tablecreate3")
    my_cursor.execute(f"CREATE TABLE `Air`.`{ort_l}` (`Zeit` DATETIME UNIQUE NOT NULL,`WINDRI` FLOAT NULL,"
                      f"`TEMP` FLOAT NULL,`FEUCHT` FLOAT NULL,`STRAHL` FLOAT NULL,`DRUCK` FLOAT NULL,"
                      f"`WINDGE` FLOAT NULL,`PM10_As` FLOAT NULL,`PM10_BaP` FLOAT NULL,`PM10_Cd` FLOAT NULL,"
                      f"`PM10_Ni` FLOAT NULL,`PM10_Pb` FLOAT NULL,`BEN` FLOAT NULL,`NO` FLOAT NULL,`NO2` FLOAT NULL,"
                      f"`O3` FLOAT NULL,`SO2` FLOAT NULL,`PM10_TEOM` FLOAT NULL,`PM10_HVS` FLOAT NULL,`PM10_eCT` FLOAT NULL,"
                      f"`PM10_oCT` FLOAT NULL,`R_Menge` FLOAT NULL,`PM2.5` FLOAT NULL,`RUSSPM10` FLOAT NULL,`RUSS_PM1` FLOAT NULL,"
                      f"`TOL` FLOAT NULL,`XYL` FLOAT NULL,PRIMARY KEY (`Zeit`),"
                      f"UNIQUE INDEX `Zeit_UNIQUE` (`Zeit` ASC) VISIBLE);")
    print("Start Tablecreate4")
