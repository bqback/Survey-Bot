import logging
import gettext

from uuid import uuid4

from telegram.ext import CallbackContext
from telegram import Update

from bot.constants import SURVEYS_KEY

import bot.conv_constants as cc
import bot.keyboards as kbs

kb = None

_ = gettext.gettext
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
        context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = _("Добро пожаловать, {name}!").format(name = user.first_name), 
                reply_markup = kb.INITIAL_STATE_KB
            )
        return cc.START_STATE

def start_survey(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    bot_data = context.bot_data
    if len(context.bot_data[SURVEYS_KEY]) > 0:
        survey_list = ""
        for idx, survey in enumerate(context.bot_data[SURVEYS_KEY]):
            survey_list.append(f"{idx}. {survey['title']}\n")
        query.edit_message_text(
                text = _("Выберите опрос из существующих\n\n"
                            "{list}\n\n"
                            "Для выбора опроса введите номер из списка").format(list = survey_list),
                reply_markup = kb.MAIN_MENU_KB
            )
    else:
        query.edit_message_text(
                text = _("Опросов пока что нет! Создайте новый опрос, нажав на кнопку"), 
                reply_markup = kb.START_SURVEY_NONE_KB
            )
    return cc.START_SURVEY_STATE

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

def confirm_start_over(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    update.message.reply_text(text.CONFIRM_START_OVER, reply_markup = kb.YES_NO_KB)
    return cc.START_OVER_STATE

def confirm_return_to_main(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    update.message.reply_text(text.CONFIRM_RETURN_TO_MAIN, reply_markup = kb.YES_NO_KB)
    return cc.MAIN_MENU_STATE


