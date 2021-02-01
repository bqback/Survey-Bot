from typing import Union, List
from functools import partial

from bot.constants import (SURVEYS_KEY, ADMINS_KEY)

import bot.conv_constants as cc
import bot.commands as commands
import bot.inline as inline
import bot.access as access
import bot.manage as manage
import bot.compose as compose

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

    add_survey = ConversationHandler(
        entry_points = [CallbackQueryHandler(compose.get_title, pattern='^{}$'.format(cc.CREATE_SURVEY_CB))],
        states = {
            cc.GET_TITLE_STATE: [
                MessageHandler(filters.Filters.text, compose.save_title)
            ],
            cc.SAVE_TITLE_STATE: [
                CallbackQueryHandler(compose.get_desc, pattern='^{}$'.format(cc.SAVE_TITLE_CB)),
                CallbackQueryHandler(compose.get_title, pattern='^{}$'.format(cc.ENTER_AGAIN_CB))
            ],
            cc.GET_DESC_STATE: [
                MessageHandler(filters.Filters.text, compose.save_desc)
            ],
            cc.SAVE_DESC_STATE: [
                CallbackQueryHandler(compose.get_question, pattern='^{}$'.format(cc.SAVE_DESC_CB)),
                CallbackQueryHandler(compose.get_desc, pattern='^{}$'.format(cc.ENTER_AGAIN_CB))
            ],
            cc.GET_QUESTION_STATE: [
                MessageHandler(filters.Filters.text, compose.save_question)
            ],
            cc.SAVE_QUESTION_STATE: [
                CallbackQueryHandler(compose.get_multi, pattern='^{}$'.format(cc.SAVE_QUESTION_CB)),
                CallbackQueryHandler(partial(compose.get_question, returning = True), pattern='^{}$'.format(cc.ENTER_AGAIN_CB))
            ],
            cc.GET_MULTIANS_STATE: [
                CallbackQueryHandler(compose.get_multi, pattern='^{}$'.format(cc.SAVE_QUESTION_CB)),
                CallbackQueryHandler(compose.get_question, pattern='^{}$'.format(cc.ENTER_AGAIN_CB))
            ],
            cc.RECORD_MULTIANS_STATE: [
                CallbackQueryHandler(partial(compose.save_multi, multi = True), pattern='^{}$'.format(cc.YES_CB)),
                CallbackQueryHandler(partial(compose.save_multi, multi = False), pattern='^{}$'.format(cc.NO_CB))
            ],
            cc.SAVE_MULTIANS_STATE: [
                CallbackQueryHandler(compose.get_answer, pattern='^{}$'.format(cc.SAVE_MULTI_CB)),
                CallbackQueryHandler(compose.get_multi, pattern='^{}$'.format(cc.ENTER_AGAIN_CB))
            ],
            cc.GET_ANSWER_STATE: [
                MessageHandler(filters.Filters.text, compose.record_answer)
            ],
            cc.RECORD_ANSWER_STATE: [
                CallbackQueryHandler(compose.save_answer, pattern='^{}$'.format(cc.SAVE_ANSWER_CB)),
                CallbackQueryHandler(partial(compose.get_answer, returning = True), pattern='^{}$'.format(cc.ENTER_AGAIN_CB))
            ],
            cc.SAVE_ANSWER_STATE: [
                CallbackQueryHandler(compose.get_answer, pattern='^{}$'.format(cc.NEXT_ANSWER_CB)),
                CallbackQueryHandler(compose.get_question, pattern='^{}$'.format(cc.NEXT_QUESTION_CB)),
                CallbackQueryHandler(compose.review, pattern='^{}$'.format(cc.FINISH_CREATING_CB))
            ],
            cc.REVIEW_STATE: [
                CallbackQueryHandler(compose.finish, pattern='^{}$'.format(cc.CREATION_COMPLETE_CB)),
                CallbackQueryHandler(edit.pick_part, pattern='^{}$'.format(cc.EDIT_SURVEY_CB)),
            ],
            cc.START_OVER_STATE: [
                CallbackQueryHandler(compose.get_title, pattern='^{}$'.format(cc.YES_CB)),
                CallbackQueryHandler(partial(compose.review, returning = True), pattern='^{}$'.format(cc.NO_CB))
            ]
        },
        fallbacks=[
            CallbackQueryHandler(manage.confirm_start_over, pattern='^{}$'.format(cc.START_OVER_SURVEY_CB)),
        ],
        map_to_parent = {
            cc.END: cc.START_STATE
        })

    edit_survey = ConversationHandler(
        entry_points = [CallbackQueryHandler(edit.pick_survey, pattern='^{}$'.format(cc.PICK_SURVEY_CB))],
        states = {
            cc.PICK_SURVEY_STATE: [
                MessageHandler(filters.Filters.text, edit.pick_part)
            ],
            cc.PICK_PART_STATE: [
                CallbackQueryHandler(edit.title, pattern='^{}$'.format(cc.CREATION_COMPLETE_CB)),
                CallbackQueryHandler(edit.desc, pattern='^{}$'.format(cc.EDIT_SURVEY_CB)),
                CallbackQueryHandler(edit.questions, pattern='^{}$'.format(cc.START_OVER_SURVEY_CB)),
            ]
        },
        fallbacks=[
            CallbackQueryHandler(edit.title, pattern='^{}$'.format(cc.CREATION_COMPLETE_CB)),
        ],
        map_to_parent = {
            cc.END: cc.START_STATE
        })

    main_conv = ConversationHandler(
                entry_points = [CommandHandler('start', commands.start)],
                states = {
                    cc.START_STATE: [
                        CallbackQueryHandler(manage.start_survey, pattern='^{}$'.format(cc.START_SURVEY_CB)),
                        CallbackQueryHandler(manage.manage_surveys, pattern='^{}$'.format(cc.MANAGE_SURVEYS_CB))
                    ],
                    cc.START_SURVEY_STATE: [
                        CallbackQueryHandler(manage.get_title, pattern='^{}$'.format(cc.CREATE_SURVEY_CB)),
                    ],
                    cc.START_OVER_STATE: [
                        CallbackQueryHandler(manage.get_title, pattern='^{}$'.format(cc.YES_CB)),
                        CallbackQueryHandler(manage.to_prev_step, pattern='^{}$'.format(cc.NO_CB))
                    ],
                    cc.MAIN_MENU_STATE: [
                        CallbackQueryHandler(manage.start, pattern='^{}$'.format(cc.YES_CB)),
                        CallbackQueryHandler(manage.to_prev_step, pattern='^{}$'.format(cc.NO_CB))
                    ],
                    cc.MANAGE_SURVEYS_STATE: [
                        CallbackQueryHandler(manage.get_title, pattern='^{}$'.format(cc.CREATE_SURVEY_CB)),
                        CallbackQueryHandler(manage.choose_survey, pattern='^{}$'.format(cc.CHOOSE_SURVEY_CB))
                    ],
                    cc.GET_TITLE_STATE: add_survey
                },
                fallbacks = [
                    CallbackQueryHandler(manage.to_prev_step, pattern='^{}$'.format(cc.RETURN_CB)),
                    CallbackQueryHandler(manage.confirm_start_over, pattern='^{}$'.format(cc.RETURN_START_OVER_CB)),
                    CallbackQueryHandler(manage.confirm_return_to_main, pattern='^{}$'.format(cc.RETURN_TO_MAIN_CB)),
                    CommandHandler('start', commands.start)
                ]
        )

    # Set commands
    dispatcher.bot.set_my_commands(BOT_COMMANDS)

    bot_data = dispatcher.bot_data
    if not bot_data.get(SURVEYS_KEY):
        bot_data[SURVEYS_KEY] = []
    if not bot_data.get(ADMINS_KEY):
        bot_data[ADMINS_KEY] = admins