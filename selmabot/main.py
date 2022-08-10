# Importing the necessary modules for the bot to work.
import logging
import time

import mysql.connector  # 8.0.28
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, \
    ReplyKeyboardMarkup  # 20.0a1
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, \
    filters, ConversationHandler  # 20.0a1

import crypro_neu as cry  # own
import webgetting as selma  # own
from package import variables as v

# Defining the variables that are used in the program.
version = "V 3.0"  # Live
ort = "home"
database = "Selma"
live = False
loschtimer = 7
stundenabstand_push = 1
day = 0
SETUP, SETUP_BENUTZER, SETUP_PASSWORT, SETUP_PUSH, SETUP_END = range(5)
update_message = f'Der Bot updatet auf {version}\n' \
                 f'Feature: Die Statusmeldung umfasst nun mehr Informationen.' \
                 f'Feature: Nun ist ein Setup möglich ohne Separate Befehle.' \
                 f'Dies ermöglicht nun ein reibungsloses Einrichten vom Bot.\n' \
                 f'Bug fixe:Passwörter und Benutzer werden nicht mehr Leerzeichenabhänig gespeichert. ' \
                 f'werden.\n' \
                 f'Bug fix: /menu wurde für die Handyansicht überarbeitet.'

# Setting up the logging module to log info messages.
if selma.on_server:
    pass
else:
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

"""""""""
Interne Funktionen für die Botverwaltung
"""""


def zugelassen(user_id):
    with mysql.connector.connect(
            host=v.host(ort),
            user=v.user(ort),
            passwd=v.passwd(ort),
            database=v.database(database),
            auth_plugin='mysql_native_password') as mydb:

        my_cursor = mydb.cursor()
        my_cursor.execute(f"SELECT Zugelassen FROM `Selma`.`Users` WHERE User_Id = ({user_id}) ")
        zug = my_cursor.fetchone()
        zug = int(str(zug).replace("(", "").replace(",)", ""))
        if zug == 1:
            return True
        else:
            return False


def userlogging(user_id, username, message_chat_id, message_txt, message_id, first_name, last_name, land_code):
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    time_sql = time.strftime("%Y-%m-%d %H:%M:%S")
    if live:

        sql_maske = "INSERT INTO `Selma`.`Messages` (`Time`,`User_Id`,`Username`,`Chat_Id`,`Message_Text`," \
                    "`Message_Id`,`First_Name`,`Last_Name`,`Land_Code`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s); "
        data_n = (
            time_sql, user_id, username, message_chat_id, message_txt, message_id, first_name, last_name, land_code)
        my_cursor.execute(sql_maske, data_n)
        mydb.commit()
        my_cursor.close()

    else:

        sql_maske = "INSERT INTO `Telegram`.`Messagesbeta` (`Time`,`User_Id`,`Username`,`Chat_Id`,`Message_Text`," \
                    "`Message_Id`,`First_Name`,`Last_Name`,`Land_Code`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s); "
        data_n = (
            time_sql, user_id, username, message_chat_id, message_txt, message_id, first_name, last_name, land_code)
        my_cursor.execute(sql_maske, data_n)
        mydb.commit()
        my_cursor.close()


def user_create(user_id, username):
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    my_cursor.execute(f"SELECT Username_Selma,Password_Selma FROM `Selma`.`Users` WHERE User_Id = ({user_id}) ")
    result = my_cursor.fetchone()
    if result is None:
        sql_maske = "INSERT INTO `Selma`.`Users` (`User_Id`,`Username`) VALUES (%s, %s); "
        data_n = (user_id, username)
        my_cursor.execute(sql_maske, data_n)
        mydb.commit()
    else:
        pass
    my_cursor.close()


def get_username(user_id):
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    my_cursor.execute(f"SELECT Username_Selma FROM `Selma`.`Users` WHERE User_Id = ({user_id}) ")
    enc_username = my_cursor.fetchone()
    my_cursor.close()
    dec_username = cry.decoding(enc_username[0])
    return dec_username


