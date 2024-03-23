#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

import logging
import asyncio

from config import TOKEN
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from pprint import pprint

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
    # filename="Test_bot/py_log.log",
    # filemode="w"
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


main_keyboard = [
    [InlineKeyboardButton('Left', callback_data='left'), 
     InlineKeyboardButton('Forward', callback_data='forward'), 
     InlineKeyboardButton('Right', callback_data='right')]
]

reply_markup = InlineKeyboardMarkup(main_keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(context._chat_id, 
        "Choose your way", 
        reply_markup=reply_markup        
)


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
