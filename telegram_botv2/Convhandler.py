#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from package import variables as v
import mysql.connector  # 8.0.28
import time

ort = "home"
database = "Main"
live = False
import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters, CallbackQueryHandler,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)


def fragen_getter():
    mydb = mysql.connector.connect(
        host=v.host(ort),
        user=v.user(ort),
        passwd=v.passwd(ort),
        database=v.database(database),
        auth_plugin='mysql_native_password')

    my_cursor = mydb.cursor()
    my_cursor.execute(f"SELECT * FROM Main.Zoll order by rand() limit 1")
    results_raw = my_cursor.fetchone()
    return results_raw


def antwort_setter(antwort, fragen_id):
    if antwort:
        mydb = mysql.connector.connect(
            host=v.host(ort),
            user=v.user(ort),
            passwd=v.passwd(ort),
            database=v.database(database),
            auth_plugin='mysql_native_password')

        my_cursor = mydb.cursor()
        my_cursor.execute(f"SELECT Error_Richtig FROM Main.Zoll WHERE (`idZoll` = {fragen_id})")
        richtige_anzahl = my_cursor.fetchone()
        print(richtige_anzahl)
        richtige_anzahl = int(str(richtige_anzahl).replace("(", "").replace(",)", "")) + 1
        my_cursor.close()

        mydb = mysql.connector.connect(
            host=v.host(ort),
            user=v.user(ort),
            passwd=v.passwd(ort),
            database=v.database(database),
            auth_plugin='mysql_native_password')

        my_cursor = mydb.cursor()
        my_cursor.execute(
            f"UPDATE `Main`.`Zoll` SET `Error_Richtig` = '{richtige_anzahl}' WHERE (`idZoll` = {fragen_id});")
        mydb.commit()
        my_cursor.close()
    else:
        mydb = mysql.connector.connect(
            host=v.host(ort),
            user=v.user(ort),
            passwd=v.passwd(ort),
            database=v.database(database),
            auth_plugin='mysql_native_password')

        my_cursor = mydb.cursor()
        my_cursor.execute(f"SELECT Error_Falsch FROM Main.Zoll WHERE (`idZoll` = {fragen_id})")
        falsche_anzahl = my_cursor.fetchone()
        print(falsche_anzahl)
        falsche_anzahl = int(str(falsche_anzahl).replace("(", "").replace(",)", "")) + 1
        my_cursor.close()

        mydb = mysql.connector.connect(
            host=v.host(ort),
            user=v.user(ort),
            passwd=v.passwd(ort),
            database=v.database(database),
            auth_plugin='mysql_native_password')

        my_cursor = mydb.cursor()
        my_cursor.execute(
            f"UPDATE `Main`.`Zoll` SET `Error_Falsch` = '{falsche_anzahl}' WHERE (`idZoll` = {fragen_id});")
        mydb.commit()
        my_cursor.close()

        mydb = mysql.connector.connect(
            host=v.host(ort),
            user=v.user(ort),
            passwd=v.passwd(ort),
            database=v.database(database),
            auth_plugin='mysql_native_password')

        my_cursor = mydb.cursor()
        my_cursor.execute(f"UPDATE `Main`.`Zoll` SET `Error_Richtig` = 0 WHERE (`idZoll` = {fragen_id});")
        mydb.commit()
        my_cursor.close()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(update.effective_user.id, text=f"Der Selma-Bot sagt herzlich hallo ;-)\n"
                                                                  f"Alle deine persönlichen Daten werden verschlüsselt.\n"
                                                                  f"Du kannst deine Anregungen gerne mit der /msg Funktion teilen.\n")


async def set_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [InlineKeyboardButton("Zoll Start", callback_data="start_zoll")],
        [InlineKeyboardButton("Zoll Stop", callback_data="stop_zoll")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Bitte wählen:", reply_markup=reply_markup)


async def menu_actions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    frage = fragen_getter()
    if query.data == 'start_zoll':

        menu_2 = [[InlineKeyboardButton('Antwort: A', callback_data='antwort_a')],
                  [InlineKeyboardButton('Antwort: B', callback_data='antwort_b')],
                  [InlineKeyboardButton('Antwort: C', callback_data='antwort_c')],
                  [InlineKeyboardButton('Antwort: D', callback_data='antwort_d')],
                  ]
        reply_markup = InlineKeyboardMarkup(menu_2)
        await query.edit_message_text(text=f'{frage[3]}\n\n'
                                           f'a) {frage[4]}\n'
                                           f'b) {frage[5]}\n'
                                           f'c) {frage[6]}\n'
                                           f'd) {frage[7]}', reply_markup=reply_markup)

    elif query.data == 'stop_zoll':
        await query.delete_message()

    elif query.data == 'antwort_a':
        if frage[8] == "a":
            antwort_setter(True, frage[0])
            await context.bot.send_message(update.effective_message.chat_id,
                                           text="Das war die Richtige Antwort!")
        else:
            antwort_setter(False, frage[0])
            await context.bot.send_message(update.effective_message.chat_id,
                                           text=f'Die richtige Antwort war {frage[8]}')
        await query.delete_message()

    elif query.data == 'antwort_b':
        if frage[8] == "b":
            antwort_setter(True, frage[0])
            await context.bot.send_message(update.effective_message.chat_id,
                                           text="Das war die Richtige Antwort!")
        else:
            antwort_setter(False, frage[0])
            await context.bot.send_message(update.effective_message.chat_id,
                                           text=f'Die richtige Antwort war {frage[8]}')
        await query.delete_message()
    elif query.data == 'antwort_c':
        if frage[8] == "c":
            antwort_setter(True, frage[0])
            await context.bot.send_message(update.effective_message.chat_id,
                                           text="Das war die Richtige Antwort!")
        else:
            antwort_setter(False, frage[0])
            await context.bot.send_message(update.effective_message.chat_id,
                                           text=f'Die richtige Antwort war {frage[8]}')
        await query.delete_message()
    elif query.data == 'antwort_d':
        if frage[8] == "d":
            antwort_setter(True, frage[0])
            await context.bot.send_message(update.effective_message.chat_id,
                                           text="Das war die Richtige Antwort!")
        else:
            antwort_setter(False, frage[0])
            await context.bot.send_message(update.effective_message.chat_id,
                                           text=f'Die richtige Antwort war {frage[8]}')
        await query.delete_message()
    else:
        pass
    frage = []


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(v.telegram_api(live)).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("menu", set_menu))
    application.add_handler(CallbackQueryHandler(menu_actions))
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