def get_userpass(user_id):
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    my_cursor.execute(f"SELECT Password_Selma FROM `Selma`.`Users` WHERE User_Id = ({user_id}) ")
    enc_userpass = my_cursor.fetchone()
    my_cursor.close()
    dec_userpass = cry.decoding(enc_userpass[0])
    return dec_userpass


def get_user_email(user_id):
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    my_cursor.execute(f"SELECT Email FROM `Selma`.`Users` WHERE User_Id = ({user_id}) ")
    enc_email = my_cursor.fetchone()
    my_cursor.close()
    dec_userpass = cry.decoding(enc_email[0])
    return dec_userpass


def userdel(user_id):
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    my_cursor.execute(
        f"UPDATE `Selma`.`Users` SET `Email` = NULL,`Username_Selma` = NULL,`Password_Selma` = NULL WHERE (`User_Id` = {user_id});")
    mydb.commit()
    my_cursor.close()


def exam_save_toggle(speichern, update):
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    if speichern:
        my_cursor.execute(
            f"UPDATE `Selma`.`Users` SET `Speichern_Prüfungen` = '1' WHERE (`User_Id` = {update.effective_user.id});")
    else:
        my_cursor.execute(
            f"UPDATE `Selma`.`Users` SET `Speichern_Prüfungen` = '0' WHERE (`User_Id` = {update.effective_user.id});")
    mydb.commit()
    my_cursor.close()


def noti_toggle(speichern, update):
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    if speichern:
        my_cursor.execute(
            f"UPDATE `Selma`.`Users` SET `Push_Toggle` = '1' WHERE (`User_Id` = {update});")
    else:
        my_cursor.execute(
            f"UPDATE `Selma`.`Users` SET `Push_Toggle` = '0' WHERE (`User_Id` = {update});")
    mydb.commit()
    my_cursor.close()


def push_updates():
    results_clean = []
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    my_cursor.execute(f"SELECT User_Id FROM `Selma`.`Users` WHERE Push_Toggle = 1 and Push = 1")
    results_raw = my_cursor.fetchall()
    my_cursor.close()
    for raw in results_raw:
        clen = int(str(raw).replace("(", "").replace(",)", "").strip())
        results_clean.append(clen)
    return results_clean


def benutzer_setzer(userid, benutzer):
    try:
        user = cry.encoding(benutzer.strip())
        mydb = mysql.connector.connect(
            host=v.host(ort),
            user=v.user(ort),
            passwd=v.passwd(ort),
            database=v.database(database),
            auth_plugin='mysql_native_password')

        my_cursor = mydb.cursor()
        my_cursor.execute(
            f"UPDATE `Selma`.`Users` SET `Username_Selma` = '{user}' WHERE (`User_Id` = {userid});")
        mydb.commit()
        my_cursor.close()
        return True
    except:
        return False


def passwort_setzer(userid, passwort):
    try:
        passw = cry.encoding(passwort.strip())
        mydb = mysql.connector.connect(
            host=v.host(ort),
            user=v.user(ort),
            passwd=v.passwd(ort),
            database=v.database(database),
            auth_plugin='mysql_native_password')

        my_cursor = mydb.cursor()
        my_cursor.execute(
            f"UPDATE `Selma`.`Users` SET `Password_Selma` = '{passw}' WHERE (`User_Id` = {userid});")
        mydb.commit()
        my_cursor.close()
        return True
    except:
        return False


def email_setzer(userid, email):
    try:
        email = cry.encoding(email)
        mydb = mysql.connector.connect(
            host=v.host(ort),
            user=v.user(ort),
            passwd=v.passwd(ort),
            database=v.database(database),
            auth_plugin='mysql_native_password')

        my_cursor = mydb.cursor()
        my_cursor.execute(f"UPDATE `Selma`.`Users` SET `Email` = '{email}' WHERE (`User_Id` = {userid});")
        mydb.commit()
        mydb.close()
        return True
    except:
        return False


