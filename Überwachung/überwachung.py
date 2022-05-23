import time
from SQL_Daten import sql_zeitvergleich as sql
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import variables as v

username = v.username
password = v.password
mail_from = v.mail_from
mail_to = v.mail_to
mail_subject_rain = v.mail_subject_rain
mail_subject_wind = v.mail_subject_wind

a = True
while a == True:
    true = sql.zeitabstand(5,a)
    print(true)
    time.sleep(1)