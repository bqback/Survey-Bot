from typing import Union, List

from telegram import Update
from telegram.ext import CallbackContext

from bot.constants import ADMINS_KEY, SURVEYS_MANAGE
from bot.manage import manage

def start(update: Update, context: CallbackContext) -> None:
    if context.args[0] == SURVEYS_MANAGE:
        manage(context.bot_data)

def show_id(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.from_user.id)

def update_admins(update: Update, context: CallbackContext, admins: Union[int, List[int]]) -> None:
    context.bot_data[ADMINS_KEY] = admins
    update.message.reply_text('Admin list updated!')