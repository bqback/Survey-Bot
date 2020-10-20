from typing import List

from telegram import Update
from telegram.ext import CallbackContext

from bot.constants import ADMINS_KEY

def check(update: Update, context: CallbackContext, commands: List[str], logger) -> None:
    
    if not update.effective_user:
        raise DispatcherHandlerStop()
    
    user_id = update.effective_user.id
    bot_data = context.bot_data

    if user_id in bot_data[ADMINS_KEY]:
        logger.info('Admin {} used command {}'.format(user_id, update.message.text))
        return
    elif update.message.text in commands:
        logger.info('User {} tried to access admin only command {}'.format(user_id, update.message.text))
        raise DispatcherHandlerStop()

    if update.poll_answer:
        return

