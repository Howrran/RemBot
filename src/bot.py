"""
Bot realisation
"""

from src.local_settings import BOT_TOKEN  # pylint: disable= no-name-in-module
from telegram.ext import Updater, CommandHandler  # pylint: disable= import-error
from src.services.user import UserService


def send_word(context):
    """
    send message to the user

    :param context:
    :return:
    """
    context.bot.send_message(chat_id=context.job.context, text='TA ZA SHO')


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


def start_bot(update, context):
    """
    Add user to the database and start timer job for him

    :param update:
    :param context:
    :return:
    """

    username = update.message.from_user.username
    telegram_id = update.message.from_user.id

    print(username, telegram_id)

    user = UserService.create(username=username, telegram_id=telegram_id)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Starting!')

    start_timer(user.interval, update, context)

    print(updater.job_queue)

    # context.job_queue.run_repeating(
    #     callback=send_word,
    #     interval=user.interval,
    #     context=update.message.chat_id,
    #     name=user.telegram_id)


def stop_bot(update, context):
    """
    Stop all jobs for all users

    :param update:
    :param context:
    :return:
    """
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Bot Stopped!')

    context.job_queue.stop()


def status(context, update):
    """Not mine Xd not work for now"""
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Active!')


updater = Updater(BOT_TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start_bot, pass_job_queue=True))
updater.dispatcher.add_handler(CommandHandler('stop', stop_timer, pass_job_queue=True))
updater.dispatcher.add_handler(CommandHandler('stop_bot', stop_bot, pass_job_queue=True))
updater.dispatcher.add_handler(CommandHandler('status', status, pass_job_queue=True))

updater.start_polling()
