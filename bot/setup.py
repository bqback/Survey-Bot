from typing import Union, List
from functools import partial

from bot.constants import (SURVEYS_KEY, ADMINS_KEY)

import bot.conv_constants as cc
import bot.commands as commands
import bot.inline as inline
import bot.access as access
import bot.manage as manage

from telegram import BotCommand, Update
from telegram.utils.request import Request
from telegram.ext import (Dispatcher, CommandHandler, InlineQueryHandler, ConversationHandler, 
                          TypeHandler, CallbackQueryHandler, MessageHandler, filters)

BOT_COMMANDS: List[BotCommand] = [
    BotCommand('start', 'Reserved for managing surveys'),
    BotCommand('show_id', 'Replies with id of the user'),
    BotCommand('update_admins', 'Updates the list of admin ids')
]

def register_dispatcher(dispatcher: Dispatcher, admins: Union[int, List[int]], logger) -> None:

    dispatcher.add_handler(TypeHandler(Update, partial(access.check, logger = logger)), group = -2)

    dispatcher.add_handler(InlineQueryHandler(inline.surveys))
    dispatcher.add_handler(CommandHandler('show_id', commands.show_id))
    dispatcher.add_handler(CommandHandler('update_admins', partial(commands.update_admins, admins = admins)))

    dispatcher.add_handler(ConversationHandler(
                entry_points = [CommandHandler('start', commands.start)],
                states = {
                    cc.START: [
                        CallbackQueryHandler(manage.start_survey, pattern='^'+cc.START_SURVEY_CB+'$'),
                        CallbackQueryHandler(manage.manage_surveys, pattern='^'+cc.MANAGE_SURVEYS_CB+'$')
                    ],
                    cc.START_SURV: [
                        CallbackQueryHandler(manage.get_description, pattern='^'+cc.CREATE_SURVEY_CB+'$'),
                    ],
                    cc.GET_DESC: [
                        MessageHandler(filters.Filters.text, manage.save_description)
                    ]
                    сс.START_OVER: [
                        CallbackQueryHandler(manage.get_description, pattern='^'+cc.YES_CB+'$'),
                        CallbackQueryHandler(manage.to_prev_step, pattern='^'+cc.NO_CB+'$')
                    ],
                    cc.MAIN_MENU: [
                        CallbackQueryHandler(manage.get_description, pattern='^'+cc.YES_CB+'$'),
                        CallbackQueryHandler(manage.to_prev_step, pattern='^'+cc.NO_CB+'$')
                    ]
                },
                fallbacks = [
                    CallbackQueryHandler(manage.to_prev_step, pattern='^'+cc.RETURN_CB+'$')
                    CallbackQueryHandler(manage.confirm_start_over, pattern='^'+cc.RETURN_START_OVER_CB+'$')
                    CallbackQueryHandler(manage.confirm_return_to_main, pattern='^'+cc.RETURN_TO_MAIN_CB+'$')
                    CommandHandler('start', commands.start)
                ]
        ))

    # Set commands
    dispatcher.bot.set_my_commands(BOT_COMMANDS)

    bot_data = dispatcher.bot_data
    if not bot_data.get(SURVEYS_KEY):
        bot_data[SURVEYS_KEY] = dict()
    if not bot_data.get(ADMINS_KEY):
        bot_data[ADMINS_KEY] = admins