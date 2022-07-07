version = "V1.4"  # Live
import logging
from package import variables as v
from telegram import __version__ as TG_VER  # v20
import mysql.connector
import webgetting as selma
import time


ort = "home"
database = "Selma"
live = False
loschtimer = 5

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"Dieses Beispiel ist nicht kompatibel mit deiner PTB version {TG_VER}."
        f"{TG_VER} version von diesem Beispiel, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


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

    else:

        sql_maske = "INSERT INTO `Telegram`.`Messagesbeta` (`Time`,`User_Id`,`Username`,`Chat_Id`,`Message_Text`," \
                    "`Message_Id`,`First_Name`,`Last_Name`,`Land_Code`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s); "
        data_n = (
            time_sql, user_id, username, message_chat_id, message_txt, message_id, first_name, last_name, land_code)
        my_cursor.execute(sql_maske, data_n)
        mydb.commit()
        my_cursor.close()


def usercreate(user_id, username):
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    time_sql = time.strftime("%Y-%m-%d %H:%M:%S")
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
    result = my_cursor.fetchone()
    my_cursor.close()
    return result[0]


def get_userpass(user_id):
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    my_cursor.execute(f"SELECT Password_Selma FROM `Selma`.`Users` WHERE User_Id = ({user_id}) ")
    result = my_cursor.fetchone()
    my_cursor.close()
    return result[0]


def get_user_email(user_id):
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    my_cursor.execute(f"SELECT Email FROM `Selma`.`Users` WHERE User_Id = ({user_id}) ")
    result = my_cursor.fetchone()
    my_cursor.close()
    return result[0]


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


def push_updates():
    results_clean = []
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    my_cursor.execute(f"SELECT User_Id FROM `Selma`.`Users` WHERE Push = 1 ")
    results_raw = my_cursor.fetchall()
    my_cursor.close()
    for raw in results_raw:
        clen = int(str(raw).replace("(", "").replace(",)", "").strip())
        results_clean.append(clen)
        mydb = mysql.connector.connect(
            host=v.host(ort),
            user=v.user(ort),
            passwd=v.passwd(ort),
            database=v.database(database),
            auth_plugin='mysql_native_password')

        my_cursor = mydb.cursor()
        my_cursor.execute(
            f"UPDATE `Selma`.`Users` SET `Push` = 0 WHERE (`User_Id` = {clen});")
        mydb.commit()
        my_cursor.close()
    return results_clean


