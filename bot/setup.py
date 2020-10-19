from typing import Union

from bot import (SURVEYS_KEY)

from telegram import Bot
from telegram.utils.request import Request
from telegram.ext import Dispatcher

import bot.inline as inline

def register_dispatcher(dispatcher: Dispatcher, admin: Union[int, str]) -> None:

    #dispatcher.add_handler(InlineQueryHandler(inline.surveys))

    bot_data = dispatcher.bot_data
    if not bot_data.get(SURVEYS_KEY):
        bot_data[SURVEYS_KEY] = dict()