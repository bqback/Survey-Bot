import logging

from re import match
from typing import List

from telegram import Update
from telegram.ext import CallbackContext, DispatcherHandlerStop

from bot.constants import ADMINS_KEY

def check(update: Update, context: CallbackContext) -> None:

    logger = logging.getLogger(__name__)
 
    if not update.effective_user:
        raise DispatcherHandlerStop()
    
    user_id = update.effective_user.id
    bot_data = context.bot_data
    user_data = context.user_data

    if update.message:
        if not user_data['lang']:
            raise DispatcherHandlerStop()
        else:
            if match('^\/.*', update.message.text):
                if not match('^\/show_id$', update.message.text):
                    if user_id in bot_data[ADMINS_KEY]:
                        logger.info('Admin {} used command {}'.format(user_id, update.message.text))
                        return
                    else:
                        logger.info('User {} tried to access admin only command {}'.format(user_id, update.message.text))
                        raise DispatcherHandlerStop()
                else:
                    logger.info('User {} used command {}'.format(user_id, update.message.text))
                    return

    if update.inline_query:
        if user_id in bot_data[ADMINS_KEY]:
            return
        else:
            raise DispatcherHandlerStop()

    if update.poll_answer:
        return

