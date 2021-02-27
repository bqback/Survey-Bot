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
    kb = kbs.Keyboards(context.user_data["settings"]["lang"])
    locale = gettext.translation(
        "manage", localedir="locales", languages=[context.user_data["settings"]["lang"]]
    )
    locale.install()
    _ = locale.gettext
    query.edit_message_text(
        text=_("Выберите действие"), reply_markup=kb.MANAGE_SURVEYS_KB
    )
    return cc.MANAGE_SURVEYS_STATE


def pick(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    if query.data != "PAGENUM":
        if len(context.bot_data[consts.SURVEYS_KEY]) > 0:
            survey_list = utils.num_list(
                context.bot_data[consts.SURVEYS_KEY], key="title"
            )
            multipage = context.user_data["settings"]["page_len"] < len(
                context.bot_data[consts.SURVEYS_KEY]
            )
            if multipage:
                if "page" not in context.chat_data:
                    context.chat_data["page"] = 1
                elif query.data == "prev page":
                    context.chat_data["page"] -= 1
                elif query.data == "next page":
                    context.chat_data["page"] += 1
            else:
                context.chat_data["page"] = None
            keyboard = kb.populate_keyboard(
                page_len=context.user_data["settings"]["page_len"],
                per_row=context.user_data["settings"]["row_len"],
                length=len(context.bot_data[consts.SURVEYS_KEY]),
                multipage=multipage,
                page=context.chat_data["page"],
            )
            query.edit_message_text(
                text=_("Выберите опрос из существующих\n\n" "{list}").format(
                    list=survey_list
                ),
                reply_markup=keyboard,
            )
        else:
            query.edit_message_text(
                text=_("Опросов пока что нет! Создайте новый опрос, нажав на кнопку"),
                reply_markup=kb.START_SURVEY_NONE_KB,
            )
    return cc.MANAGE_PICK_SURVEY_STATE


def survey(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    if "s_idx" not in context.chat_data:
        idx = int(query.data)
        context.chat_data["s_idx"] = idx
    query.edit_message_text(
        text=_("Что вы хотите сделать?"), reply_markup=kb.MANAGE_SURVEY_KB
    )
    return cc.MANAGE_SURVEY_STATE


def print_survey(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    idx = context.chat_data["s_idx"]
    survey = utils.print_survey(context.bot_data[consts.SURVEYS_KEY][idx])
    query.edit_message_text(
        text=_("{survey}\n\nЧто вы хотите сделать?").format(survey=survey),
        reply_markup=kb.MANAGE_SURVEY_KB,
    )
    return cc.MANAGE_SURVEY_STATE


def confirm_delete(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text=_("Вы уверены, что хотите удалить этот опрос?"), reply_markup=kb.YES_NO_KB
    )
    return cc.MANAGE_DELETE_CONFIRM_STATE


def delete(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    idx = context.chat_data["s_idx"]
    del context.chat_data["s_idx"]
    del context.bot_data[consts.SURVEYS_KEY][idx]
    query.edit_message_text(
        text=_("Выберите действие"), reply_markup=kb.MANAGE_AFTER_DELETE_KB
    )
    return cc.MANAGE_AFTER_DELETE_STATE
