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
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
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


async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.send_message(job.chat_id, text=f"Beep! {job.data} Sekunden sind vorbei!")


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id

    user_logging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                 update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                 update.effective_user.last_name, update.effective_user.language_code)

    try:
        # args[0] should contain the time for the timer in seconds
        due = float(context.args[0])
        if due < 0:
            await update.effective_message.reply_text("Sorry we can not go back to future!")
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(alarm, due, chat_id=chat_id, name=str(chat_id), data=due)
        context.job_queue.run_daily()
        text = "Timer successfully set!"
        if job_removed:
            text += " Old one was removed."
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /set <seconds>")


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # await update.message.reply_text(update.message.text)
    user_logging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                 update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                 update.effective_user.last_name, update.effective_user.language_code)
    user_message = str(update.message.text).lower()

    if user_message in ("zeitabstand", "1"):
        message = zeitv.getZeitabstand()
        # A f-string. It is a new way to format strings in Python.
        await update.message.reply_text(f'Der Zeitabstand beträgt:\n hh:mm:ss \n {message}')

    elif user_message in ("wetter", "2"):
        # weather = [temp, temp_max, temp_min, clouds, general, wind_speed, sunset, rain]
        #            0        1        2        3       4          5          6     7
        weather = wetter.wetter()
        # print(weather)
        await update.message.reply_text(f'Die Temperatur beträgt:                   {weather[0]} °C \n'
                                        f'mit einer Höchsttemperatur von: {weather[1]} °C \n'
                                        f'und einer Tiefsttemperatur:              {weather[2]} °C. \n'
                                        f'Die Windgeschwindigkeit ist:           {weather[5]} km/h \n'
                                        f'Die Regenmenge beträgt:         {weather[7]} \n l/qm'
                                        f'Die Wolkenbedeckung beträgt:        {weather[3]}%\n'
                                        f'General kann man sagen:            {weather[4]}\n'
                                        f'Sonnenuntergang ist:                  {weather[6]}\n')

    elif user_message in ("bitcoin", "3"):
        i = 0
        btc_neu = btc.btc()
        if i == 0:
            btc_neu = btc.btc()
            await update.message.reply_text(f'Bitcoin Preis beträgt {btc.btc()} Euro')
        elif i != 0:
            await update.message.reply_text(
                f'Bitcoin Preis beträgt {btc.btc()} Euro mit einer Differenz von {btc.btc() - btc_neu} Euro')
            btc_neu = btc.btc()
        else:
            pass
    else:
        await update.message.reply_text("Der Befehl wurde falsch eingegeben")


async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Wecker erfolgreich abgebrochen!" if job_removed else "Du hast keinen aktiven Wecker."
    await update.message.reply_text(text)


async def msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_logging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                 update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                 update.effective_user.last_name, update.effective_user.language_code)
    chat_id = v.telegram_user_id
    await context.bot.send_message(chat_id,
                                   text=f'User:({update.effective_user.username}) hat dir ({update.message.text.replace("/msg ", "")}) '
                                        f'geschickt!')
    await update.message.reply_text(
        f'Deine Nachricht {update.message.text.replace("/msg ", "")} wurde an den Developer geschickt!')


async def zoll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["Boy", "Girl", "Other"]]

    await update.message.reply_text(
        "Hi! My name is Professor Bot. I will hold a conversation with you. "
        "Send /cancel to stop talking to me.\n\n"
        "Are you a boy or a girl?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Boy or Girl?"
        ),
    )

    return GENDER


async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "I see! Please send me a photo of yourself, "
        "so I know what you look like, or send /skip if you don't want to.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHOTO


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download("user_photo.jpg")
    logger.info("Photo of %s: %s", user.first_name, "user_photo.jpg")
    await update.message.reply_text(
        "Gorgeous! Now, send me your location please, or send /skip if you don't want to."
    )

    return LOCATION


async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the photo and asks for a location."""
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    await update.message.reply_text(
        "I bet you look great! Now, send me your location please, or send /skip."
    )

    return LOCATION


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the location and asks for some info about the user."""
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    await update.message.reply_text(
        "Maybe I can visit you sometime! At last, tell me something about yourself."
    )

    return BIO


async def skip_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the location and asks for info about the user."""
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    await update.message.reply_text(
        "You seem a bit paranoid! At last, tell me something about yourself."
    )

    return BIO


async def bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text("Thank you! I hope we can talk again some day.")

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    application = Application.builder().token(v.telegram_api(live)).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("unset", unset))
    application.add_handler(CommandHandler("msg", msg))
    # massage handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("zoll", zoll)],
        states={
            GENDER: [MessageHandler(filters.Regex("^(Boy|Girl|Other)$"), gender)],
            PHOTO: [MessageHandler(filters.PHOTO, photo), CommandHandler("skip", skip_photo)],
            LOCATION: [
                MessageHandler(filters.LOCATION, location),
                CommandHandler("skip", skip_location),
            ],
            BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
