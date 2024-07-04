"""
This script creates a Telegram bot that prints the `chat_id` of any group or conversation it is added to.
The `chat_id` is necessary for configuring other bots or services that interact with Telegram.

Functionality:
1. Receives messages in groups or private conversations.
2. Prints the `chat_id` to the console.
3. Responds with the `chat_id` in the chat where the message was received.

Setup:
1. Replace `TOKEN` with your Telegram bot token.
2. Add the bot to a group or send a direct message.
3. Run the script to get and print the `chat_id`.

Dependencies:
- telepot: Library for interacting with the Telegram API. Install using `pip install telepot`.

Execution:
- Run `python BOT_Whats_your_ID.py` in the terminal.
- Add the bot to a group or send a direct message.
- See the `chat_id` printed in the console and received in the response message.
"""

# Import the telepot library to interact with the Telegram API
import telepot
import time

# Replace with your Telegram bot token
TOKEN = ''

# Function to handle incoming messages
def handle(msg):
    # Extract the content type, chat type, and chat_id from the received message
    content_type, chat_type, chat_id = telepot.glance(msg)
    # Print the chat_id to the console
    print(f'chat_id: {chat_id}')
    # Send a message back to the chat with the chat_id
    bot.sendMessage(chat_id, f'The chat_id of this group is: {chat_id}')

# Create an instance of the bot with the provided token
bot = telepot.Bot(TOKEN)
# Set up the bot to call the handle function when a message is received
bot.message_loop(handle)

# Inform that the bot is waiting for messages
print('Waiting for messages...')

# Keep the script running
while True:
    time.sleep(10)
