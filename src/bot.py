"""
Bot realisation
"""

from src.local_settings import BOT_TOKEN  # pylint: disable= no-name-in-module
from telegram.ext import Updater, CommandHandler  # pylint: disable= import-error
from src.services.user import UserService
from src.services.user_word import UserWordService
from src.services.translate_doc import NewWordsService
from src.services.words import WordService
from random import choice

def add_user(update):
    username = update.message.from_user.username
    telegram_id = update.message.from_user.id

    print(username, telegram_id)

    user = UserService.create(username=username, telegram_id=telegram_id)
    return user

def get_user(update):
    telegram_id = update.message.from_user.id
    user = UserService.filter(telegram_id=telegram_id)[0]
    return user

def start_bot(update, context):
    """
    Add user to the database and start timer job for him

    :param update:
    :param context:
    :return:
    """
    user = add_user(update)
    start_timer(user.interval, update, context)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Starting!')


def stop_bot(update, context):
    """
    Stop updater and all jobs

    :param update:
    :param context:
    :return:
    """
    if update.message.from_user.id != 372481161:
        return

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Bot Stopped!')

    context.job_queue.stop()


def start_timer(interval, update, context):
    """
    Add job_queue that send message to the user
    job is stored in context.chat_data['job']

    :param interval: int | interval in sec
    :param update:
    :param context:
    :return:
    """
    # if user already has timer
    if 'job' in context.chat_data:
        old_job = context.chat_data['job']
        old_job.schedule_removal()

    context.chat_data['user_telegram_id'] = update.message.from_user.id
    new_job = context.job_queue.run_repeating(send_word, interval, context=update.message.chat_id)
    context.chat_data['job'] = new_job


def stop_timer(update, context):
    """
    delete job from user chat data

    :param update:
    :param context:
    :return:
    """

    if 'job' not in context.chat_data:
        update.message.reply_text('You have no active timer')
        return

    job = context.chat_data['job']
    job.schedule_removal()
    del context.chat_data['job']

    update.message.reply_text('Timer successfully unset!')


def send_word(context):
    """
    send message to the user

    :param context:
    :return:
    """
    user_telegram_id= context.job.context #  get user telegram id

    if user := UserService.filter(telegram_id=user_telegram_id):
        user = user[0]
    else:
        return

    words = UserWordService.filter(user_id=user.id, status=True)
    user_word = choice(words)

    word = WordService.get_by_id(user_word.word_id)

    print(word)
    message = f'{word.word} [{word.transcription}] - {word.rus_translation}' \
              f'\n\n{word.explanation}' \
              f'\n\n {word.link}'

    context.bot.send_message(chat_id=context.job.context, text=message)

def add_words(update, context):
    user = get_user(update)
    args = update.message.text.split()
    if len(args) != 2:
        return
    link = args[1]
    print(link)
    words = NewWordsService.add_user_words_from_doc_russian(user.telegram_id, link)
    print(words)# todo count



def status(update, context):
    """Not mine Xd not work for now"""
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Active!')


updater = Updater(BOT_TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start_bot, pass_job_queue=True))
updater.dispatcher.add_handler(CommandHandler('stop', stop_timer, pass_job_queue=True))
updater.dispatcher.add_handler(CommandHandler('stop_bot', stop_bot, pass_job_queue=True))
updater.dispatcher.add_handler(CommandHandler('status', status, pass_job_queue=True))
updater.dispatcher.add_handler(CommandHandler('add_words', add_words, pass_job_queue=True, pass_args=True))

updater.start_polling()
