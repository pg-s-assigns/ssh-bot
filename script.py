import telebot
import logging
import argparse
import threading
import time
import subprocess

MAX_TG_MESSAGE_LENGTH = 4096
SLEEP_AFTER_READ = 0.5
OUTPUT_ENCODING = 'UTF-8'

logging.basicConfig(format="%(asctime)s : %(message)s",
                    level=logging.INFO, datefmt="%H:%M:%S")

parser = argparse.ArgumentParser(description='Argument parser')
parser.add_argument('--token', type=str, help='Telegram token', required=True)
parser.add_argument('--chats', nargs='*', help='Whitelisted chats', default=[])

args = parser.parse_args()
WHITELIST = set([int(chat) for chat in args.chats])
logging.info('Whitelisted chats: ' + str(WHITELIST))
bot = telebot.TeleBot(args.token, parse_mode=None)

chat_to_subprocess = dict()


class SubprocessOutputHandler(threading.Thread):
    def __init__(self, chat_id, output_stream):
        super().__init__()
        self.__chat_id = chat_id
        self.__output_stream = output_stream

    def run(self):
        while True:
            readen_output = self.__output_stream.read1(
                MAX_TG_MESSAGE_LENGTH).decode(OUTPUT_ENCODING)
            time.sleep(SLEEP_AFTER_READ)
            bot.send_message(self.__chat_id, readen_output)


class Subprocess:
    def __init__(self, chat_id):
        self.__process = subprocess.Popen(
            ['/bin/sh'], shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.__output_handler = SubprocessOutputHandler(
            chat_id, self.__process.stdout)
        self.__output_handler.start()

    def add_symbols(self, symbols):
        self.__process.stdin.write(bytes(symbols, OUTPUT_ENCODING))
        self.__process.stdin.flush()


def whitelisted(chat_id=None):
    return chat_id in WHITELIST


@bot.message_handler(commands=['start', 'help', 'chatid', 'info'])
def info(message):
    logging.info(
        '/info from {} {}'.format(message.from_user.username, message.chat.id))
    bot.reply_to(message, "ChatID: {}".format(message.chat.id))


@bot.message_handler(commands=['exec'])
def exec(message):
    logging.info(
        '/exec from {} {}'.format(message.from_user.username, message.chat.id))
    if not whitelisted(message.chat.id):
        return

    if message.chat.id not in chat_to_subprocess:
        chat_to_subprocess[message.chat.id] = Subprocess(message.chat.id)

    chat_to_subprocess[message.chat.id].add_symbols(
        message.text[len('/exec '):] + '\n')

@bot.message_handler(commands=['download'])
def download(message):
    logging.info('/download from {} {}'.format(message.from_user.username, message.chat.id))

    if not whitelisted(message.chat.id):
        return

    filename = message.text[len('/download '):]

    with open(filename, 'rb') as misc:
        f = misc.read()

    bot.send_document(message.chat.id, f)


if __name__ == '__main__':
    bot.infinity_polling()
