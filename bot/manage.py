import gettext
import logging

import bot.constants as consts
import bot.conv_constants as cc
import bot.utils as utils
import bot.keyboards as kbs

from telegram import Update
from telegram.ext import CallbackContext

_ = gettext.gettext
kb = None

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    global _
    global kb
    kb = kbs.Keyboards(context.user_data['lang'])
    locale = gettext.translation('manage', localedir = 'locales', languages = [context.user_data['lang']])
    locale.install()
    _ = locale.gettext
    query.edit_message_text(
            text = _("Выберите действие"),
            reply_markup = kb.MANAGE_SURVEYS_KB
        )
    return cc.MANAGE_SURVEYS_STATE

def pick(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    if len(context.bot_data[consts.SURVEYS_KEY]) > 0:
        survey_list = utils.num_list(context.bot_data[consts.SURVEYS_KEY], key = 'title')
        query.edit_message_text(
                text = _("Выберите опрос из существующих\n\n"
                            "{list}\n"
                            "Для выбора опроса введите номер из списка").format(list = survey_list),
                reply_markup = kb.MAIN_MENU_KB
            )
    else:
        query.edit_message_text(
                text = _("Опросов пока что нет! Создайте новый опрос, нажав на кнопку"), 
                reply_markup = kb.START_SURVEY_NONE_KB
            )
    return cc.MANAGE_PICK_SURVEY_STATE

def survey(update: Update, context: CallbackContext) -> int:
    if update.callback_query is None:
        try:
            idx = utils.validate_index(update.message.text, context.bot_data[consts.SURVEYS_KEY])
            context.chat_data['s_idx'] = idx
            update.message.reply_text(
                    text = _("Что вы хотите сделать?"),
                    reply_markup = kb.MANAGE_SURVEY_KB
                )
            return cc.MANAGE_SURVEY_STATE
        except IndexError:
            update.message.reply_text(
                    text = _("Введённого номера нет в списке! Попробуйте ещё раз"),
                )
            return cc.MANAGE_PICK_SURVEY_STATE
        except ValueError:
            update.message.reply_text(
                    text = _("Неправильно введён номер! Попробуйте ещё раз"),
                )
            return cc.MANAGE_PICK_SURVEY_STATE
    else:
        query = update.callback_query
        query.answer()
        query.edit_message_text(
                text = _("Что вы хотите сделать?"),
                reply_markup = kb.MANAGE_SURVEY_KB
            )
        return cc.MANAGE_SURVEY_STATE

def confirm_delete(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(
            text = _("Вы уверены, что хотите удалить этот опрос?"),
            reply_markup = kb.YES_NO_KB
        )
    return cc.MANAGE_DELETE_CONFIRM_STATE

def delete(update: Update, context: CallbackContext) -> int:
    idx = context.chat_data['s_idx']
    del context.chat_data['s_idx']
    del context.bot_data[SURVEYS_KEY][idx]
    query.edit_message_text(
            text = _("Выберите действие"),
            reply_markup = kb.MANAGE_AFTER_DELETE_KB
        )
    return cc.MANAGE_AFTER_DELETE_STATE