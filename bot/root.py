import logging
import gettext

from uuid import uuid4

from telegram.ext import CallbackContext
from telegram import Update

import bot.constants as consts
import bot.conv_constants as cc
import bot.keyboards as kbs
import bot.utils as utils

kb = None

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    if 'lang' not in context.user_data or context.user_data['lang'] == None:
        context.bot.send_message(
                    chat_id = update.effective_chat.id,
                    text = f"{cc.CHOOSE_LANG}", 
                    reply_markup = kbs.LANG_KB
            )
        return cc.LANG_STATE
    else:
        global _
        global kb
        kb = kbs.Keyboards(context.user_data['lang'])
        locale = gettext.translation('root', localedir = 'locales', languages = [context.user_data['lang']])
        locale.install()
        _ = locale.gettext
        if update.callback_query is None:
            context.bot.send_message(
                    chat_id = update.effective_chat.id,
                    text = _("Добро пожаловать, {name}!").format(name = user.first_name), 
                    reply_markup = kb.INITIAL_STATE_KB
                )
        else:
            query = update.callback_query
            query.answer()
            query.edit_message_text(
                    text = _("Добро пожаловать, {name}!").format(name = user.first_name), 
                    reply_markup = kb.INITIAL_STATE_KB
                )
        return cc.START_STATE

def manage_surveys(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    user = update.effective_user
    query.answer()
    query.edit_message_text(
            text = _("Выберите действие"), 
            reply_markup = kb.MANAGE_SURVEYS_KB
        )
    return cc.MANAGE_SURVEYS_STATE

def choose_survey(update: Update, context: CallbackContext) -> int:
    return

def load_survey(update: Update, context: CallbackContext) -> int:
    return

def to_prev_step(update: Update, context: CallbackContext) -> int:
    argsdict = {'update': update, 'context': context}
    globals()[context.chat_data['last_handler']](**argsdict)
    return context.chat_data['last_state']

def confirm_return_to_main(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(
            text = _("Вы уверены, что хотите вернуться в главное меню?"), 
            reply_markup = kb.YES_NO_KB
        )
    return cc.MAIN_MENU_STATE


