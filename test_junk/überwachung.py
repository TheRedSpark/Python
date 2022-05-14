import time

import sql_zeitvergleich as sql
a = True
while a == True:
    true = sql.zeitabstand(5,a)
    print(true)
    time.sleep(1)