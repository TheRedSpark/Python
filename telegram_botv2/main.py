# V4.0 Live 23.06.2022
# credits to https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/echobot.py
import logging
from package import variables as v
from telegram import __version__ as TG_VER  # v20
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
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


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
        data_n = (time_sql, user_id, username, message_chat_id, message_txt, message_id, first_name, last_name, land_code)
        my_cursor.execute(sql_maske, data_n)
        mydb.commit()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_logging(update.effective_user.id, update.effective_user.username, update.effective_message.chat_id,
                 update.effective_message.text_markdown, update.effective_message.id, update.effective_user.first_name,
                 update.effective_user.last_name, update.effective_user.language_code)
    await update.message.reply_text('Benutze /help um diese Nachricht anzuzeigen'
                                    'Benutze /set <Sekunden> um einen Wecker zu stellen\n'
                                    'Benutze /msg <Nachricht> um die Nachricht an den Developer zu schicken\n'
                                    'Schreibe 1 F??r das Alter des letzten Datensatzes der SQL-Datenbank Wetter\n'
                                    'Schreibe 2 F??r die Wetterdaten von Heute von Dresden \n'
                                    'Schreibe 3 F??r den aktuellen Bitcoin Preis \n')


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
        await update.message.reply_text(f'Der Zeitabstand betr??gt:\n hh:mm:ss \n {message}')

    elif user_message in ("wetter", "2"):
        # weather = [temp, temp_max, temp_min, clouds, general, wind_speed, sunset, rain]
        #            0        1        2        3       4          5          6     7
        weather = wetter.wetter()
        # print(weather)
        await update.message.reply_text(f'Die Temperatur betr??gt:                   {weather[0]} ??C \n'
                                        f'mit einer H??chsttemperatur von: {weather[1]} ??C \n'
                                        f'und einer Tiefsttemperatur:              {weather[2]} ??C. \n'
                                        f'Die Windgeschwindigkeit ist:           {weather[5]} km/h \n'
                                        f'Die Regenmenge betr??gt:         {weather[7]} \n l/qm'
                                        f'Die Wolkenbedeckung betr??gt:        {weather[3]}%\n'
                                        f'General kann man sagen:            {weather[4]}\n'
                                        f'Sonnenuntergang ist:                  {weather[6]}\n')

    elif user_message in ("bitcoin", "3"):
        i = 0
        btc_neu = btc.btc()
        if i == 0:
            btc_neu = btc.btc()
            await update.message.reply_text(f'Bitcoin Preis betr??gt {btc.btc()} Euro')
        elif i != 0:
            await update.message.reply_text(
                f'Bitcoin Preis betr??gt {btc.btc()} Euro mit einer Differenz von {btc.btc() - btc_neu} Euro')
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


def main() -> None:
    application = Application.builder().token(v.telegram_api(live)).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("unset", unset))
    application.add_handler(CommandHandler("msg", msg))
    # massage handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