async def send_push(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("send push")
    anzahl = push_updates()
    print(anzahl)
    for t_user in anzahl:
        try:
            await context.bot.send_message(t_user, text="Du Hast neue Prüfungsergebnisse!\n"
                                                        "Benutze im Bot /exam um diese abzurufen und setze mit /reset die Benachrichtigungen zurück!")
            print(f'Erfolg für User: {t_user}')
        except:
            print(f'Fehlgeschlagen für User: {t_user}')
    await context.bot.send_message(v.telegram_user_id,text=f'Push fertig für {len(anzahl)}')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    usercreate(update.effective_user.id, update.effective_user.username)
    await context.bot.send_message(update.effective_user.id, text=f"Der Selma-Bot sagt herzlich hallo ;-)\n"
                                                                  f"Bei Problemen Bugs oder Anmerkungen gerne die Msg Funktion benutzen\n"
                                                                  f"Selma Bot Version {version}")
    await update.message.reply_text('Benutze /help um Hilfe mit den Befehlen und der Funktionsweise des Bots zu '
                                    'erhalten. \n'
                                    'Benutze /menu um den Bot aufzusetzen oder um deine Daten zu löschen\n'
                                    'Benutze /update um zu Überprüfen ob neue Prüfungsergebnisse Vorliegen'
                                    'Benutze /exam um deine Prüfungsergebnisse abzurufen\n'
                                    'Benutze /msg <Nachricht> um die Nachricht an die Developer zu schicken\n')


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    await update.message.reply_text('Benutze /help um Hilfe mit den Befehlen und der Funktionsweise des Bots zu '
                                    'erhalten. \n'
                                    'Benutze /menu um den Bot aufzusetzen oder um deine Daten zu löschen\n'
                                    'Benutze /exam um deine Prüfungsergebnisse abzurufen\n'
                                    'Benutze /msg <Nachricht> um die Nachricht an die Developer zu schicken\n')


async def update_exam(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    await context.bot.send_message(update.effective_user.id, text="Deine Daten werden aktuell Abgerufen bitte warten:")
    exam_data = selma.exam_updater(update.effective_user.id)
    print(exam_data)
    if exam_data is False:
        # print(exam_data)
        await context.bot.send_message(update.effective_user.id,
                                       text="Deine Zugangsdaten sind Fehlerhaft bitte benutze /menu um diese zu aktualisiren")
    elif exam_data == 0:
        await context.bot.send_message(update.effective_user.id,
                                       text="Leider gibt es keine neuen Prüfungsergebnisse für dich")
    elif exam_data == 1:
        await context.bot.send_message(update.effective_user.id,
                                       text="Hurrah es gibt neue Ergebnisse nutze /exam um diese abzurufen! \n"
                                            "Und denk dran mit /reset um die Benachrichtigungen zurückzusetzen!")
    else:
        await context.bot.send_message(update.effective_user.id,
                                       text="Leider ist etwas schiefgelaufen bitte schreibe dem Developer")


async def setmenu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [InlineKeyboardButton("Benutzernamen Selma", callback_data="user")],
        [InlineKeyboardButton("Passwort Selma", callback_data="passw")],
        [InlineKeyboardButton("Email", callback_data="email")],
        [InlineKeyboardButton("Daten löschen", callback_data="datadel")],
        [InlineKeyboardButton("Ergebnisspeicherung", callback_data="exam_save")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Bitte wählen:", reply_markup=reply_markup)


async def menu_actions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    await query.answer()

    if query.data == 'user':
        # first submenu
        menu_2 = [[InlineKeyboardButton('Selma Benutzernamen speichern', callback_data='user_speichern')],
                  [InlineKeyboardButton('Selma Benutzernamen anzeigen', callback_data='user_anzeigen')]]
        reply_markup = InlineKeyboardMarkup(menu_2)
        await query.edit_message_text(text='Choose the option:', reply_markup=reply_markup)

    elif query.data == 'user_anzeigen':
        # second submenu
        # first submenu
        if get_username(update.effective_user.id) is None:
            await context.bot.send_message(update.effective_message.chat_id,
                                           text="Du hast noch kein Selma Benutzernamen")
        else:
            await context.bot.send_message(update.effective_message.chat_id,
                                           text=get_username(update.effective_user.id))
        await query.delete_message()

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
        await query.edit_message_text(text='Choose the option:', reply_markup=reply_markup)

    elif query.data == 'passw_anzeigen':
        # second submenu
        # first submenu
        if get_userpass(update.effective_user.id) is None:
            await query.edit_message_text(text="Du hast noch kein Passwort")
        else:
            await context.bot.send_message(update.effective_message.chat_id,
                                           text=f"Die nachfolgende Nachricht verschindet in {loschtimer} sec")
            await query.edit_message_text(text=get_userpass(update.effective_user.id))
            time.sleep(loschtimer)
        await query.delete_message()

    elif query.data == 'passw_speichern':
        await query.edit_message_text(
            text="Bitte nutze den /setpassw PASSWORD Befehl wobei PASSWORD durch dein Selmapassword ersetzt wird")

    elif query.data == 'user_speichern':
        await query.edit_message_text(
            text="Bitte nutze den /setuser BENUTZER Befehl wobei BENUTZER durch dein Selma-Benutzernamen ersetzt wird")

    elif query.data == 'email_speichern':
        await query.edit_message_text(
            text="Bitte nutze den /setemail EMAIL Befehl wobei EMAIL durch deie Email ersetzt wird")




    elif query.data == 'email':
        # second submenu
        # first submenu
        menu_2 = [[InlineKeyboardButton('Email Speichern', callback_data='email_speichern')],
                  [InlineKeyboardButton('Email Anzeigen', callback_data='email_anzeigen')]]
        reply_markup = InlineKeyboardMarkup(menu_2)
        await query.edit_message_text(text='Choose the option:', reply_markup=reply_markup)

    elif query.data == 'email_anzeigen':
        # second submenu
        # first submenu
        if get_user_email(update.effective_user.id) is None:
            await query.edit_message_text(text="Du hast noch keine Email")
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
    await context.bot.send_message(update.effective_user.id, text="Deine Daten werden aktuell Abgerufen bitte warten:")
    exam_data = []
    exam_data = selma.exam_getter(update.effective_user.id)
    if exam_data is False:
        # print(exam_data)
        await context.bot.send_message(update.effective_user.id,
                                       text="Deine Zugangsdaten sind Fehlerhaft bitte benutze /menu um diese zu aktualisiren")
    else:
        exam_anzahl = 0
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
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    passw = str(update.message.text).replace("/setpassw", "").strip()
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    my_cursor.execute(
        f"UPDATE `Selma`.`Users` SET `Password_Selma` = '{passw}' WHERE (`User_Id` = {update.effective_user.id});")
    mydb.commit()
    my_cursor.close()
    await update.message.reply_text('Dein Password wurde Erfolgreich gesetzt')


async def setuser(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    user = str(update.message.text).replace("/setuser", "").strip()
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    my_cursor.execute(
        f"UPDATE `Selma`.`Users` SET `Username_Selma` = '{user}' WHERE (`User_Id` = {update.effective_user.id});")
    mydb.commit()
    my_cursor.close()
    await update.message.reply_text('Dein Benutzername wurde Erfolgreich gesetzt')


async def setemail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    email = str(update.message.text).replace("/setemail", "").strip()
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    my_cursor.execute(f"UPDATE `Selma`.`Users` SET `Email` = '{email}' WHERE (`User_Id` = {update.effective_user.id});")
    mydb.commit()
    my_cursor.close()
    await update.message.reply_text('Deine Email wurde Erfolgreich gesetzt')


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userlogging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.language_code)
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    my_cursor.execute(
        f"UPDATE `Selma`.`Users` SET `Results_Update` = '0' WHERE (`User_Id` = {update.effective_user.id});")
    mydb.commit()
    my_cursor.close()
    await update.message.reply_text('Reset wurde erfolgreich Durchgeführt')


async def msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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


def main() -> None:
    application = Application.builder().token(v.telegram_selma_api(live)).build()

    # on different commands - answer in Telegram
    # application.add_handler(CommandHandler(["start", "help", "menu", "setpassw", "setuser", "setemail", "exam"], logging))
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("msg", msg))
    application.add_handler(CommandHandler("menu", setmenu))
    application.add_handler(CommandHandler("setpassw", setpassw))
    application.add_handler(CommandHandler("reset", reset))
    application.add_handler(CommandHandler("update", update_exam))
    application.add_handler(CommandHandler("setuser", setuser))
    application.add_handler(CommandHandler("setemail", setemail))
    application.add_handler(CommandHandler("exam", exam))
    application.add_handler(CommandHandler("push", send_push))
    application.add_handler(CallbackQueryHandler(menu_actions))

    # massage handler
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
