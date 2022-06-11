import time
import sql_zeitvergleich as sql
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import variables as v
import os

username = v.username
password = v.password
mail_from = v.mail_from
mail_to = v.mail_to
mail_subject_server = v.mail_subject_server
mail_subject_sql = v.mail_subject_sql
mail_subject_offline = v.mail_subject_offline
mail_body_sql = "Test überwachung"
mail_body_server = "TTTT"
mail_body_offline = "Offline"


def ping(host):
    response = os.system("ping -c 1 " + host)
    if response == 0:
        return True
    else:
        return False


def email_sql():
    mimemsg = MIMEMultipart()
    mimemsg['From'] = mail_from
    mimemsg['To'] = mail_to
    mimemsg['Subject'] = mail_subject_sql
    mimemsg.attach(MIMEText(mail_body_sql, 'plain'))
    connection = smtplib.SMTP(host='mail.gmx.net', port=587)
    connection.starttls()
    connection.login(username, password)
    connection.send_message(mimemsg)
    connection.quit()
    print('Emain regen erfolg')


def email_server():
    mimemsg = MIMEMultipart()
    mimemsg['From'] = mail_from
    mimemsg['To'] = mail_to
    mimemsg['Subject'] = mail_subject_server
    mimemsg.attach(MIMEText(mail_body_server, 'plain'))
    connection = smtplib.SMTP(host='mail.gmx.net', port=587)
    connection.starttls()
    connection.login(username, password)
    connection.send_message(mimemsg)
    connection.quit()
    print('Email wind erfolg')


def email_offline():
    mimemsg = MIMEMultipart()
    mimemsg['From'] = mail_from
    mimemsg['To'] = mail_to
    mimemsg['Subject'] = mail_subject_offline
    mimemsg.attach(MIMEText(mail_body_offline, 'plain'))
    connection = smtplib.SMTP(host='mail.gmx.net', port=587)
    connection.starttls()
    connection.login(username, password)
    connection.send_message(mimemsg)
    connection.quit()
    print('Email wind erfolg')


# email_sql()
while True:
    if ping(v.sqladdr):
        if sql.zeitabstand(30, False) == True:
            mail_body_sql = f'Der letzte Datensatz ist {sql.getZeitabstand()} her irgendein Problem muss bestehen'
            email_sql()
            print("Hi")
            time.sleep(30)
        elif sql.zeitabstand(30, False) == False:
            pass
        else:
            print("Fehler")
            sys.exit()
    else:
        email_offline()

    print(sql.getZeitabstand())
    print("Durchlauf")
    time.sleep(3)
