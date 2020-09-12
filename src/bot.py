"""
Bot realisation
"""
# TODO add language settigns
# TODO add custom translate in user_words
# TODO add pick random word from db function
from telegram.ext import Updater, CommandHandler  # pylint: disable= import-error
from telegram.ext.dispatcher import run_async

from src.local_settings import BOT_TOKEN  # pylint: disable= no-name-in-module
from src.services.translate_doc import NewWordsService
from src.services.user import UserService
from src.services.user_word import UserWordService
from src.utils.validators import Validator


def add_user(update):
    """
    add new user to db or return if exist

    :param update:
    :return:
    """
    username = update.message.from_user.username
    telegram_id = update.message.from_user.id

    print(username, telegram_id)

    user = UserService.create(username=username, telegram_id=telegram_id)
    return user


def get_user(update):
    """
    Get user by user`s message

    :param update:
    :return:
    """
    if update.message is None:
        return None
    telegram_id = update.message.from_user.id
    user = UserService.filter(telegram_id=telegram_id)[0]
    return user


@run_async
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


@run_async
def stop_bot(update, context):
    """
    Stop updater and all jobs

    :param update:
    :param context:
    :return:
    """
    if update.message.from_user.id != 372481161:  # admin`s id
        return

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Bot Stopped!')

    context.job_queue.stop()


@run_async
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


@run_async
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


@run_async
def send_word(context):
    """
    send message to the user

    :param context:
    :return:
    """
    user_telegram_id = context.job.context  # get user telegram id
    word = UserWordService.get_user_word(user_telegram_id)
    message = get_message(user_telegram_id, word)

    context.bot.send_message(chat_id=context.job.context, text=message)


@run_async
def add_words(update, context):  # pylint: disable=unused-argument
    """
    Add new words to DB and link them to user

    args: /add_words link_to_google_doc

    :param update:
    :param context:
    :return:
    """
    user = get_user(update)
    if user is None:
        return None

    link = get_arg(update)
    if link is None:
        return None

    if not Validator.google_doc_validator(link):
        update.message.reply_text('Invalid Link')

    update.message.reply_text('Adding words...\nThis process may take a while')
    words = NewWordsService.add_user_words_from_doc(user.telegram_id, link)

    if not words:
        update.message.reply_text('Something went wrong...')
        return None

    success_list = [word for word in words if words[word]]
    fail_list = [word for word in words if not words[word]]  # list of words that was not added to db

    print_result(update, success_list, fail_list)

    return True


def add_single_word(update, context):  # pylint: disable=unused-argument
    """
    Add new word to db and link it to user

    :param update:
    :param context:
    :return:
    """
    user = get_user(update)
    if user is None:
        return None

    word = get_arg(update)
    if word is None:
        return None

    if word.startswith('http'):
        return None

    new_word = NewWordsService.add_single_word(user.telegram_id, word)
    message = "Word has been added!" if new_word else "Error, word hasn`t been added"
    update.message.reply_text(message)
    return new_word


def status(update, context):
    """Not mine, not work for now"""
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Active!')


def print_result(update, success_list, fail_list):
    """
    Print result of add_words function

    :param update:
    :param success_list: list of words which were added to db
    :param fail_list: list of words which were not added to db
    :return:
    """
    fail = '; '.join(fail_list)
    success = '; '.join(success_list)

    if success_list and fail_list:
        update.message.reply_text('Operation success. Following words have been added:')
        update.message.reply_text(f'_{success}_',
                                  parse_mode="Markdown")
        update.message.reply_text('But the following words haven`t been added:')
        update.message.reply_text(f'_{fail}_', parse_mode="Markdown")
    elif success_list and not fail_list:
        update.message.reply_text('Operation success. All words have been added')
        update.message.reply_text(f'_{success}_',
                                  parse_mode="Markdown")
    elif not success_list and fail_list:
        update.message.reply_text('Operation Failed. All words have not been added')
        update.message.reply_text(f'_{fail}_',
                                  parse_mode="Markdown")
    else:
        update.message.reply_text('Why is it blank?')


