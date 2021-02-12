from typing import Union, List
from functools import partial

from bot.constants import (SURVEYS_KEY, ADMINS_KEY)

import bot.conv_constants as cc
import bot.commands as commands
import bot.inline as inline
import bot.access as access
import bot.root as root
import bot.compose as compose
import bot.edit as edit

from telegram import BotCommand, Update
from telegram.utils.request import Request
from telegram.ext import (Updater, CommandHandler, InlineQueryHandler, ConversationHandler, 
                          TypeHandler, CallbackQueryHandler, MessageHandler, filters)

BOT_COMMANDS: List[BotCommand] = [
    BotCommand('add_admin', '[ADMIN] Adds an admin or a list of admins,\nseparated by a space, comma or semicolon'),
    BotCommand('restart', '[ADMIN] Restarts the bot'),
    BotCommand('remove_admin', '[ADMIN] Removes an admin or a list of admins. separated by a space, comma or semicolon'),
    BotCommand('rotate_log', '[ADMIN] Backs up current log and starts a new one'),
    BotCommand('show_current_survey', 'Displays everything contained in the current survey'),
    BotCommand('show_id', 'Replies with id of the user'),
    # BotCommand('start', 'Reserved for managing surveys'),
    BotCommand('update_admins', '[ADMIN] Updates the list of admin ids')
]

def register_dispatcher(updater: Updater, admins: Union[int, List[int]]) -> None:

    dispatcher = updater.dispatcher

    dispatcher.add_handler(TypeHandler(Update, access.check), group = -2)

    dispatcher.add_handler(InlineQueryHandler(inline.surveys))
    dispatcher.add_handler(CommandHandler('add_admin', commands.add_admin))
    dispatcher.add_handler(CommandHandler('restart', partial(commands.restart, updater = updater)))
    dispatcher.add_handler(CommandHandler('remove_admin', commands.remove_admin))
    dispatcher.add_handler(CommandHandler('rotate_log', commands.rotate_log))
    dispatcher.add_handler(CommandHandler('show_current_survey', commands.show_current_survey))
    dispatcher.add_handler(CommandHandler('show_id', commands.show_id))
    dispatcher.add_handler(CommandHandler('update_admins', commands.update_admins))

    edit_survey = ConversationHandler(
        entry_points = [
            CallbackQueryHandler(partial(edit.pick_part, source = 'compose'), pattern='^{}$'.format(cc.EDIT_SURVEY_COMPOSE_CB)),
            CallbackQueryHandler(partial(edit.pick_part, source = 'manage'), pattern='^{}$'.format(cc.EDIT_SURVEY_MANAGE_CB))
        ],
        states = {
            cc.PICK_PART_STATE: [
                CallbackQueryHandler(edit.title, pattern='^{}$'.format(cc.EDIT_TITLE_CB)),
                CallbackQueryHandler(edit.desc, pattern='^{}$'.format(cc.EDIT_DESC_CB)),
                CallbackQueryHandler(edit.questions, pattern='^{}$'.format(cc.EDIT_QUESTIONS_CB)),
            ],
            cc.EDIT_TITLE_STATE: [
                CallbackQueryHandler(compose.get_title, pattern='^{}$'.format(cc.NEW_TITLE_CB)),
                CallbackQueryHandler(edit.pick_part, pattern='^{}$'.format(cc.KEEP_CURRENT_TITLE_CB))
            ],
            cc.GET_TITLE_STATE: [
                MessageHandler(filters.Filters.text, compose.save_title)
            ],
            cc.SAVE_TITLE_STATE: [
                CallbackQueryHandler(edit.pick_part, pattern='^{}$'.format(cc.SAVE_TITLE_CB)),
                CallbackQueryHandler(compose.get_title, pattern='^{}$'.format(cc.ENTER_AGAIN_CB))
            ],
            cc.EDIT_DESC_STATE: [
                CallbackQueryHandler(compose.get_desc, pattern='^{}$'.format(cc.NEW_DESC_CB)),
                CallbackQueryHandler(edit.pick_part, pattern='^{}$'.format(cc.KEEP_CURRENT_DESC_CB))
            ],
            cc.GET_DESC_STATE: [
                MessageHandler(filters.Filters.text, compose.save_desc)
            ],
            cc.SAVE_DESC_STATE: [
                CallbackQueryHandler(edit.pick_part, pattern='^{}$'.format(cc.SAVE_DESC_CB)),
                CallbackQueryHandler(compose.get_desc, pattern='^{}$'.format(cc.ENTER_AGAIN_CB))
            ],
            cc.PICK_QUESTION_STATE: [
                MessageHandler(filters.Filters.text, edit.question)
            ]
        },
        fallbacks=[
            CallbackQueryHandler(root.confirm_return_to_main, pattern='^{}$'.format(cc.RETURN_TO_MAIN_CB)),
            CallbackQueryHandler(edit.save_changes, pattern='^{}$'.format(cc.SAVE_AND_EXIT_CB))
        ],
        map_to_parent = {
            cc.END_COMPOSE: cc.REVIEW_STATE,
            cc.END_MANAGE: cc.PICK_SURVEY_STATE
        })
    
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
                edit_survey
            ],
            cc.START_OVER_STATE: [
                CallbackQueryHandler(compose.get_title, pattern='^{}$'.format(cc.YES_CB)),
                CallbackQueryHandler(partial(compose.review, returning = True), pattern='^{}$'.format(cc.NO_CB))
            ]
        },
        fallbacks=[
            CallbackQueryHandler(root.confirm_start_over, pattern='^{}$'.format(cc.START_OVER_SURVEY_CB)),
        ],
        map_to_parent = {
            cc.END: cc.START_STATE,
            cc.START_STATE: cc.START_STATE
        })

    main_conv = ConversationHandler(
                entry_points = [CommandHandler('start', root.start)],
                states = {
                    cc.LANG_STATE: [
                        CallbackQueryHandler(partial(commands.set_lang, lang = ru), pattern='^{}$'.format(cc.RU_CB)),
                        CallbackQueryHandler(partial(commands.set_lang, lang = en), pattern='^{}$'.format(cc.EN_CB)),
                    ],
                    cc.START_STATE: [
                        CallbackQueryHandler(root.start_survey, pattern='^{}$'.format(cc.START_SURVEY_CB)),
                        CallbackQueryHandler(root.manage_surveys, pattern='^{}$'.format(cc.MANAGE_SURVEYS_CB))
                    ],
                    cc.START_SURVEY_STATE: [
                        add_survey,
                        MessageHandler(filters.Filters.text)
                    ]
                },
                fallbacks = [
                    CallbackQueryHandler(root.to_prev_step, pattern='^{}$'.format(cc.RETURN_CB)),
                    CallbackQueryHandler(root.confirm_start_over, pattern='^{}$'.format(cc.RETURN_START_OVER_CB)),
                    CallbackQueryHandler(root.confirm_return_to_main, pattern='^{}$'.format(cc.RETURN_TO_MAIN_CB)),
                    CommandHandler('start', root.start)
                ]
        )

    dispatcher.add_handler(main_conv)

    # Set commands
    dispatcher.bot.set_my_commands(BOT_COMMANDS)

    bot_data = dispatcher.bot_data
    if not bot_data.get(SURVEYS_KEY):
        bot_data[SURVEYS_KEY] = []
    if not bot_data.get(ADMINS_KEY):
        bot_data[ADMINS_KEY] = admins