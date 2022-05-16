#V2.0 LIVE 27.03.2022
import konstants as keys
from telegram.ext import *
import responses as R
import time
from datetime import datetime
import os
import mysql.connector
from SQL_Daten import zugang as anbin #Own Library
from SQL_Daten import sql_zeitvergleich as zeitv
import wetterbot as wetter
now = datetime.now()
date_time = now.strftime("%d/%m/%y, %H:%M:%S")
ort = 'lap'
database = 'Wetter'
mydb = mysql.connector.connect(
        host=anbin.host(ort),
        user=anbin.user(ort),
        passwd=anbin.passwd(ort),
        database=anbin.database(database),
        auth_plugin='mysql_native_password')

my_cursor = mydb.cursor()

def start_command(update, context):
    update.message.reply_text('Wähle einen Befehl')

def help_command(update, context):
    update.message.reply_text('1 Für das Alter des letzten Datensatzes der SQL-Datenbank Wetter\n'
                              '2 Für die Wetterdaten von Heute von Dresden \n'
                              '3 Für Test \n')

def handle_message(update, context):
    input_text = str(update.message.text).lower()
    #response = R.sample_response(input_text)
    #update.message.reply_text(response)
    user_message = str(input_text).lower()

    if user_message in ("Zeitabstand", "1"):
        message = zeitv.getZeitabstand()
        update.message.reply_text(f'Der Zeitabstand beträgt:\n hh:mm:ss \n {message}')

    elif user_message in ("tschau", "2"):
        update.message.reply_text(str(wetter.wetter()))

    elif user_message in ("time", "3"):
        update.message.reply_text( str(date_time))

    elif user_message in ("reboot", "4"):
        update.message.reply_text( "reboot")

    elif user_message in ("5"):
        update.message.reply_text("g")

    elif user_message in ("6"):
        update.message.reply_text("Eingabe folgt:")

    else:
     update.message.reply_text( "Der Befehl wurde falsch eingegeben")


def error(update, context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(keys.API, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling(0)
    updater.idle()

main()