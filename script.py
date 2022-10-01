import telebot
import logging
import argparse

logging.basicConfig(format="%(asctime)s : %(message)s",
                    level=logging.INFO, datefmt="%H:%M:%S")

parser = argparse.ArgumentParser(description='Argument parser')
parser.add_argument('--token', type=str, help='Telegram token', required=True)
parser.add_argument('--users', nargs='+', help='Whitelisted users', required=True)

args = parser.parse_args()
WHITELIST = list(args.users)
logging.info(WHITELIST)
bot = telebot.TeleBot(args.token, parse_mode=None)
bot.infinity_polling()


def whitelisted(user=None):
    return user in WHITELIST


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    logging.info(message.from_user)
    if whitelisted(message.from_user.username):
        bot.reply_to(message, "Howdy, how are you doing?")