def resetter(userid):
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    my_cursor.execute(
        f"UPDATE `Selma`.`Users` SET `Results_Update` = '0' WHERE (`User_Id` = {userid});")
    my_cursor.execute(
        f"UPDATE `Selma`.`Users` SET `Push` = '0' WHERE (`User_Id` = {userid});")
    my_cursor.execute(
        f"UPDATE `Selma`.`Users` SET `Error_Anmeldung` = '0' WHERE (`User_Id` = {userid});")
    mydb.commit()
    my_cursor.close()


def get_allpush_0():
    results_clean = []
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    my_cursor.execute(f"SELECT User_Id FROM `Selma`.`Users` WHERE Push_Toggle = 1 and Push = 0 and Zugelassen = 1")
    results_raw = my_cursor.fetchall()
    my_cursor.close()
    for raw in results_raw:
        clen = int(str(raw).replace("(", "").replace(",)", "").strip())
        results_clean.append(clen)
    return results_clean


def error_anzahl(user):
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    my_cursor.execute(
        f"SELECT Error_Anmeldung FROM `Selma`.`Users` WHERE User_Id = {user}")
    fehleranzahl = my_cursor.fetchone()
    my_cursor.close()
    fehleranzahl = int(str(fehleranzahl).replace("(", "").replace(",)", ""))
    if fehleranzahl >= 20:
        return True
    else:
        return False


def nachrichten_getter(user):
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    my_cursor.execute(
        f"SELECT COUNT(User_Id) FROM Selma.Messages where User_Id = {user}")
    nachrichten = my_cursor.fetchone()
    my_cursor.close()
    nachrichten = int(str(nachrichten).replace("(", "").replace(",)", ""))
    return nachrichten


def status(user):
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    my_cursor.execute(
        f"SELECT Username,Results_Num,Results_Update,Push_Toggle,Zugelassen,Error_Anmeldung FROM `Selma`.`Users` WHERE User_Id = {user}")
    status = my_cursor.fetchone()
    my_cursor.close()
    print(status)
    if str(status[0]) == "None":
        username = "Nicht vorhanden"
    else:
        username = str(status[0])
    anzahl_prufungen = int(status[1])
    if int(status[2]) == 1:
        neue_ergebnisse = f'Ja'
    else:
        neue_ergebnisse = f'Nein'

    if int(status[3]) == 1:
        push_benach = f'Ja'
    else:
        push_benach = f'Nein'

    if int(status[4]) == 1:
        zuge = f'Ja'
    else:
        zuge = f'Nein'

    if int(status[5]) == 0:
        zuga = f'functional'
    else:
        zuga = f'fehlerhaft'

    error_anmel = int(status[5])

    return [username, anzahl_prufungen, neue_ergebnisse, push_benach, zuge, error_anmel, zuga]


"""""""""
Bot Funktionen
"""


