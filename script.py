import telebot
import logging

logger = logging.Logger(__name__, level=logging.DEBUG)

WHITELIST = []
bot = telebot.TeleBot(
    "", parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    logger.info(message.from_user)

    if message.from_user.username not in WHITELIST:
        return

    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


if __name__ == '__main__':
    bot.infinity_polling()
