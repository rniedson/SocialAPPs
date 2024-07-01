# This script implements a simple Telegram bot that responds with the current time when prompted by a user.
# It uses the 'python-telegram-bot' library to interact with the Telegram API and 'nest_asyncio' to enable
# asyncio usage in environments that typically do not support it, such as Google Colab.

# Install the necessary libraries
!pip install python-telegram-bot nest_asyncio

# Import necessary libraries
import nest_asyncio
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime
import logging

# Bot token provided by BotFather
TOKEN = 'your-key'

# Apply patch to allow asyncio usage in Google Colab
nest_asyncio.apply()

# Configure logging for debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to handle the /start command
# When the user sends /start, the bot responds with a welcome message.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Received /start command")
    await update.message.reply_text('Hello! Send /time to know the current time.')

# Function to handle the /time command
# When the user sends /time, the bot responds with the current time.
async def time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Received /time command")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    await update.message.reply_text(f'The current time is {current_time}')

# Main function to set up and run the bot
async def main() -> None:
    logger.info("Initializing the bot")
    app = ApplicationBuilder().token(TOKEN).build()

    # Add handlers for /start and /time commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("time", time))

    logger.info("Starting polling")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    # Keep the bot running
    logger.info("Bot is running, waiting for commands...")
    await asyncio.Future()  # Keep the bot running

# Finalize any previous asyncio instance to avoid conflicts
try:
    loop = asyncio.get_running_loop()
    for task in asyncio.all_tasks(loop):
        task.cancel()
    loop.stop()
    loop.run_forever()
    loop.close()
except:
    pass

logger.info("Running the bot")
# Execute the main function to start the bot
asyncio.run(main())
