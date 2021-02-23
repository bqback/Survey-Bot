import logging

from re import match
from typing import List

import bot.constants as consts

from telegram import Update
from telegram.ext import CallbackContext, DispatcherHandlerStop

def check(update: Update, context: CallbackContext) -> None:

    logger = logging.getLogger(__name__)
 
    if not update.effective_user:
        raise DispatcherHandlerStop()
    
    user_id = update.effective_user.id
    bot_data = context.bot_data
    user_data = context.user_data

    if update.message:
        text = update.message.text
        if 'lang' not in user_data and not match('^\/start$', text):
            raise DispatcherHandlerStop()
        else:
            if match('^\/.*', text):
                if not match('^\/show_id$', text):
                    if user_id in bot_data[consts.ADMINS_KEY]:
                        logger.info('Admin {} used command {}'.format(user_id, text))
                        return
                    else:
                        logger.info('User {} tried to access admin only command {}'.format(user_id, text))
                        raise DispatcherHandlerStop()
                else:
                    logger.info('User {} used command {}'.format(user_id, update.message.text))
                    return

    if update.inline_query:
        if user_id in bot_data[consts.ADMINS_KEY]:
            return
        else:
            raise DispatcherHandlerStop()

    if update.poll_answer:
        return

