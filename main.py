#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Bot for adding words and its translate in database.
"""
import logging, psycopg2
from psycopg2 import sql

from config import TOKEN
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes
from pprint import pprint

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def adding_word(table_name: str, word: str, translate: str) -> str:
    """Add words and its translate in database"""
    
    try:
        conn = psycopg2.connect(dbname='monster_test_base', user='monster_pg', password='pok90RyVal$&', host='127.0.0.1', port='5432')
    except:
        return "Can't establish connection to database"

    cursor = conn.cursor()


    # query = "INSERT INTO {} (word, translate) VALUES (%s, %s)"
    # query = sql.SQL("INSERT INTO {} (word, translate) VALUES (%s, %s)")
    # .format(sql.Identifier(table_name)), (word, translate)
    cursor.execute(
        sql.SQL("INSERT INTO {} (word, translate) VALUES (%s, %s)").format(sql.Identifier(table_name)), 
        (word, translate)
    )
    conn.commit()
    conn.close()

    return "OK"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("IT", callback_data="it"),
            InlineKeyboardButton("Everyday words", callback_data="everyday"),
            InlineKeyboardButton("Idioms", callback_data="idioms"),
            InlineKeyboardButton("Other", callback_data="other")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Choose the theme:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    await context.bot.send_message(query.message.chat.id, "Input word:")
    
    result = adding_word(query.data, 'tel', 'тел')

    await context.bot.send_message(query.message.chat.id, result)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /start to test this bot.")


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
