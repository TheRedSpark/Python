import logging
from package import variables as v
from telegram import __version__ as TG_VER  # v20
import mysql.connector
from package import variables as v

ort = "home"
database = "Selma"
live = True
results_clen = []
update_version = 1.5
update_message = f'Der Bot updatet auf V{update_version}\n' \
                 f'Bug fixes und Erweiterung der Sicherheit führte dazu das Selma-Benutzer und Pass gelöscht wurden'

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



async def send(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for t_user in results_clen:
        try:
            await context.bot.send_message(t_user, text=update_message)
            print(f'Erfolg für User: {t_user}')
        except:
            print(f'Fehlgeschlagen für User: {t_user}')


def main() -> None:
    application = Application.builder().token(v.telegram_selma_api(live)).build()

    # on different commands - answer in Telegram
    # application.add_handler(CommandHandler(["start", "help", "menu", "setpassw", "setuser", "setemail", "exam"], logging))
    application.add_handler(CommandHandler("send", send))

    # massage handler
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
