#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Bot for adding words and its translate in database.
"""
import logging

from config import TOKEN
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, \
    ConversationHandler, CallbackQueryHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
# set higher logging level for httpx to avoid all
# GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


direction_keyboard = [
    [InlineKeyboardButton("Left",
                          callback_data='left')],
    [InlineKeyboardButton("Forward",
                          callback_data='forward')],
    [InlineKeyboardButton("Right",
                          callback_data='right')],
    [InlineKeyboardButton("I'm so tired",
                          callback_data='tired')]]

left_keyboard = [
    [InlineKeyboardButton("To loose the horse",
                          callback_data='loose_horse')],
    [InlineKeyboardButton("Go back",
                          callback_data='to_stone')]]

forward_keyboard = [
    [InlineKeyboardButton("To stay alive but loose your mind",
                          callback_data='loose_mind')],
    [InlineKeyboardButton("Go back",
                          callback_data='to_stone')]]

right_keyboard = [
    [InlineKeyboardButton("To die",
                          callback_data='death')],
    [InlineKeyboardButton("Go back",
                          callback_data='to_stone')]]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_markup = InlineKeyboardMarkup(direction_keyboard)
    await context.bot.send_message(
                             context._chat_id,
                             "Choose your way",
                             reply_markup=reply_markup)
    return 0


async def tired(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
                             context._chat_id,
                             "Your journey is over")


async def left(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("led")
    query = update.callback_query
    await query.answer()

    await context.bot.send_message(
        context._chat_id,
        "left",
        reply_markup=InlineKeyboardMarkup(left_keyboard))
    return 0


async def forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await context.bot.send_message(
        context._chat_id,
        "forward",
        reply_markup=InlineKeyboardMarkup(forward_keyboard))
    return 0


async def right(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await context.bot.send_message(
        context._chat_id,
        "right",
        reply_markup=InlineKeyboardMarkup(right_keyboard))
    return 0


async def loose_horse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await context.bot.send_message(context._chat_id, "loose horse")


async def loose_mind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await context.bot.send_message(context._chat_id, "loose mind")


async def death(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await context.bot.send_message(context._chat_id, "You are dead")


async def to_stone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    reply_markup = InlineKeyboardMarkup(direction_keyboard)
    await context.bot.send_message(
                             context._chat_id,
                             "Stone welcomes you. Again. Choose your way",
                             reply_markup=reply_markup)

    return ConversationHandler.END


async def wrong(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await context.bot.send_message(context._chat_id,
                                   "Choose correct buttons, bastard!")

left_conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(left, "left")],
    states={0: [CallbackQueryHandler(loose_horse, "loose_horse")]},
    fallbacks=[CallbackQueryHandler(to_stone, "to_stone")]
)

forward_conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(forward, "forward")],
    states={0: [CallbackQueryHandler(loose_mind, "loose_mind")]},
    fallbacks=[CallbackQueryHandler(to_stone, "to_stone")]
)

right_conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(right, "right")],
    states={0: [CallbackQueryHandler(death, "death")]},
    fallbacks=[CallbackQueryHandler(to_stone, "to_stone")]
)

stone_conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={0: [left_conv,
                forward_conv,
                right_conv]},
    fallbacks=[
        # CallbackQueryHandler(exit, "exit")
        CallbackQueryHandler(wrong)
    ]
)


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # application.add_handler(CommandHandler("start", start))
    application.add_handler(stone_conv)
    application.add_handler(CallbackQueryHandler(tired, pattern="tired"))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
