import telebot
import logging
import argparse
import os
import threading
import time
import subprocess

logging.basicConfig(format="%(asctime)s : %(message)s",
                    level=logging.INFO, datefmt="%H:%M:%S")

parser = argparse.ArgumentParser(description='Argument parser')
parser.add_argument('--token', type=str, help='Telegram token', required=True)
parser.add_argument('--chats', nargs='*', help='Whitelisted chats', default=[])

args = parser.parse_args()
EXECUTION_TIMEOUT = 2.0
WHITELIST = list(args.chats)
logging.info(WHITELIST)
bot = telebot.TeleBot(args.token, parse_mode=None)


def whitelisted(chat_id=None):
    return chat_id in WHITELIST


@bot.message_handler(commands=['start', 'help', 'chatid', 'info'])
def info(message):
    logging.info('/info from {} {}'.format(message.from_user.username, message.chat.id))
    bot.reply_to(message, "ChatID: {}".format(message.chat.id))


@bot.message_handler(commands=['exec'])
def exec(message):
    logging.info('/exec from {} {}'.format(message.from_user.username, message.chat.id))
    if not whitelisted(message.chat.id):
        return

    process = subprocess.run(message.text, shell=True, capture_output=True)
    time.sleep(EXECUTION_TIMEOUT)

    bot.reply_to(message, process.stdout)

if __name__ == '__main__':
    bot.infinity_polling()