def change_interval(update, context):
    """
    Change users word sending interval

    :param update:
    :param context:
    :return:
    """
    user = get_user(update)
    if user is None:
        return None
    new_interval = get_arg(update)
    if new_interval is None:
        return None

    if not Validator.interval_validator(new_interval):
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text='Invalid Interval\nInterval must be in range 1 < interval < 86 400')
        return None

    user = UserService.update(user_id=user.id, interval=new_interval)
    if user:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f'Interval changed successfully!\nNew interval is {new_interval} seconds.')
        return True
    return None


def change_language(update, context):
    """
    Change users language

    :param update:
    :param context:
    :return:
    """
    user = get_user(update)
    if user is None:
        return None

    new_language = get_arg(update)

    if new_language is None:
        return None

    if not Validator.language_validator(new_language):
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text='Invalid Language\nSupported languages: Ukrainian(ukr), Russian(rus)')
        return None

    user = UserService.update(user_id=user.id, language=new_language)
    if user:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f'Language changed successfully!\nNew Language is {new_language}.')
        return True
    return None

def reset_user_words(update, context):
    """
    Change all user word status to unused

    :param update:
    :param context:
    :return:
    """
    user_telegram_id = update.message.from_user.id
    response = UserWordService.reset_user_words(user_telegram_id)

    if response:
        message = 'All words successfully reset!'
    else:
        message = 'Something went wrong'

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=message)


def get_message(user_telegram_id, word):
    """
    get message for send word
    depends on user language

    :param user_telegram_id:
    :param word:
    :return:
    """
    user = UserService.filter(telegram_id=user_telegram_id)
    if user:
        user = user[0]
    else:
        return None

    if word and user.language == 'ukr':
        message = f'{word.word} [{word.transcription}] - {word.ukr_translation}' \
                  f'\n\n{word.explanation}' \
                  f'\n\n {word.link}'
    elif word and user.language == 'rus':
        message = f'{word.word} [{word.transcription}] - {word.rus_translation}' \
                  f'\n\n{word.explanation}' \
                  f'\n\n {word.link}'
    else:
        # todo stop timer
        # if user has no available words
        message = 'You have no available words.\nPlease add new words or refresh existing one.\n' \
                  'As an option you can get all available words from the database.'

    return message


def get_arg(update):
    """
    Get arguments from user`s message

    :param args: /command argument
    :return:
    """
    args = update.message.text.split()

    if len(args) != 2:
        update.message.reply_text('Invalid arguments\n/command argument')
        return None

    arg = args[1]
    return arg


updater = Updater(BOT_TOKEN, use_context=True)
updater.dispatcher.add_handler(
    CommandHandler(
        'start',
        start_bot,
        pass_job_queue=True)
)
updater.dispatcher.add_handler(
    CommandHandler(
        'stop',
        stop_timer,
        pass_job_queue=True)
)
updater.dispatcher.add_handler(
    CommandHandler(
        'stop_bot',
        stop_bot,
        pass_job_queue=True)
)
updater.dispatcher.add_handler(
    CommandHandler(
        'status',
        status,
        pass_job_queue=True)
)
updater.dispatcher.add_handler(
    CommandHandler(
        'add_words',
        add_words,
        pass_job_queue=True,
        pass_args=True)
)
updater.dispatcher.add_handler(
    CommandHandler(
        'interval',
        change_interval,
        pass_job_queue=True)
)
updater.dispatcher.add_handler(
    CommandHandler(
        'language',
        change_language,
        pass_job_queue=True)
)
updater.dispatcher.add_handler(
    CommandHandler(
        'reset',
        reset_user_words,
        pass_job_queue=True)
)
updater.dispatcher.add_handler(
    CommandHandler(
        'add',
        add_single_word,
        pass_job_queue=True,
        pass_args=True)
)

updater.start_polling()