async def send_push(context: ContextTypes.DEFAULT_TYPE) -> None:
    global anzahl_0
    if live:
        anzahl = push_updates()
        for t_user in anzahl:
            try:
                await context.bot.send_message(t_user, text="Du hast neue Prüfungsergebnisse!\n"
                                                            "Benutze im Bot /exam um diese abzurufen und setze mit /reset die Benachrichtigungen zurück!")
                print(f'Update:Erfolg für User: {t_user}')
                await context.bot.send_message(v.telegram_user_id, text=f'Push fertig für {len(anzahl)} User')
            except:
                print(f'Fehlgeschlagen für User: {t_user}')
        trigger = time.gmtime()
        if trigger.tm_hour + 2 == 12:
            anzahl_0 = get_allpush_0()
            for t_user in anzahl_0:
                try:
                    await context.bot.send_message(t_user, text=f'Mahlzeit! Deine tägliche Benachrichtigung:\n'
                                                                f'Leider gibt es keine Neuigkeiten für dich ;-(\n'
                                                                f'Du kannst diese Benachrichtigungen unter\n'
                                                                f' /menu abstellen.\n'
                                                                f'Bei Neuigkeiten wirst du sofort unabhängig von dieser '
                                                                f'Benachrichtigt.\n')
                    print(f'Daily:Erfolg für User: {t_user}')
                except:
                    print(f'Fehlgeschlagen für User: {t_user}')
                if error_anzahl(t_user):
                    try:
                        await context.bot.send_message(t_user,
                                                       text="Du bekommst keine automatischen Updates mehr! Bitte "
                                                            "kontrolliere deine Zugangsdaten und benutze /reset "
                                                            "um wieder Automatische Updates zu erhalten.")

                    except:
                        print(f'Fehlgeschlagen für User: {t_user}')

            await context.bot.send_message(v.telegram_user_id, text=f'Daily: Push fertig für {len(anzahl_0)} User')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    user_create(update.effective_user.id, update.effective_user.username)
    await context.bot.send_message(update.effective_user.id, text=f"Der Selma-Bot sagt herzlich hallo ;-)\n"
                                                                  f"Alle deine persönlichen Daten werden verschlüsselt.\n"
                                                                  f"Du kannst deine Anregungen gerne mit der /msg Funktion teilen.\n"
                                                                  f"Selma Bot {version}")
    await context.bot.send_message(update.effective_user.id,
                                   text=f'Benutze /help um Hilfe mit den Befehlen und der Funktionsweise des Bots zu '
                                        'erhalten. \n'
                                        'Benutze /setup um den Bot für dich einzurichten.\n'
                                        'Unter /menu findest du einige nützliche Funktionen.\n'
                                        'Benutze /update um zu Überprüfen ob neue Prüfungsergebnisse vorliegen.\n'
                                        'Benutze /exam um deine Prüfungsergebnisse abzurufen.\n'
                                        'Benutze /msg <Nachricht> um die Nachricht an die Developer zu schicken.\n'
                                        'Auf Anfrage kann ich dir den Quellcode der aktuellen Version zukommen '
                                        'lassen. ;-)\n')

    if not zugelassen(update.effective_user.id):
        await context.bot.send_message(update.effective_user.id,
                                       text=f'Du bist leider nicht für die Nutzung des Bots berechtigt, du kannst ihn dennoch gerne mit /menu aufsetzen, das steigert deine Möglichkeiten.'
                                            f'Du wirst benachrichtigt, wenn etwas von den begrenzten Kapazitäten frei wird ;-)')


