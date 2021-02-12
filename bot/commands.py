import os
import sys
import re
import logging
import importlib

from functools import partial
from threading import Thread
from typing import Union, List
from configparser import ConfigParser

from telegram import Update
from telegram.ext import CallbackContext, Updater

import bot.conv_constants as cc
import bot.root as root
import bot.keyboards as kbs

from bot.constants import ADMINS_KEY, SURVEYS_MANAGE_ARG

text = None
kb = None

logger = logging.getLogger(__name__)

def show_id(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.from_user.id)

def update_admins(update: Update, context: CallbackContext) -> None:
    config = ConfigParser()
    config.read('bot.ini')
    admins = [int(admin_id) for admin_id in config.get('bot', 'admins').split(',')]
    context.bot_data[ADMINS_KEY] = admins
    update.message.reply_text('Admin list updated!')

def add_admin(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 0:
        config = ConfigParser(comment_prefixes = '/', allow_no_value = True)
        config.read_file(open('bot.ini'))
        admins = config['bot']['admins']
        admin_list = admins.split(',')
        for new_admin in context.args:
            new_admin = re.sub('[^0-9 ]+', '', new_admin)
            if new_admin not in admin_list:
                admins += ',{}'.format(new_admin)
                update.message.reply_text('New admin {} was added!'.format(new_admin))
            else:
                update.message.reply_text('Admin {} is already on the list!'.format(new_admin))
        config['bot']['admins'] = admins
        config.write(open('bot.ini', 'w'))
    else:
        update.message.reply_text('You must include a list of IDs to add!')

def remove_admin(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 0:
        config = ConfigParser(comment_prefixes = '/', allow_no_value = True)
        config.read_file(open('bot.ini'))
        admins = config['bot']['admins']
        admin_list = admins.split(',')
        for remove_admin in context.args:
            remove_admin = re.sub('[^0-9 ]+', '', remove_admin)
            if remove_admin in admin_list:
                admin_list.remove(remove_admin)
                update.message.reply_text('Admin {} was removed!'.format(remove_admin))
            else:
                update.message.reply_text('Admin {} is not on the admin list!'.format(remove_admin))
        config['bot']['admins'] = ','.join(admin_list)
        config.write(open('bot.ini', 'w'))
    else:
        update.message.reply_text('You must include a list of IDs to remove!')

def restart(update: Update, context: CallbackContext, updater: Updater) -> None:
    update.message.reply_text('Restarting...')
    Thread(target = partial(stop_and_restart, updater = updater)).start()

def stop_and_restart(updater: Updater) -> None:
    updater.stop()
    sys.argv[0] = '"' + sys.argv[0] + '"'
    os.execl(sys.executable, sys.executable, *sys.argv)

def rotate_log(update: Update, context: CallbackContext) -> None:
    logger = logging.getLogger(__name__)
    logger.info('{}: Rotating log over as requested'.format(update.effective_user.id))
    logger.info('\n---------\nLog closed on %s.\n---------\n' % time.asctime())
    logger.handlers[0].doRollover()

def show_current_survey(update: Update, context: CallbackContext) -> None:
    try:
        current = context.chat_data['current_survey']
        print(current)
        out = ''
        try:
            out += 'Название текущего опроса:\n{}\n\n'.format(current['title'])
        except KeyError:
            out += 'У текущего опроса нет названия (Чё)\n\n'
        try:
            out += 'Описание текущего опроса:\n{}\n\n'.format(current['desc'])
        except KeyError:
            out += 'У текущего опроса нет описания (Чё)\n\n'
        try:
            out += 'Вопросы:\n'
            for question in current['questions']:
                multi = 'неск. вариантов' if question['multi'] else 'один вариант'
                out += '\n{} ({})'.format(question['question'], multi)
                try:
                    for answer in question['answers']:
                        out += '\n\t{}'.format(answer)
                except KeyError:
                    out += 'У текущего вопроса нет ответов (Чё)\n'
        except KeyError:
            out += 'У текущего опроса нет вопросов (Чё)\n\n'
    except KeyError:
        out += 'В настоящее время не обрабатывается опрос'
    update.message.reply_text(out)

def set_lang(update: Update, context: CallbackContext, lang: str) -> None:
    global text
    global kb
    if lang == '🇷🇺':
        context.user_data['lang'] = 'ru'
        text = importlib.import_module('locale.{}'.format(context.user_data['lang']))
        kb = kbs.Keyboards(context.user_data['lang'])
    elif lang == '🇺🇸':
        context.user_data['lang'] = 'en'
        text = importlib.import_module('locale.{}'.format(context.user_data['lang']))
        kb = kbs.Keyboards(context.user_data['lang'])
    else:
        logger.error('User {} picked an invalid language?'.format(update.effective_user.id))
    root.start(update, context)
