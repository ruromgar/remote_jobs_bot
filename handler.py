import telegram
import sys
import os

TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = 000000  # Change this

def send_message(event, context):

    bot = telegram.Bot(token=TOKEN)
    bot.sendMessage(chat_id = CHAT_ID, text = 'Hey there!')
