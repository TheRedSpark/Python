# V4.0 Live 23.06.2022
# credits to https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/echobot.py
import logging
from package import variables as v
from telegram import __version__ as TG_VER, ReplyKeyboardRemove  # v20
import mysql.connector
from package import sql_zeitvergleich as zeitv
import wetterbot as wetter
from package import bitcoin_preis as btc
import time

ort = "home"
database = "Telegram"
live = False

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
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)



def user_logging(user_id, username, message_chat_id, message_txt, message_id, first_name, last_name, land_code):
    if live:
        mydb = mysql.connector.connect(
            host=v.host(ort),
            user=v.user(ort),
            passwd=v.passwd(ort),
            database=v.database(database),
            auth_plugin='mysql_native_password')

        my_cursor = mydb.cursor()
        time_sql = time.strftime("%Y-%m-%d %H:%M:%S")
        sql_maske = "INSERT INTO `Telegram`.`Messages` (`Time`,`User_Id`,`Username`,`Chat_Id`,`Message_Text`," \
                    "`Message_Id`,`First_Name`,`Last_Name`,`Land_Code`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s); "
        data_n = (
            time_sql, user_id, username, message_chat_id, message_txt, message_id, first_name, last_name, land_code)
        my_cursor.execute(sql_maske, data_n)
        mydb.commit()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_logging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                 update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                 update.effective_user.last_name, update.effective_user.language_code)
    await update.message.reply_text('Benutze /help um diese Nachricht anzuzeigen'
                                    'Benutze /set <Sekunden> um einen Wecker zu stellen\n'
                                    'Benutze /msg <Nachricht> um die Nachricht an den Developer zu schicken\n'
                                    'Schreibe 1 Für das Alter des letzten Datensatzes der SQL-Datenbank Wetter\n'
                                    'Schreibe 2 Für die Wetterdaten von Heute von Dresden \n'
                                    'Schreibe 3 Für den aktuellen Bitcoin Preis \n')


async def eingabemenu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [InlineKeyboardButton("", callback_data="")],
        [InlineKeyboardButton("", callback_data="")],
        [InlineKeyboardButton("", callback_data="")],
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



def main() -> None:
    application = Application.builder().token(v.telegram_api(live)).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(["start", "help"], start))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
