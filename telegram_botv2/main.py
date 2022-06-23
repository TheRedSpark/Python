import logging
from package import variables
from telegram import __version__ as TG_VER  # v20

import mysql.connector
from package import zugang as anbin  # Own Library
from package import sql_zeitvergleich as zeitv
import wetterbot as wetter
from package import bitcoin_preis as btc

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
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text("Hi! Use /set <seconds> to set a timer\n"
                                    '1 Für das Alter des letzten Datensatzes der SQL-Datenbank Wetter\n'
                                    '2 Für die Wetterdaten von Heute von Dresden \n'
                                    '3 Für den Bitcoin Preis \n')


async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    job = context.job
    await context.bot.send_message(job.chat_id, text=f"Beep! {job.data} seconds are over!")


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = float(context.args[0])
        if due < 0:
            await update.effective_message.reply_text("Sorry we can not go back to future!")
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(alarm, due, chat_id=chat_id, name=str(chat_id), data=due)

        text = "Timer successfully set!"
        if job_removed:
            text += " Old one was removed."
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /set <seconds>")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    # await update.message.reply_text(update.message.text)
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
                                        f'Die Regenmenge beträgt:         {weather[7]} \n'
                                        f'Die Wolkenbedeckung beträgt:        {weather[3]}%\n'
                                        f'General kann man sagen:            {weather[4]}\n'
                                        f'Sonnenuntergang ist:                  {weather[6]}\n')

    elif user_message in ("Bitcoin", "3"):
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
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Timer successfully cancelled!" if job_removed else "You have no active timer."
    await update.message.reply_text(text)


def main() -> None:
    """Run bot."""
    application = Application.builder().token(variables.API).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("unset", unset))
    # massage handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
