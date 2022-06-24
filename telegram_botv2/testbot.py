#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
 https://github.com/python-telegram-bot/python-telegram-bot/wiki/InlineKeyboard-Example.
"""
import logging
from package import variables as v
from telegram import __version__ as TG_VER

live = False

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
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Benutze /help um diese Nachricht anzuzeigen'
                                    'Benutze /set <Sekunden> um einen Wecker zu stellen\n'
                                    'Benutze /msg <Nachricht> um die Nachricht an den Developer zu schicken\n'
                                    'Schreibe 1 Für das Alter des letzten Datensatzes der SQL-Datenbank Wetter\n'
                                    'Schreibe 2 Für die Wetterdaten von Heute von Dresden \n'
                                    'Schreibe 3 Für den aktuellen Bitcoin Preis \n')


async def mainmenu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data="m1")],
        [InlineKeyboardButton("Option 2", callback_data="m2")]
        ,
        [InlineKeyboardButton("Option 3", callback_data="m3")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)


async def menu_actions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    if query.data == 'm1':
        # first submenu
        menu_1 = [[InlineKeyboardButton('Submenu 1-1', callback_data='m1_1')],
                  [InlineKeyboardButton('Submenu 1-2', callback_data='m1_2')]]
        reply_markup = InlineKeyboardMarkup(menu_1)
        await query.edit_message_text(text='Choose the option:', reply_markup=reply_markup)

    elif query.data == 'm1_1':
        # second submenu
        # first submenu
        menu_2 = [[InlineKeyboardButton('Submenu 2-1', callback_data='m2_1')],
                  [InlineKeyboardButton('Submenu 2-2', callback_data='m2_2')]]
        reply_markup = InlineKeyboardMarkup(menu_2)
        await query.edit_message_text(text='Choose the option:', reply_markup=reply_markup)

    elif query.data == 'm2_1':
        # second submenu
        # first submenu
        await query.answer("Pl input number")
        zahl = query.data
        print(zahl)

    else:
        await query.edit_message_text(text=f"Selected option: {query.data}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /start to test this bot.")


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(v.telegram_api(live)).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", mainmenu))
    application.add_handler(CallbackQueryHandler(menu_actions))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
