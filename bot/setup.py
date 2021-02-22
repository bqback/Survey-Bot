from typing import Union, List
from functools import partial

import bot.constants as consts
import bot.conv_constants as cc
import bot.commands as commands
import bot.inline as inline
import bot.access as access
import bot.root as root
import bot.compose as compose
import bot.edit as edit
import bot.poll as poll
import bot.settings as settings
import bot.manage as manage

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

def register_dispatcher(updater: Updater, admins: Union[int, List[int]], gsheets: str) -> None:

    dispatcher = updater.dispatcher

    dispatcher.add_handler(TypeHandler(Update, access.check), group = -2)

    dispatcher.add_handler(PollAnswerHandler(poll.collect_answer), group = -1)

    dispatcher.add_handler(InlineQueryHandler(inline.surveys))
    dispatcher.add_handler(CommandHandler('add_admin', commands.add_admin))
    dispatcher.add_handler(CommandHandler('add_chat', commands.add_chat))
    dispatcher.add_handler(CommandHandler('restart', partial(commands.restart, updater = updater)))
    dispatcher.add_handler(CommandHandler('remove_admin', commands.remove_admin))
    dispatcher.add_handler(CommandHandler('remove_chat', commands.remove_chat))
    dispatcher.add_handler(CommandHandler('rotate_log', commands.rotate_log))
    dispatcher.add_handler(CommandHandler('show_current_survey', commands.show_current_survey))
    dispatcher.add_handler(CommandHandler('show_id', commands.show_id))
    dispatcher.add_handler(CommandHandler('update_admins', commands.update_admins))
    dispatcher.add_handler(CommandHandler('update_chats', commands.update_chats))

    edit_conv = ConversationHandler(
        entry_points = [
            CallbackQueryHandler(partial(edit.pick_part, source = 'compose'), pattern='^{}$'.format(cc.EDIT_SURVEY_COMPOSE_CB)),
            CallbackQueryHandler(partial(edit.pick_part, source = 'manage'), pattern='^{}$'.format(cc.EDIT_SURVEY_MANAGE_CB))
        ],
        states = {
            cc.PICK_PART_STATE: [
                CallbackQueryHandler(edit.title, pattern='^{}$'.format(cc.EDIT_TITLE_CB)),
                CallbackQueryHandler(edit.desc, pattern='^{}$'.format(cc.EDIT_DESC_CB)),
                CallbackQueryHandler(edit.pick_question, pattern='^{}$'.format(cc.EDIT_QUESTIONS_CB)),
                CallbackQueryHandler(edit.save_changes, pattern='^{}$'.format(cc.SAVE_AND_EXIT_CB)),
                CallbackQueryHandler(edit.discard_changes, pattern='^{}$'.format(cc.DISCARD_AND_EXIT_CB))
            ],
            cc.EDIT_TITLE_STATE: [
                CallbackQueryHandler(partial(compose.get_title, mode = 'edit'), pattern='^{}$'.format(cc.NEW_TITLE_CB)),
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
                MessageHandler(filters.Filters.text, edit.question),
                CallbackQueryHandler(edit.pick_part, pattern='^{}$'.format(cc.RETURN_CB))
            ],
            cc.PICK_QUESTION_PART_STATE: [
                CallbackQueryHandler(edit.question_text, pattern='^{}$'.format(cc.EDIT_QUESTION_TEXT_CB)),
                CallbackQueryHandler(edit.multi, pattern='^{}$'.format(cc.EDIT_MULTI_CB)),
                CallbackQueryHandler(edit.answers, pattern='^{}$'.format(cc.EDIT_ANSWERS_CB)),
                CallbackQueryHandler(edit.remove_question_confirm, pattern='^{}$'.format(cc.REMOVE_QUESTION_CB)),
                CallbackQueryHandler(edit.pick_question, pattern='^{}$'.format(cc.RETURN_CB))
            ],
            cc.EDIT_QUESTION_TEXT_STATE: [
                CallbackQueryHandler(partial(compose.get_question, mode = 'edit'), pattern='^{}$'.format(cc.NEW_QUESTION_TEXT_CB)),
                CallbackQueryHandler(edit.question, pattern='^{}$'.format(cc.KEEP_CURRENT_QUESTION_TEXT_CB)),
                CallbackQueryHandler(edit.remove_question_confirm, pattern='^{}$'.format(cc.REMOVE_QUESTION_CB))
            ],
            cc.GET_QUESTION_STATE: [
                MessageHandler(filters.Filters.text, partial(compose.save_question, mode = 'edit'))
            ],
            cc.SAVE_QUESTION_STATE: [
                CallbackQueryHandler(partial(edit.save_result, result = 'question'), pattern='^{}$'.format(cc.SAVE_QUESTION_CB)),
                CallbackQueryHandler(partial(compose.get_question, mode = 'edit'), pattern='^{}$'.format(cc.ENTER_AGAIN_CB))
            ],
            cc.EDIT_MULTI_STATE: [
                CallbackQueryHandler(compose.get_multi, pattern='^{}$'.format(cc.NEW_MULTI_CB)),
                CallbackQueryHandler(edit.question, pattern='^{}$'.format(cc.KEEP_CURRENT_MULTI_CB))
            ],
            cc.GET_MULTIANS_STATE: [
                CallbackQueryHandler(partial(compose.save_multi, multi = True, mode = 'edit'), pattern='^{}$'.format(cc.YES_CB)),
                CallbackQueryHandler(partial(compose.save_multi, multi = False, mode = 'edit'), pattern='^{}$'.format(cc.NO_CB))
            ],
            cc.SAVE_MULTIANS_STATE: [
                CallbackQueryHandler(partial(edit.save_result, result = 'multi'), pattern='^{}$'.format(cc.YES_CB)),
                CallbackQueryHandler(compose.get_multi, pattern='^{}$'.format(cc.ENTER_AGAIN_CB))
            ],
            cc.EDIT_ANSWERS_STATE: [
                CallbackQueryHandler(edit.pick_answer, pattern='^{}$'.format(cc.EDIT_EXISTING_ANSWER_CB)),
                CallbackQueryHandler(partial(compose.get_answer, mode = 'edit'), pattern='^{}$'.format(cc.ADD_NEW_ANSWER_CB)),
                CallbackQueryHandler(edit.question, pattern='^{}$'.format(cc.RETURN_CB))
            ],
            cc.PICK_ANSWER_STATE: [
                MessageHandler(filters.Filters.text, edit.answer),
                CallbackQueryHandler(edit.question, pattern='^{}$'.format(cc.RETURN_CB))
            ],
            cc.EDIT_ANSWER_STATE: [
                CallbackQueryHandler(partial(compose.get_answer, mode = 'edit'), pattern='^{}$'.format(cc.EDIT_ANSWER_CB)),
                CallbackQueryHandler(edit.remove_answer_confirm, pattern='^{}$'.format(cc.REMOVE_ANSWER_CB))
            ],
            cc.GET_ANSWER_STATE: [
                MessageHandler(filters.Filters.text, partial(compose.save_answer, mode = 'edit'))
            ],
            cc.SAVE_ANSWER_STATE: [
                CallbackQueryHandler(partial(edit.save_result, result = 'answers'), pattern='^{}$'.format(cc.SAVE_ANSWER_CB)),
                CallbackQueryHandler(partial(compose.get_question, mode = 'edit'), pattern='^{}$'.format(cc.ENTER_AGAIN_CB))
            ],
            cc.REMOVE_ANSWER_CONFIRM_STATE: [
                CallbackQueryHandler(edit.remove_answer, pattern = '^{}$'.format(cc.YES_CB)),
                CallbackQueryHandler(edit.pick_answer, pattern = '^{}$'.format(cc.NO_CB))
            ],
            cc.REMOVE_QUESTION_CONFIRM_STATE: [
                CallbackQueryHandler(edit.remove_question, pattern = "^{}$".format(cc.YES_CB)),
                CallbackQueryHandler(edit.question, pattern = '^{}$'.format(cc.NO_CB))
            ],
            cc.EDIT_AFTER_SAVE_STATE: [
                CallbackQueryHandler(edit.pick_part, pattern='^{}$'.format(cc.TO_PARTS_CB)),
                CallbackQueryHandler(edit.pick_question, pattern='^{}$'.format(cc.TO_QUESTIONS_CB))
            ],
            cc.SAVE_CONFIRM_STATE: [
                CallbackQueryHandler(edit.save_changes, pattern = "^{}$".format(cc.YES_CB)),
                CallbackQueryHandler(edit.pick_part, pattern = '^{}$'.format(cc.NO_CB))
            ],
            cc.DISCARD_CONFIRM_STATE: [
                CallbackQueryHandler(edit.discard_changes, pattern = "^{}$".format(cc.YES_CB)),
                CallbackQueryHandler(edit.pick_part, pattern = '^{}$'.format(cc.NO_CB))
            ]
        },
        fallbacks=[
            CallbackQueryHandler(root.confirm_return_to_main, pattern='^{}$'.format(cc.RETURN_TO_MAIN_CB)),
        ],
        map_to_parent = {
            cc.END_COMPOSE: cc.REVIEW_STATE,
            cc.END_MANAGE: cc.MANAGE_SURVEYS_STATE
        })
    
    compose_conv = ConversationHandler(
                entry_points = [CallbackQueryHandler(compose.get_title, pattern='^{}$'.format(cc.CREATE_SURVEY_CB))],
                states = {
                    cc.GET_TITLE_STATE: [
                        MessageHandler(filters.Filters.text, compose.save_title),
                        CallbackQueryHandler(compose.return_to_step, pattern='^{}$'.format(cc.YES_CB)),
                        CallbackQueryHandler(compose.get_title, pattern='^{}$'.format(cc.NO_CB))
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
                        CallbackQueryHandler(partial(compose.save_multi, multi = True), pattern='^{}$'.format(cc.YES_CB)),
                        CallbackQueryHandler(partial(compose.save_multi, multi = False), pattern='^{}$'.format(cc.NO_CB))
                    ],
                    cc.SAVE_MULTIANS_STATE: [
                        CallbackQueryHandler(compose.get_answer, pattern='^{}$'.format(cc.YES_CB)),
                        CallbackQueryHandler(compose.get_multi, pattern='^{}$'.format(cc.ENTER_AGAIN_CB))
                    ],
                    cc.GET_ANSWER_STATE: [
                        MessageHandler(filters.Filters.text, compose.save_answer)
                    ],
                    cc.SAVE_ANSWER_STATE: [
                        CallbackQueryHandler(compose.checkpoint, pattern='^{}$'.format(cc.SAVE_ANSWER_CB)),
                        CallbackQueryHandler(partial(compose.get_answer, returning = True), pattern='^{}$'.format(cc.ENTER_AGAIN_CB))
                    ],
                    cc.CHECKPOINT_STATE: [
                        CallbackQueryHandler(compose.get_answer, pattern='^{}$'.format(cc.NEXT_ANSWER_CB)),
                        CallbackQueryHandler(compose.get_question, pattern='^{}$'.format(cc.NEXT_QUESTION_CB)),
                        CallbackQueryHandler(compose.review, pattern='^{}$'.format(cc.FINISH_CREATING_CB))
                    ],
                    cc.REVIEW_STATE: [
                        CallbackQueryHandler(compose.finish, pattern='^{}$'.format(cc.CREATION_COMPLETE_CB)),
                        edit_conv
                    ],
                    cc.START_OVER_STATE: [
                        CallbackQueryHandler(compose.get_title, pattern='^{}$'.format(cc.YES_CB)),
                        CallbackQueryHandler(partial(compose.review, returning = True), pattern='^{}$'.format(cc.NO_CB))
                    ]
                },
                fallbacks=[
                    CommandHandler('start', root.start)
                ],
                map_to_parent = {
                    cc.END: cc.START_STATE,
                    cc.START_STATE: cc.START_STATE,
                    cc.MAIN_MENU_STATE: cc.MAIN_MENU_STATE
                }
        )

    manage_conv = ConversationHandler(
                entry_points = [CallbackQueryHandler(manage.start, pattern="^{}$".format(cc.MANAGE_SURVEYS_CB))],
                states = {
                    cc.MANAGE_SURVEYS_STATE: [
                        compose_conv,
                        CallbackQueryHandler(manage.pick, pattern="^{}$".format(cc.CHOOSE_SURVEY_CB))
                    ],
                    cc.MANAGE_PICK_SURVEY_STATE: [
                        MessageHandler(filters.Filters.text, manage.survey),
                        compose_conv
                    ],
                    cc.MANAGE_SURVEY_STATE:[
                        edit_conv,
                        CallbackQueryHandler(manage.confirm_delete, pattern="^{}$".format(cc.MANAGE_DELETE_SURVEY_CB)),
                        CallbackQueryHandler(manage.print_survey, pattern="^{}$".format(cc.PRINT_SURVEY_CB))
                    ],
                    cc.MANAGE_DELETE_CONFIRM_STATE: [
                        CallbackQueryHandler(manage.delete, pattern="^{}$".format(cc.YES_CB)),
                        CallbackQueryHandler(manage.survey, pattern="^{}$".format(cc.NO_CB))
                    ],
                    cc.MANAGE_AFTER_DELETE_STATE: [
                        CallbackQueryHandler(manage.pick, pattern="^{}$".format(cc.CHOOSE_SURVEY_CB))
                    ],
                    cc.MAIN_MENU_STATE: [
                        CallbackQueryHandler(root.start, pattern="^{}$".format(cc.YES_CB)),
                        CallbackQueryHandler(manage.start, pattern="^{}$".format(cc.NO_CB))
                    ]
                },
                fallbacks = [
                    CallbackQueryHandler(root.confirm_return_to_main, pattern='^{}$'.format(cc.RETURN_TO_MAIN_CB))
                ],
                map_to_parent = {
                    cc.START_STATE: cc.START_STATE
                }
        )

    settings_conv = ConversationHandler(
                entry_points = [CallbackQueryHandler(settings.pick, pattern='^{}$'.format(cc.SETTINGS_CB))],
                states = {
                    cc.PICK_SETTING_STATE: [
                        CallbackQueryHandler(settings.lang, pattern="^{}$".format(cc.SETTINGS_LANG_CB))
                    ]
                },
                fallbacks = [],
                map_to_parent = {
                    cc.SETTINGS_LANG_STATE: cc.LANG_STATE
                }
        )

    poll_conv = ConversationHandler(
                entry_points = [CallbackQueryHandler(poll.pick_survey, pattern="^{}$".format(cc.START_SURVEY_CB))],
                states = {
                    cc.POLL_PICK_STATE: [
                        MessageHandler(filters.Filters.text, poll.preview),
                        compose_conv
                    ],
                    cc.POLL_PREVIEW_STATE: [
                        CallbackQueryHandler(poll.pick_chat, pattern="^{}$".format(cc.PICK_CHAT_CB)),
                        CallbackQueryHandler(poll.pick_survey, pattern="^{}$".format(cc.CHOOSE_SURVEY_CB))
                    ],
                    cc.PICK_CHAT_STATE: [
                        MessageHandler(filters.Filters.text, poll.set_cap)
                    ],
                    cc.SET_CAP_STATE: [
                        CallbackQueryHandler(poll.confirm, pattern="^{}$".format(cc.USE_RECOMMENDED_CB)),
                        CallbackQueryHandler(poll.get_cap, pattern="^{}$".format(cc.SET_OWN_CAP_CB))
                    ],
                    cc.GET_CAP_STATE: [
                        MessageHandler(filters.Filters.text, poll.validate_cap)
                    ],
                    cc.VALIDATE_CAP_STATE:[
                        CallbackQueryHandler(poll.confirm, pattern="^{}$".format(cc.USE_RECOMMENDED_CB)),
                        CallbackQueryHandler(poll.confirm, pattern="^{}$".format(cc.USE_CUSTOM_CB)),
                        CallbackQueryHandler(poll.get_cap, pattern="^{}$".format(cc.ENTER_AGAIN_CB))
                    ],
                    cc.POLL_CONFIRM_STATE:[
                        CallbackQueryHandler(poll.launch, pattern="^{}$".format(cc.START_SURVEY_CB))
                        CallbackQueryHandler(poll.pick_survey, pattern="^{}$".format(cc.CHANGE_SURVEY_CB)),
                        CallbackQueryHandler(poll.pick_chat, pattern="^{}$".format(cc.CHANGE_CHAT_CB)),
                        CallbackQueryHandler(poll.set_cap, pattern="^{}$".format(cc.CHANGE_CAP_CB))
                    ]
                },
                fallbacks = [
                    CallbackQueryHandler(root.confirm_return_to_main, pattern='^{}$'.format(cc.RETURN_TO_MAIN_CB))
                ],
                map_to_parent = {
                    cc.START_STATE: cc.START_STATE,
                    cc.START_SURVEY_STATE: cc.START_SURVEY_STATE
                }
        )

    main_conv = ConversationHandler(
                entry_points = [CommandHandler('start', root.start)],
                states = {
                    cc.LANG_STATE: [
                        CallbackQueryHandler(partial(commands.set_lang, lang = "ru"), pattern="^{}$".format(cc.RU_CB)),
                        CallbackQueryHandler(partial(commands.set_lang, lang = "en"), pattern="^{}$".format(cc.EN_CB)),
                    ],
                    cc.START_STATE: [
                        poll_conv
                        manage_conv,
                        settings_conv
                    ],
                    cc.MAIN_MENU_STATE: [
                        CallbackQueryHandler(root.start, pattern = "^{}$".format(cc.YES_CB))
                    ]
                },
                fallbacks = [
                    CallbackQueryHandler(root.to_prev_step, pattern='^{}$'.format(cc.RETURN_CB)),
                    CallbackQueryHandler(root.confirm_return_to_main, pattern='^{}$'.format(cc.RETURN_TO_MAIN_CB)),
                    CommandHandler('start', root.start)
                ]
        )

    dispatcher.add_handler(main_conv)

    # Set commands
    dispatcher.bot.set_my_commands(BOT_COMMANDS)

    bot_data = dispatcher.bot_data
    if not bot_data.get(consts.SURVEYS_KEY):
        bot_data[consts.SURVEYS_KEY] = []
    if not bot_data.get(consts.ADMINS_KEY):
        bot_data[consts.ADMINS_KEY] = admins
    if not bot_data.get(consts.SHEETS_KEY):
        bot_data[consts.ADMINS_KEY] = gsheets