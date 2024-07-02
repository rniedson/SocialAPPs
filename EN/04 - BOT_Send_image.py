# Import necessary libraries
import nest_asyncio
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, JobQueue
from datetime import timedelta
import logging
import os

# Apply patch to allow asyncio usage in environments that don't support it natively
nest_asyncio.apply()

# Configure logging for debugging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define the bot token provided by BotFather
TOKEN = '6919153576:AAEZqCdeNsDlhZtSYdmJq9uFycLJe-YoYJM'

# List of image file paths and corresponding messages
image_info = [
    ("1.jpg", "Message for image 1"),
    ("2.jpg", "Message for image 2")
]

# Function to send an image with a message to the group
async def send_image_with_message(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    chat_id = job_data['chat_id']
    image_path, message = job_data['image_info'][job_data['current_index']]
    
    if os.path.exists(image_path):
        await context.bot.send_photo(chat_id=chat_id, photo=open(image_path, 'rb'), caption=message)
    
    # Update index for next image
    job_data['current_index'] = (job_data['current_index'] + 1) % len(job_data['image_info'])

# Function to start the bot and schedule image posts
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id

    # Initial job data
    job_data = {
        'image_info': image_info,
        'current_index': 0,
        'chat_id': chat_id
    }

    # Schedule the job to run every 2 minutes
    interval_minutes = 2  # Change this value to set a different interval
    context.job_queue.run_repeating(send_image_with_message, interval=timedelta(minutes=interval_minutes), first=0, data=job_data)
    await update.message.reply_text('Bot started! Images will be posted every {} minutes.'.format(interval_minutes))

# Main function to configure and run the bot
async def main() -> None:
    logger.info("Setting up the bot")

    # Initialize JobQueue explicitly
    job_queue = JobQueue()

    # Create the application and attach the JobQueue
    app = ApplicationBuilder().token(TOKEN).job_queue(job_queue).build()

    app.add_handler(CommandHandler("start", start))

    logger.info("Initializing the application")
    await app.initialize()

    logger.info("Starting the application")
    await app.start()

    # Start the JobQueue
    await job_queue.start()

    logger.info("Starting polling")
    await app.updater.start_polling()

    logger.info("Bot is running, waiting for commands...")
    await asyncio.Future()

# Finalize any previous asyncio instance
try:
    loop = asyncio.get_running_loop()
    for task in asyncio.all_tasks(loop):
        task.cancel()
    loop.stop()
    loop.run_forever()
    loop.close()
except:
    pass

# Debug log before running the bot
logger.info("Running the bot")

# Execute the main function to start the bot
asyncio.run(main())
