import asyncio
from telegram import Bot

async def main():
    bot_token = "TOKEN"
    group_id = -123456789  # Group D

    bot = Bot(token=bot_token)
    await bot.leave_chat(chat_id=group_id)

if __name__ == "__main__":
    asyncio.run(main())