async def update_exam(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    if not zugelassen(update.effective_user.id):
        await context.bot.send_message(update.effective_user.id,
                                       text=f'Du bist leider nicht für die Nutzung des Bots berechtigt, du kannst ihn dennoch gerne mit /menu oder /setup aufsetzen, das steigert deine Möglichkeiten.'
                                            f'Du wirst benachrichtigt, wenn etwas von den begrenzten Kapazitäten frei wird ;-)')
    else:
        await context.bot.send_message(update.effective_user.id,
                                       text="Deine Daten werden aktuell abgerufen bitte warten:")
        exam_data = selma.exam_updater(update.effective_user.id)
        if exam_data is False:
            # print(exam_data)
            await context.bot.send_message(update.effective_user.id,
                                           text="Deine Zugangsdaten sind Fehlerhaft bitte benutze /menu oder /setup um diese zu "
                                                "aktualisieren")
        elif exam_data == 0:
            await context.bot.send_message(update.effective_user.id,
                                           text="Leider gibt es keine neuen Prüfungsergebnisse für dich")
        elif exam_data == 1:
            await context.bot.send_message(update.effective_user.id,
                                           text="Hurrah es gibt neue Ergebnisse nutze /exam um diese abzurufen! \n"
                                                "Und denk dran mit /reset die Benachrichtigungen zurückzusetzen!")
        else:
            await context.bot.send_message(update.effective_user.id,
                                           text="Leider ist etwas schiefgelaufen bitte schreibe dem Developer")


async def set_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [InlineKeyboardButton("Status abrufen", callback_data="status"),
         InlineKeyboardButton("Notification", callback_data="noti"), ],
        [InlineKeyboardButton("Benutzernamen Selma", callback_data="user"),
         InlineKeyboardButton("Passwort Selma", callback_data="passw"), ],
        [InlineKeyboardButton("Daten löschen", callback_data="datadel")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Bitte wählen:", reply_markup=reply_markup)


async def menu_actions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'user':
        menu_2 = [[InlineKeyboardButton('Selma Benutzernamen speichern', callback_data='user_speichern')],
                  [InlineKeyboardButton('Selma Benutzernamen anzeigen', callback_data='user_anzeigen')]]
        reply_markup = InlineKeyboardMarkup(menu_2)
        await query.edit_message_text(text='Deine Daten werden Verschlüsselt gespeichert!', reply_markup=reply_markup)

    elif query.data == 'status':
        user = update.effective_user.id
        status_liste = status(user)
        nachrichten = nachrichten_getter(user)
        benutzer = get_username(user)
        if not benutzer:
            benutzer = "nicht vorhanden"
        userpass = get_userpass(user)
        if not userpass or len(userpass) < 3:
            userpass = "nicht vorhanden"
        else:
            userpass = "vorhanden"
        await query.edit_message_text(text=f'Statusmeldung:\n'
                                           f'Telegram User ID:  ({update.effective_user.id})\n'
                                           f'Username:   ({status_liste[0]})\n'
                                           f'Zugangsdatenstatus:   ({status_liste[6]})\n'
                                           f'Benutzername Selma:  ({benutzer})\n'
                                           f'Passwort Selma:   ({userpass})\n'
                                           f'Anzahl der Prüfungen:   ({status_liste[1]})\n'
                                           f'Neue Ergebnisse:   ({status_liste[2]})\n'
                                           f'Automatische Benachrichtigungen:   ({status_liste[3]})\n'
                                           f'Zugangsberechtigung zum Bot:   ({status_liste[4]})\n'
                                           f'Fehlanmeldungen:   ({status_liste[5]})\n'
                                           f'Nachrichten an den Bot:   ({nachrichten})\n')

    elif query.data == 'user_anzeigen':
        # second submenu
        # first submenu
        if get_username(update.effective_user.id) is None:
            await context.bot.send_message(update.effective_message.chat_id,
                                           text="Du hast noch kein Selma Benutzernamen")
        elif get_username(update.effective_user.id) is False:
            await query.edit_message_text(
                text="Deine Zugangsdaten sind Fehlerhaft bitte benutze /menu um diese zu aktualisieren")

        else:
            await context.bot.send_message(update.effective_message.chat_id,
                                           text=get_username(update.effective_user.id))
            await query.delete_message()

    elif query.data == 'noti':
        # first submenu
        menu_2 = [[InlineKeyboardButton('Push Benachrichtigungen deaktivieren', callback_data='noti_off')],
                  [InlineKeyboardButton('Push Benachrichtigungen aktivieren (Standard)',
                                        callback_data='noti_on')]]
        reply_markup = InlineKeyboardMarkup(menu_2)
        await query.edit_message_text(text='Choose the option:', reply_markup=reply_markup)

    elif query.data == 'noti_on':
        # first submenu
        noti_toggle(True, update.effective_user.id)
        await query.edit_message_text(text='Nun wirst du aktiv benachrichtigt')

    elif query.data == 'noti_off':
        # first submenu
        noti_toggle(False, update.effective_user.id)
        await query.edit_message_text(text='Nun wirst du nicht mehr belästigt')

    elif query.data == 'exam_save':
        # first submenu
        menu_2 = [[InlineKeyboardButton('Deine Prüfungsdaten Speichern', callback_data='exam_save_on')],
                  [InlineKeyboardButton('Deine Prüfungsdaten nicht speichern(Standard)',
                                        callback_data='exam_save_off')]]
        reply_markup = InlineKeyboardMarkup(menu_2)
        await query.edit_message_text(text='Choose the option:', reply_markup=reply_markup)

    elif query.data == 'exam_save_on':
        # first submenu
        exam_save_toggle(True, update)
        await query.edit_message_text(text='Deine Prüfungsergebnisse werden nun gespeichert')

    elif query.data == 'exam_save_off':
        # first submenu
        exam_save_toggle(False, update)
        await query.edit_message_text(text='Deine Prüfungsergebnisse werden nun nicht gespeichert')

    elif query.data == 'passw':
        # first submenu
        menu_2 = [[InlineKeyboardButton('Selma Passwort speichern', callback_data='passw_speichern')],
                  [InlineKeyboardButton('Selma Passwort anzeigen', callback_data='passw_anzeigen')]]
        reply_markup = InlineKeyboardMarkup(menu_2)
        await query.edit_message_text(text='Deine Daten werden verschlüsselt gespeichert!', reply_markup=reply_markup)

    elif query.data == 'passw_anzeigen':
        # second submenu
        # first submenu
        if get_userpass(update.effective_user.id) is None:
            await query.edit_message_text(text="Du hast noch kein Passwort")
        elif get_userpass(update.effective_user.id) is False:
            await query.edit_message_text(
                text="Deine Zugangsdaten sind Fehlerhaft bitte benutze /menu um diese zu aktualisieren")
        else:
            await context.bot.send_message(update.effective_message.chat_id,
                                           text=f"Die nachfolgende Nachricht verschwindet in {loschtimer} sec")
            await query.edit_message_text(text=get_userpass(update.effective_user.id))
            time.sleep(loschtimer)
            await query.delete_message()

    elif query.data == 'passw_speichern':
        await query.edit_message_text(
            text="Bitte nutze den /setpassw PASSWORD Befehl wobei PASSWORD durch dein Selmapassword ersetzt wird")

    elif query.data == 'user_speichern':
        await query.edit_message_text(
            text="Bitte nutze den /setuser BENUTZER Befehl wobei BENUTZER durch deinen Selma-Benutzernamen ersetzt wird")

    elif query.data == 'email_speichern':
        await query.edit_message_text(
            text="Bitte nutze den /setemail EMAIL Befehl wobei EMAIL durch deine Email ersetzt wird")

    elif query.data == 'email':
        # second submenu
        # first submenu
        menu_2 = [[InlineKeyboardButton('Email Speichern', callback_data='email_speichern')],
                  [InlineKeyboardButton('Email Anzeigen', callback_data='email_anzeigen')]]
        reply_markup = InlineKeyboardMarkup(menu_2)
        await query.edit_message_text(text='Deine Daten werden Verschlüsselt gespeichert!', reply_markup=reply_markup)

    elif query.data == 'email_anzeigen':
        # second submenu
        # first submenu
        if get_user_email(update.effective_user.id) is None:
            await query.edit_message_text(text="Du hast noch keine Email")
        elif get_user_email(update.effective_user.id) is False:
            await query.edit_message_text(
                text="Deine Email ist Fehlerhaft bitte benutze /menu um diese zu aktualisieren")
        else:
            await query.edit_message_text(text=get_user_email(update.effective_user.id))

    elif query.data == 'datadel':
        userdel(update.effective_user.id)
        await query.edit_message_text(text="Deine Persönlichen Daten wurden Erfolgreich gelöscht")

    else:
        await query.delete_message()


async def exam(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    if not zugelassen(update.effective_user.id):
        await context.bot.send_message(update.effective_user.id,
                                       text=f'Du bist leider nicht für die Nutzung des Bots berechtigt, du kannst ihn dennoch gerne mit /menu aufsetzen, das steigert deine Möglichkeiten.'
                                            f'Du wirst benachrichtigt, wenn etwas von den begrenzten Kapazitäten frei wird ;-)')
    else:
        await context.bot.send_message(update.effective_user.id,
                                       text="Deine Daten werden aktuell abgerufen bitte warten:")
        exam_data = selma.exam_getter(update.effective_user.id)
        if exam_data is False:
            # print(exam_data)
            await context.bot.send_message(update.effective_user.id,
                                           text="Deine Zugangsdaten sind Fehlerhaft bitte benutze /menu um diese zu "
                                                "aktualisieren")
        else:
            exam_anzahl = int(exam_data.pop())
            i = 0
            while True:
                await context.bot.send_message(update.effective_user.id, text=f'{exam_data.pop(0)}\n'
                                                                              f'{exam_data.pop(0)}\n'
                                                                              f'{exam_data.pop(0)}\n'
                                                                              f'{exam_data.pop(0)}\n'
                                                                              f'{exam_data.pop(0)}')
                i = i + 1
                if exam_anzahl == i:
                    break

            await update.message.reply_text('Deine Ergebnisse')


async def setpassw(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                "/setpassw", update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    passw_raw = str(update.message.text).replace("/setpassw", "").strip()
    if passw_raw == "":
        await update.message.reply_text("Dein Passwort ist leer und kann deshalb nicht gesetzt werden.\n"
                                        "Du benutzt diesen Befehl so:/setpassw DEINPASSWORT")
    else:
        if passwort_setzer(update.effective_user.id, passw_raw) and not passw_raw == "":
            await update.message.reply_text('Dein Passwort wurde erfolgreich gesetzt')
        else:
            await update.message.reply_text('Dein Passwort konnte nicht gesetzt werden')


async def setuser(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                "/setuser", update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    user_raw = str(update.message.text).replace("/setuser", "").strip()
    if user_raw == "":
        await update.message.reply_text("Dein Username ist leer und kann deshalb nicht gesetzt werden.\n"
                                        "Du benutzt diesen Befehl so:/setuser DEINUSERNAME")
    else:
        if benutzer_setzer(update.effective_user.id, user_raw):
            await update.message.reply_text('Dein Benutzername wurde erfolgreich gesetzt')
        else:
            await update.message.reply_text('Dein Benutzername konnte nicht gesetzt werden')


async def set_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                "/setmail", update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    email_raw = str(update.message.text).replace("/setemail", "").strip()
    if email_raw == "":
        await update.message.reply_text("Deine Email ist leer und kann deshalb nicht gesetzt werden.\n"
                                        "Du benutzt diesen Befehl so:/setemail DEINEEMAIL")
    else:
        if email_setzer(update.effective_user.id, email_raw):
            await update.message.reply_text('Deine Email wurde Erfolgreich gesetzt')
        else:
            await update.message.reply_text('Deine Email konnte nicht gesetzt werden')


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    resetter(update.effective_user.id)
    await update.message.reply_text('Reset wurde erfolgreich durchgeführt')


async def msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # The code is sending a message to the developer.
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    chat_id = v.telegram_user_id
    await context.bot.send_message(chat_id,
                                   text=f'User:({update.effective_user.username}) hat dir ({update.message.text.replace("/msg ", "")}) '
                                        f'geschickt!')
    await update.message.reply_text(
        f'Deine Nachricht {update.message.text.replace("/msg ", "")} wurde an den Developer geschickt!')


async def logging(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)

    await update.message.reply_text('Kein Befehl erkannt, bitte nutze einen Befehl unter /help')


async def send(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    results_clen = []
    if update.effective_user.id == v.telegram_user_id:
        mydb = mysql.connector.connect(
            host=v.host(ort),
            user=v.user(ort),
            passwd=v.passwd(ort),
            database=v.database(database),
            auth_plugin='mysql_native_password')

        my_cursor = mydb.cursor()
        my_cursor.execute(f"SELECT User_Id FROM `Selma`.`Users` ")
        results_raw = my_cursor.fetchall()
        my_cursor.close()
        for raw in results_raw:
            clen = int(str(raw).replace("(", "").replace(",)", "").strip())
            results_clen.append(clen)
        for t_user in results_clen:
            try:
                await context.bot.send_message(t_user, text=update_message)
                print(f'Erfolg für User: {t_user}')
            except:
                print(f'Fehlgeschlagen für User: {t_user}')
    else:
        context.bot.send_message(v.telegram_user_id,
                                 text=f'User {update.effective_user.id} hat versucht /send auszuführen')


async def setup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    await update.message.reply_text(
        "Willkommen zum Setup!\n"
        "Du kannst jederzeit mit /cancel abbrechen.\n"
        "Gib als erstes deinen Selma-Benutzernamen an."
    )
    return SETUP_BENUTZER


async def setup_benutzer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    benutzer_setzer(update.effective_user.id, update.message.text.strip())
    await update.message.reply_text(
        "Bitte gib nun dein Passwort für Selma an."
    )
    return SETUP_PASSWORT


async def setup_passwort(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    passwort_setzer(update.effective_user.id, update.message.text.strip())
    reply_keyboard = [["Ja", "Nein"]]

    await update.message.reply_text(
        "Möchtest du automatische Benachrichtigung aktivieren?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Ja oder Nein"
        ),
    )
    return SETUP_PUSH


async def setup_push(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text_b = ""
    desition = update.message.text
    user = int(update.effective_user.id)
    if desition == "Ja":
        noti_toggle(True, user)
        text_b = "sind aktiviert."
    elif desition == "Nein":
        noti_toggle(False, user)
        text_b = "sind deaktiviert."
    else:
        print("Fehlschlag")

    await update.message.reply_text(
        f'Push Benachachrichtigungen per Telegram {text_b}', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


async def setup_end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Willkommen zum Setup du kannst jederzeit mit /cancel abbrechen\n"
        "Gib als erstes deinen Selma-Benutzernamen an",
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    await update.message.reply_text(
        "Du hast das Setup abgebrochen!"
        "Bis zum nächsten mal ;-)", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    # Creating a telegram bot.
    application = Application.builder().token(v.telegram_selma_api(live)).build()

    # Adding the handlers for the commands.
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("msg", msg))
    application.add_handler(CommandHandler("menu", set_menu))
    application.add_handler(CommandHandler("setpassw", setpassw))
    application.add_handler(CommandHandler("reset", reset))
    application.add_handler(CommandHandler("update", update_exam))
    application.add_handler(CommandHandler("setuser", setuser))
    application.add_handler(CommandHandler("setemail", set_email))
    application.add_handler(CommandHandler("exam", exam))
    application.add_handler(CommandHandler("push", send_push))
    application.add_handler(CommandHandler("send", send))

    conv_handler_setup = ConversationHandler(
        entry_points=[CommandHandler("setup", setup)],
        states={
            SETUP: [MessageHandler(filters.TEXT & ~filters.COMMAND, setup)],
            SETUP_BENUTZER: [MessageHandler(filters.TEXT & ~filters.COMMAND, setup_benutzer)],
            SETUP_PASSWORT: [MessageHandler(filters.TEXT & ~filters.COMMAND, setup_passwort)],
            SETUP_PUSH: [MessageHandler(filters.TEXT & ~filters.COMMAND, setup_push)],
            SETUP_END: [MessageHandler(filters.TEXT & ~filters.COMMAND, setup_end)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler_setup)

    application.add_handler(CallbackQueryHandler(menu_actions))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    job_queue = application.job_queue

    # Running the function send_push every 60 seconds * 60 minutes * stundenabstand_push.
    job_queue.run_repeating(send_push, interval=60 * 60 * stundenabstand_push, first=10)

    application.run_polling(1)


print("Main Started")

if __name__ == "__main__":
    main()
