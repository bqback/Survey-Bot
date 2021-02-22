import os
import sys
import re
import logging
import gettext

from functools import partial
from threading import Thread
from typing import Union, List
from configparser import ConfigParser

from telegram import Update
from telegram.ext import CallbackContext, Updater

import bot.constants as consts
import bot.conv_constants as cc
import bot.root as root
import bot.keyboards as kbs

from bot.constants import ADMINS_KEY, SURVEYS_MANAGE_ARG

_ = gettext.gettext
kb = None

logger = logging.getLogger(__name__)

def show_id(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.from_user.id)

def show_chat_id(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.effective_chat.id)

def update_chats(update: Update, context: CallbackContext) -> None:
    config = ConfigParser()
    config.read('bot.ini')
    chats = [int(admin_id) for chat_id in config.get('bot', 'chats').split(',')]
    context.bot_data[consts.CHATS_KEY] = chats
    update.message.reply_text(_('Список чатов был обновлён!'))

def add_chat(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 0:
        config = ConfigParser(comment_prefixes = '/', allow_no_value = True)
        config.read_file(open('bot.ini'))
        chats = config['bot']['chats']
        chat_list = chats.split(',')
        for chat in context.args:
            chat = re.sub('[^0-9 ]+', '', chat)
            if chat not in chat_list:
                try:
                    context.bot.get_chat(int(chat))
                    chats += ',{}'.format(chat)
                    update.message.reply_text(_('Чат {id} был добавлен!').format(id = chat))
                except TelegramError:
                    update.message.reply_text(_('Бота нет в чате {id}! Добавьте его в этот чат, затем попробуйте снова').format(id = chat))
            else:
                update.message.reply_text(_('Чат {id} уже есть в списке!').format(id = chat))
        config['bot']['chats'] = chats
        config.write(open('bot.ini', 'w'))
    else:
        update.message.reply_text(_('Для использования команды нужно указать список добавляемых чатов!'))

def remove_chat(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 0:
        config = ConfigParser(comment_prefixes = '/', allow_no_value = True)
        config.read_file(open('bot.ini'))
        chats = config['bot']['chats']
        chat_list = chats.split(',')
        for chat in context.args:
            chat = re.sub('[^0-9 ]+', '', chat)
            if chat in chat_list:
                chat_list.remove(chat)
                update.message.reply_text(_('Чат {id} был удалён!').format(id = chat))
            else:
                update.message.reply_text(_('Чата {id} нет в списке!').format(id = chat))
        config['bot']['chats'] = ','.join(chat_list)
        config.write(open('bot.ini', 'w'))
    else:
        update.message.reply_text(_('Для использования команды нужно указать список удаляемых чатов!'))

def update_admins(update: Update, context: CallbackContext) -> None:
    config = ConfigParser()
    config.read('bot.ini')
    admins = [int(admin_id) for admin_id in config.get('bot', 'admins').split(',')]
    context.bot_data[consts.ADMINS_KEY] = admins
    update.message.reply_text(_('Список администраторов был обновлён!'))

def add_admin(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 0:
        config = ConfigParser(comment_prefixes = '/', allow_no_value = True)
        config.read_file(open('bot.ini'))
        admins = config['bot']['admins']
        admin_list = admins.split(',')
        for admin in context.args:
            admin = re.sub('[^0-9 ]+', '', admin)
            if admin not in admin_list:
                admins += ',{}'.format(admin)
                update.message.reply_text(_('Администратор {id} был добавлен!').format(id = admin))
            else:
                update.message.reply_text(_('Администратор {id} уже есть в списке!').format(id = admin))
        config['bot']['admins'] = admins
        config.write(open('bot.ini', 'w'))
    else:
        update.message.reply_text(_('Для использования команды нужно указать список добавляемых администраторов!'))

def remove_admin(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 0:
        config = ConfigParser(comment_prefixes = '/', allow_no_value = True)
        config.read_file(open('bot.ini'))
        admins = config['bot']['admins']
        admin_list = admins.split(',')
        for admin in context.args:
            admin = re.sub('[^0-9 ]+', '', admin)
            if admin in admin_list:
                admin_list.remove(admin)
                update.message.reply_text(_('Администратор {id} был удалён!').format(id = admin))
            else:
                update.message.reply_text(_('Администратора {id} нет в списке!').format(id = admin))
        config['bot']['admins'] = ','.join(admin_list)
        config.write(open('bot.ini', 'w'))
    else:
        update.message.reply_text(_('Для использования команды нужно указать список удаляемых администраторов!'))

def restart(update: Update, context: CallbackContext, updater: Updater) -> None:
    update.message.reply_text(_("Перезапуск..."))
    Thread(target = partial(stop_and_restart, updater = updater)).start()

def stop_and_restart(updater: Updater) -> None:
    updater.stop()
    sys.argv[0] = '"' + sys.argv[0] + '"'
    os.execl(sys.executable, sys.executable, *sys.argv)

def rotate_log(update: Update, context: CallbackContext) -> None:
    logger.info(_("Начат новый лог-файл по запросу {id}").format(id = update.effective_user.id))
    logger.info('\n---------\nLog closed on %s.\n---------\n' % time.asctime())
    logger.handlers[0].doRollover()

def show_current_survey(update: Update, context: CallbackContext) -> None:
    try:
        current = context.chat_data['current_survey']
        print(current)
        out = ''
        try:
            out += _("Название текущего опроса:\n{title}\n\n").format(title = current['title'])
        except KeyError:
            out += _("У текущего опроса нет названия\n\n")
        try:
            out += _("Описание текущего опроса:\n{desc}\n\n").format(desc = current['desc'])
        except KeyError:
            out += _("У текущего опроса нет описания\n\n")
        try:
            out += _("Вопросы:\n")
            for question in current['questions']:
                multi = _("неск. вариантов") if question['multi'] else _("один вариант")
                out += _("\n{question} ({multi})").format(question = question['question'], multi = multi)
                try:
                    for answer in question['answers']:
                        out += '\n\t{}'.format(answer)
                except KeyError:
                    out += _("У этого вопроса нет ответов\n")
        except KeyError:
            out += _("У текущего опроса нет вопросов\n\n")
    except KeyError:
        out += _("В настоящее время не обрабатывается опрос")
    update.message.reply_text(out)

def set_lang(update: Update, context: CallbackContext, lang: str) -> None:
    query = update.callback_query
    query.answer()
    context.user_data['lang'] = lang
    try:
        global _
        global kb
        kb = kbs.Keyboards(context.user_data['lang'])
        locale = gettext.translation('commands', localedir = 'locales', languages = [context.user_data['lang']])
        locale.install()
        _ = locale.gettext
    except ModuleNotFoundError:
        context.user_data['lang'] = None
        logger.error('User {} picked an invalid language?'.format(update.effective_user.id))
    root.start(update, context)
    return cc.START_STATE
