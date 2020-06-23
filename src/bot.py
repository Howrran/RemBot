"""
Bot realisation
"""

from uuid import uuid4
from config import BOT_TOKEN
from telegram.ext import Updater, CommandHandler
from doc_manager import DocManager

interval = 10 # interval between the messages in seconds
words = {} # dictionary where key is a word, value is translation
           # word: translation
used_words = [] # list of already used words
def put(update, context):
    """Usage: /put value"""
    # Generate ID and seperate value from command
    key = str(uuid4())
    value = update.message.text.partition(' ')[2]

    # Store value
    context.user_data[key] = value

    update.message.reply_text(key)

def get(update, context):
    """Usage: /get uuid"""
    # Seperate ID from command
    key = update.message.text.partition(' ')[2]

    # Load value
    try:
        value = context.user_data[key]
        update.message.reply_text(value)

    except KeyError:
        update.message.reply_text('Not found')

def update_words_dict(context, update):
    document_id = update.message.text.split('/')
    print(document_id)
    context = DocManager.get_doc_content()
    dictionary = {}
    for word in context.split('\n'):
        if word:
            dictionary[word.split('-')[0].strip()] = word.split('-')[1].strip()

    return dictionary

def callback_alarm(context):
    context.bot.send_message(chat_id=context.job.context, text='Alarm')

def callback_timer(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Starting!')
    context.job_queue.run_repeating(callback_alarm, interval, context=update.message.chat_id)

def stop_timer(context, update):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Stopped!')
    context.job_queue.stop()

def status(context, update):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Active!')

updater = Updater(BOT_TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', callback_timer, pass_job_queue=True))
updater.dispatcher.add_handler(CommandHandler('stop', stop_timer, pass_job_queue=True))
updater.dispatcher.add_handler(CommandHandler('status', status, pass_job_queue=True))

words = update_words_dict()
print(words)
updater.start_polling()




# from telegram.ext import Updater, CommandHandler, MessageHandler,    Filters, InlineQueryHandler
#
#
# def sayhi(bot, job):
#     job.context.message.reply_text("hi")
#
# def time(bot, update,job_queue):
#     job = job_queue.run_repeating(sayhi, 5, context=update)
#
# def main():
#     updater = Updater(BOT_TOKEN)
#     dp = updater.dispatcher
#     dp.add_handler(MessageHandler(Filters.text , time,pass_job_queue=True))
#
#
#     updater.start_polling()
#     updater.idle()
#
# if __name__ == '__main__':
#     main()
#
# bot = telebot.TeleBot(BOT_TOKEN)
#
# words = ['one', 'two', 'three']
# used_words = []
#
# def check_time(last_check, interval = 60):
#     current_time = time.time()
#
# @bot.message_handler(commands=['start', 'help'])
# def send_message(message):
#     bot.reply_to(message, "Hello there")
#
# @bot.message_handler(func=lambda m: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)
#
# bot.polling()
#
