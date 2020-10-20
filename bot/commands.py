from telegram import Update
from telegram.ext import CallbackContext

def show_id(update: Update, context: CallbackContext, logger) -> None:
    update.message.reply_text(update.message.from_user.id)