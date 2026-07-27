import os
import asyncio

from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


async def _send(message: str):
    bot = Bot(TOKEN)
    await bot.send_message(
        chat_id=CHAT_ID,
        text=message
    )


def notify(message: str):
    asyncio.run(_send(message))