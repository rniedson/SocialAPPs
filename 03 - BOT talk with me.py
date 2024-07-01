"""
Bot: Motivational Messages

This script creates a Telegram bot that sends motivational messages to a specified chat every 2 minutes. 
It's a simple bot designed to keep you inspired and motivated throughout the day.

Features:
- Sends a random motivational message from a predefined list every 2 minutes.
- Uses the `python-telegram-bot` library for interacting with the Telegram API.
- Utilizes the `schedule` library for timing the messages.
- Asynchronous operation with `asyncio` for efficient performance.

Usage:
1. Replace the TOKEN and CHAT_ID with your bot's token and target chat ID.
2. Run the script.
3. Start the bot with the /start command in the target chat.

Requirements:
- python-telegram-bot
- schedule
- asyncio

Author: Robson Niedson
https://github.com/rniedson/Bots-telegram-Google-Colab-and-others
"""

import logging
import random
import schedule
import asyncio
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Configuration of the bot
TOKEN = 'YOUR_BOT_TOKEN_HERE'
CHAT_ID = 'YOUR_CHAT_ID_HERE'

# List of motivational messages
motivational_messages = [
    "Believe you can and you're halfway there.",
    "You are stronger than you think, more capable than you imagine.",
    "Every day is a new opportunity to improve."
]

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Function to send a message
async def send_message():
    bot = Bot(TOKEN)
    message = random.choice(motivational_messages)
    await bot.send_message(chat_id=CHAT_ID, text=message)

# Scheduling configuration
def schedule_messages():
    schedule.every(2).minutes.do(lambda: asyncio.ensure_future(send_message()))

# Function to start the bot and schedule messages
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Bot started! Motivational messages will be sent every 2 minutes.')

async def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    # Start scheduling messages
    schedule_messages()

    # Run the bot in an asynchronous loop
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    logging.info("Bot started successfully")

    # Keep scheduling running
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
