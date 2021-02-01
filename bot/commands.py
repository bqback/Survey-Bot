from typing import Union, List

from telegram import Update
from telegram.ext import CallbackContext

import bot.conv_constants as cc

from bot.constants import ADMINS_KEY, SURVEYS_MANAGE_ARG, START_ARGLESS
from bot.keyboards import INITIAL_STATE_KB


def start(update: Update, context: CallbackContext) -> None:
    try:
        if context.args[0] == SURVEYS_MANAGE_ARG:
            user = update.effective_user
            update.message.reply_text('Добро пожаловать, {}!'.format(user.first_name), reply_markup = INITIAL_STATE_KB)
            return cc.START_STATE
    except IndexError:
        update.message.reply_text(START_ARGLESS)

def show_id(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.from_user.id)

def update_admins(update: Update, context: CallbackContext, admins: Union[int, List[int]]) -> None:
    context.bot_data[ADMINS_KEY] = admins
    update.message.reply_text('Admin list updated!')