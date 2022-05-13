import gettext
import logging

from re import match
from typing import List

import bot.constants as consts

from telegram import Update
from telegram.ext import CallbackContext, ApplicationHandlerStop

_ = gettext.gettext

logger = logging.getLogger(__name__)


async def check(update: Update, context: CallbackContext) -> None:

    locale = gettext.translation('access', localedir='locales', languages = ['ru'])
    locale.install()
    _ = locale.gettext

    if not update.effective_user:
        raise ApplicationHandlerStop()

    user_id = update.effective_user.id
    bot_data = context.bot_data
    user_data = context.user_data

    if update.message:
        text = update.message.text
        if "settings" not in user_data and not match("^/start$", text):
            raise ApplicationHandlerStop()
        if match("^/.+$", text):
            logger.info(
                        _("Пользователь {id} использовал команду {command}").format(
                            id=user_id, command=update.message.text
                        )
                    )
            if update.effective_chat.type != "private":
                if not match("^/show_chat_id", text):
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Все команды кроме /show_chat_id доступны только в ЛС!",
                    )
                    raise ApplicationHandlerStop()
                else:
                    logger.info(
                        _("Пользователь {id} использовал команду /show_chat_id").format(
                            id=user_id
                        )
                    )
        # else:
        #     if match('^\/.*', text):
        #         if not match('^\/show_id$', text):
        #             if user_id in bot_data[consts.ADMINS_KEY]:
        #                 logger.info('Admin {} used command {}'.format(user_id, text))
        #                 return
        #             else:
        #                 logger.info('User {} tried to access admin only command {}'.format(user_id, text))
        #                 raise ApplicationHandlerStop()
        #         else:
        #             logger.info('User {} used command {}'.format(user_id, update.message.text))
        #             return

    if update.inline_query:
        if user_id in bot_data[consts.ADMINS_KEY]:
            return
        else:
            raise ApplicationHandlerStop()

    if update.poll_answer:
        return
