import gettext
import logging

from telegram import Update
from telegram.ext import CallbackContext

import bot.constants as consts
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
    kb = kbs.Keyboards(context.user_data["settings"]["lang"])
    locale = gettext.translation(
        "settings",
        localedir="locales",
        languages=[context.user_data["settings"]["lang"]],
    )
    locale.install()
    _ = locale.gettext
    query.edit_message_text(
        text=_("Выберите настройку"),
        reply_markup=kb.SETTINGS_KB,
    )
    return cc.PICK_SETTING_STATE


def lang(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"{cc.CHOOSE_LANG}", reply_markup=kbs.LANG_KB)
    return cc.SETTINGS_LANG_STATE


def page_len(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = kb.populate_keyboard(
        page_len=100,
        per_row=3,
        length=6,
        labels=[10, 25, 50, 16, 24, 32],
        labels_as_data=True,
        returnable=True,
    )
    query.edit_message_text(
        text=_(
            "Эта настройка определяет, сколько результатов выводится на одной странице "
            "при выборе из нумерованного списка (напр. из списка опросов)\n\n"
            "Текущее значение: {curr}\n"
            "Значение по умолчанию: {default}"
        ).format(
            curr=context.user_data["settings"]["page_len"],
            default=context.bot_data[consts.DEFAULTS_KEY]["page_len"],
        ),
        reply_markup=keyboard,
    )
    return cc.SETTINGS_PAGE_LEN_STATE


def row_len(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = kb.populate_keyboard(
        page_len=100,
        per_row=5,
        length=5,
        labels=[2, 4, 5, 6, 8],
        labels_as_data=True,
        returnable=True,
    )
    query.edit_message_text(
        text=_(
            "Эта настройка определяет, сколько кнопок может максимально выводиться в одном ряду "
            "при выборе из нумерованного списка (напр. из списка опросов)\n\n"
            "Текущее значение: {curr}\n"
            "Значение по умолчанию: {default}"
        ).format(
            curr=context.user_data["settings"]["row_len"],
            default=context.bot_data[consts.DEFAULTS_KEY]["row_len"],
        ),
        reply_markup=keyboard,
    )
    return cc.SETTINGS_ROW_LEN_STATE


def change_setting(update: Update, context: CallbackContext, setting: str) -> int:
    query = update.callback_query
    query.answer()
    if setting in ("page_len", "row_len"):
        new_val = int(query.data)
    context.user_data["settings"][setting] = new_val
    query.edit_message_text(
        text=_("Настройка сохранена!\nВыберите настройку"),
        reply_markup=kb.SETTINGS_KB,
    )
    return cc.PICK_SETTING_STATE
