from typing import Union, List
from functools import partial

from bot import (SURVEYS_KEY, ADMINS_KEY)

import bot.commands as commands
import bot.inline as inline
import bot.access as access

from telegram import BotCommand, Update
from telegram.utils.request import Request
from telegram.ext import Dispatcher, CommandHandler, InlineQueryHandler, TypeHandler

BOT_COMMANDS: List[BotCommand] = [
    BotCommand('start', 'Reserved for managing surveys'),
    BotCommand('show_id', 'Replies with id of the user'),
    BotCommand('update_admins', 'Updates the list of admin ids')
]

COMMAND_LIST: List[str] = [entry.command for entry in BOT_COMMANDS]

def register_dispatcher(dispatcher: Dispatcher, admins: Union[int, List[int]], logger) -> None:

    dispatcher.add_handler(TypeHandler(Update, partial(access.check, commands = COMMAND_LIST, logger = logger)), group = -2)

    dispatcher.add_handler(InlineQueryHandler(inline.surveys))
    dispatcher.add_handler(CommandHandler('start', commands.start))
    dispatcher.add_handler(CommandHandler('show_id', commands.show_id))
    dispatcher.add_handler(CommandHandler('update_admins', partial(commands.update_admins, admins = admins)))

    # Set commands
    dispatcher.bot.set_my_commands(BOT_COMMANDS)

    bot_data = dispatcher.bot_data
    if not bot_data.get(SURVEYS_KEY):
        bot_data[SURVEYS_KEY] = dict()
    if not bot_data.get(ADMINS_KEY):
        bot_data[ADMINS_KEY] = admins