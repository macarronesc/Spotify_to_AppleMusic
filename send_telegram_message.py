from telegram import Bot
import asyncio
import sys
import os

# Spotify to Apple Music bot
TELEGRAM_API_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN') 
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID') 

async def send_to_telegram(message):
    # Initialize the Telegram bot
    bot = Bot(token=TELEGRAM_API_TOKEN)

    # Send a message to the specified Telegram chat
    await bot.send_message(chat_id=CHAT_ID, text=message)