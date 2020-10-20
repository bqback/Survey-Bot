from typing import Union, List

from telegram import Update
from telegram.ext import CallbackContext

from bot.constants import ADMINS_KEY

def show_id(update: Update, context: CallbackContext, logger) -> None:
    update.message.reply_text(update.message.from_user.id)

def update_admins(update: Update, context: CallbackContext, logger, admins: Union[int, List[int]]) -> None:
    context.bot_data[ADMINS_KEY] = admins
    update.message.reply_text('Admin list updated!')