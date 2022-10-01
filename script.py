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
parser.add_argument('--users', nargs='+', help='Whitelisted users', required=True)

args = parser.parse_args()
EXECUTION_TIMEOUT = 2.0
WHITELIST = list(args.users)
logging.info(WHITELIST)
bot = telebot.TeleBot(args.token, parse_mode=None)


def whitelisted(user=None):
    return user in WHITELIST


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    logging.info(message.from_user)
    if whitelisted(message.from_user.username):
        bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda _: True)
def execute_command(message):
    logging.info(message.from_user)
    if not whitelisted(message.from_user.username):
        return

    process = subprocess.run(message.text, shell=True, capture_output=True)
    time.sleep(EXECUTION_TIMEOUT)

    bot.reply_to(message, process.stdout)

if __name__ == '__main__':
    bot.infinity_polling()
