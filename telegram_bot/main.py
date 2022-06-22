# V3 LIVE 17.06.2022
from package import variables
from telegram.ext import *
import responses as R
import time
from datetime import datetime
import os
import mysql.connector
from package import zugang as anbin  # Own Library
from package import sql_zeitvergleich as zeitv
import wetterbot as wetter
from package import bitcoin_preis as btc

now = datetime.now()
date_time = now.strftime("%d/%m/%y, %H:%M:%S")
ort = 'home'
database = 'Wetter'
mydb = mysql.connector.connect(
    host=anbin.host(ort),
    user=anbin.user(ort),
    passwd=anbin.passwd(ort),
    database=anbin.database(database),
    auth_plugin='mysql_native_password')

my_cursor = mydb.cursor()


def start_command(update, context):
    update.message.reply_text('Wähle einen Befehl\n'
                              'Du kannst auch /help eingeben um Weiterzukommen\n')


def help_command(update, context):
    update.message.reply_text('1 Für das Alter des letzten Datensatzes der SQL-Datenbank Wetter\n'
                              '2 Für die Wetterdaten von Heute von Dresden \n'
                              '3 Für den Bitcoin Preis \n')


def handle_message(update, context):
    input_text = str(update.message.text).lower()
    # response = R.sample_response(input_text)
    # update.message.reply_text(response)
    user_message = str(input_text).lower()

    if user_message in ("Zeitabstand", "1"):
        message = zeitv.getZeitabstand()
        update.message.reply_text(f'Der Zeitabstand beträgt:\n hh:mm:ss \n {message}')

    elif user_message in ("Wetter", "2"):
        # weather = [temp, temp_max, temp_min, clouds, general, wind_speed, sunset, rain]
        #            0        1        2        3       4          5          6     7
        weather = wetter.wetter()
        # print(weather)
        update.message.reply_text(f'Die Temperatur beträgt:                   {weather[0]} °C \n'
                                  f'mit einer Höchsttemperatur von: {weather[1]} °C \n'
                                  f'und einer Tiefstemperatur:              {weather[2]} °C. \n'
                                  f'Die Windgeschwindigkeit ist:           {weather[5]} km/h \n'
                                  f'Die Regenmenge beträgt:         {weather[7]} \n'
                                  f'Die Wolkenbedeckung beträgt:        {weather[3]}%\n'
                                  f'General kann man sagen:            {weather[4]}\n'
                                  f'Sonnenuntergang ist:                  {weather[6]}\n')

    elif user_message in ("Bitcoin", "3"):
        update.message.reply_text(f'Bitcoin Preis beträgt {btc.btc()} Euro')
    else:
        update.message.reply_text("Der Befehl wurde falsch eingegeben")


def error(update, context):
    print(f"Update {update} caused error {context.error}")


def main():
    updater = Updater(variables.API, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling(0)
    print("Bot ist gestartet")
    updater.idle()


main()
