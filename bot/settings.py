import gettext
import logging

from telegram import Update
from telegram.ext import CallbackContext

import bot.conv_constants as cc
import bot.keyboards as kbs

_ = gettext.gettext
kb = None

logger = logging.getLogger(__name__)

def pick(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    global _
    global kb
    kb = kbs.Keyboards(context.user_data['lang'])
    locale = gettext.translation('settings', localedir = 'locales', languages = [context.user_data['lang']])
    locale.install()
    _ = locale.gettext
    context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = _("Выберите настройку"), 
                reply_markup = kb.SETTINGS_KB
            )
    return cc.PICK_SETTING_STATE

def lang(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(
            text = f"{cc.CHOOSE_LANG}", 
            reply_markup = kbs.LANG_KB
        )
    return cc.SETTINGS_LANG_STATE