import os
import logging
from datetime import datetime, timezone
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main_menu():
    keyboard = [
        [InlineKeyboardButton("Convert Timestamp", callback_data="convert")],
        [InlineKeyboardButton("What is Unix Time?", callback_data="learn_unix")],
        [InlineKeyboardButton("Timezone Basics", callback_data="learn_tz")],
        [InlineKeyboardButton("Practice Quiz", callback_data="quiz_start")],
        [InlineKeyboardButton("Help", callback_data="help")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Welcome to Timestamp Converter Bot.\n\n"
        "I help you learn and work with Unix timestamps and date/time handling "
        "in programming.\n\n"
        "What would you like to do?"
    )
    if update.message:
        await update.message.reply_text(text, reply_markup=main_menu())
    else:
        await update.callback_query.edit_message_text(text, reply_markup=main_menu())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "How to use this bot:\n\n"
        "/start - Open main menu\n"
        "/help - Show this message\n"
        "/settings - View bot settings\n\n"
        "You can also send me any Unix timestamp (10-digit number) "
        "and I will convert it to a human-readable date.\n\n"
        "Example: 1710517800"
    )
    if update.message:
        await update.message.reply_text(text, reply_markup=main_menu())
    else:
        await update.callback_query.edit_message_text(text, reply_markup=main_menu())


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Settings\n\n"
        "Timezone: UTC (default)\n"
        "Output format: ISO 8601\n\n"
        "More options coming soon."
    )
    keyboard = [[InlineKeyboardButton("Back to Menu", callback_data="main_menu")]]
    if update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


def convert_timestamp(ts: int) -> str:
    dt_utc = datetime.fromtimestamp(ts, tz=timezone.utc)
    iso = dt_utc.strftime("%Y-%m-%d %H:%M:%S UTC")
    human = dt_utc.strftime("%B %d, %Y at %H:%M:%S UTC")
    return (
        f"Timestamp: {ts}\n\n"
        f"Human-readable: {human}\n"
        f"ISO 8601 format: {iso}\n\n"
        f"Explanation: This timestamp represents the number of seconds "
        f"that have passed since January 1, 1970 (the Unix Epoch). "
        f"In programming, this is used to store dates as integers."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text.isdigit() and len(text) >= 9:
        ts = int(text)
        result = convert_timestamp(ts)
        keyboard = [[InlineKeyboardButton("Back to Menu", callback_data="main_menu")]]
        await update.message.reply_text(result, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(
            "Please send a valid Unix timestamp (a 9 or 10 digit number).\n\n"
            "Example: 1710517800\n\n"
            "Or use the menu to explore.",
            reply_markup=main_menu(),
        )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main_menu":
        await start(update, context)

    elif data == "convert":
        text = (
            "Send me any Unix timestamp and I will convert it.\n\n"
            "Example: 1710517800\n\n"
            "Try it now — just type the number."
        )
        keyboard = [[InlineKeyboardButton("Back to Menu", callback_data="main_menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "learn_unix":
        text = (
            "What is Unix Time?\n\n"
            "Unix time (also called Epoch time or POSIX time) is a system for "
            "describing a point in time as the number of seconds that have "
            "elapsed since 00:00:00 UTC on January 1, 1970.\n\n"
            "Why 1970? It was chosen as a convenient reference point when the "
            "Unix operating system was developed.\n\n"
            "Why is it useful?\n"
            "- It stores dates as simple integers\n"
            "- It is timezone-independent\n"
            "- It is easy to compare and sort\n\n"
            "Example: 0 = January 1, 1970, 00:00:00 UTC\n"
            "Example: 1710517800 = March 15, 2024, 14:30:00 UTC"
        )
        keyboard = [[InlineKeyboardButton("Back to Menu", callback_data="main_menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "learn_tz":
        text = (
            "Timezone Basics\n\n"
            "Unix timestamps are always in UTC (Coordinated Universal Time). "
            "When you display a timestamp to a user, you convert it to their "
            "local timezone.\n\n"
            "In Python:\n"
            "from datetime import datetime, timezone\n"
            "dt = datetime.fromtimestamp(1710517800, tz=timezone.utc)\n\n"
            "In JavaScript:\n"
            "new Date(1710517800 * 1000)\n\n"
            "Common pitfall: JavaScript uses milliseconds, not seconds. "
            "Always multiply by 1000 when working with Unix timestamps in JS."
        )
        keyboard = [[InlineKeyboardButton("Back to Menu", callback_data="main_menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "quiz_start":
        text = "Quiz: What year does Unix time start from?"
        keyboard = [
            [InlineKeyboardButton("1960", callback_data="quiz_wrong")],
            [InlineKeyboardButton("1970", callback_data="quiz_correct")],
            [InlineKeyboardButton("1980", callback_data="quiz_wrong")],
            [InlineKeyboardButton("Back to Menu", callback_data="main_menu")],
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "quiz_correct":
        text = (
            "Correct!\n\n"
            "Unix time starts from January 1, 1970, 00:00:00 UTC. "
            "This is known as the Unix Epoch.\n\n"
            "Fun fact: On January 19, 2038, 32-bit systems will overflow "
            "and reset to 1901. This is called the Year 2038 problem."
        )
        keyboard = [[InlineKeyboardButton("Back to Menu", callback_data="main_menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "quiz_wrong":
        text = (
            "Not quite.\n\n"
            "Unix time starts from January 1, 1970, 00:00:00 UTC. "
            "This is known as the Unix Epoch.\n\n"
            "Try again from the menu."
        )
        keyboard = [[InlineKeyboardButton("Back to Menu", callback_data="main_menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "help":
        await help_command(update, context)


def main():
    if not BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set in environment variables.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("settings", settings_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot is starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
