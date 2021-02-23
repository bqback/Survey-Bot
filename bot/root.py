import logging
import gettext

from uuid import uuid4

from telegram.ext import CallbackContext
from telegram import Update, BotCommand

import bot.constants as consts
import bot.conv_constants as cc
import bot.keyboards as kbs
import bot.utils as utils

from bot.extbotcommand import ExtBotCommand

kb = None

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    if 'lang' not in context.user_data or context.user_data['lang'] == None:
        context.bot.send_message(
                    chat_id = update.effective_chat.id,
                    text = f"{cc.CHOOSE_LANG}", 
                    reply_markup = kbs.LANG_KB
            )
        return cc.LANG_STATE
    else:
        global _
        global kb
        kb = kbs.Keyboards(context.user_data['lang'])
        locale = gettext.translation('root', localedir = 'locales', languages = [context.user_data['lang']])
        locale.install()
        _ = locale.gettext
        BOT_COMMANDS: List[ExtBotCommand] = [
            ExtBotCommand("add_admin", 
                            _("[Адм.] Добавляет нового администратора/администраторов с указанными ID"),
                            _("[Адм.] Добавляет нового администратора или администраторов с указанными ID\n"
                                        "Большая часть команд (в т. ч. запуск и управление опросами) доступна только администраторам\n"
                                        "После использования команды используйте команду /update_admins для использования ботом обновлённого списка\n"
                                        "ID должны быть разделены пробелами, кавычками или точками с запятыми\n"
                                        "Пример: /add_admin 11111111 22222222")
                ),
            ExtBotCommand("add_chat", 
                            _("[Адм.] Добавляет новый чат/чаты с указанными ID"),
                            _("[Адм.] Добавляет новый чат или чаты с указанными ID\n"
                                        "Для того, чтобы иметь возможность запустить опрос в чате, его предварительно нужно добавить, используя эту команду\n"
                                        "Добавить можно только те чаты, где состоит этот бот\n"
                                        "Для получения ID чата используйте команду /show_chat_id\n"
                                        "После использования команды используйте команду /update_chats для использования ботом обновлённого списка\n"
                                        "ID должны быть разделены пробелами, кавычками или точками с запятыми\n\n"
                                        "Пример: /add_chat -11111111 -22222222")
                ),
            ExtBotCommand("help", _("/help command: Выводит подробную справку по команде")),
            ExtBotCommand("restart", 
                            _("[Адм.] Перезапускает бота"),
                            _("[Адм.] Перезапускает бота\n"
                                "Происходит перезагрузка бота (аналогично простому запуску)\n"
                                "Позволяет применять внесённые в файлы бота изменения с помощью самого же бота")
                            ),
            # ExtBotCommand("remove_admin", _("[Адм.] Удаляет администратора/администраторов с указанными ID")),
            # ExtBotCommand("remove_chat", _("[Адм.] Удаляет чат/чаты с указанными ID")),
            # ExtBotCommand("reset_ongoing", _("[Адм.] Сбрасывает флаг 'сейчас идёт опрос'")),
            # ExtBotCommand("rotate_log", _("[Адм.] Сохраняет текущий лог и запускает новый")),
            # ExtBotCommand("show_chat_id", _("Показывает ID текущего чата")),
            # ExtBotCommand("show_current_survey", _("Выводит все данные обрабатываемого в данный момент опроса")),
            # ExtBotCommand("show_id", _("Показывает ID пользователя, использовавшего команду")),
            # ExtBotCommand("update_admins", _("[Адм.] Обновляет список админов в памяти бота")),
            # ExtBotCommand("update_chats", _("[Адм.] Обновляет список чатов в памяти бота"))
        ]
        context.bot.set_my_commands(BOT_COMMANDS)
        if update.callback_query is None:
            context.bot.send_message(
                    chat_id = update.effective_chat.id,
                    text = _("Добро пожаловать, {name}!").format(name = user.first_name), 
                    reply_markup = kb.INITIAL_STATE_KB
                )
        else:
            query = update.callback_query
            query.answer()
            query.edit_message_text(
                    text = _("Добро пожаловать, {name}!").format(name = user.first_name), 
                    reply_markup = kb.INITIAL_STATE_KB
                )
        return cc.START_STATE

def manage_surveys(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    user = update.effective_user
    query.answer()
    query.edit_message_text(
            text = _("Выберите действие"), 
            reply_markup = kb.MANAGE_SURVEYS_KB
        )
    return cc.MANAGE_SURVEYS_STATE

def choose_survey(update: Update, context: CallbackContext) -> int:
    return

def load_survey(update: Update, context: CallbackContext) -> int:
    return

def to_prev_step(update: Update, context: CallbackContext) -> int:
    argsdict = {'update': update, 'context': context}
    globals()[context.chat_data['last_handler']](**argsdict)
    return context.chat_data['last_state']

def confirm_return_to_main(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(
            text = _("Вы уверены, что хотите вернуться в главное меню?"), 
            reply_markup = kb.YES_NO_KB
        )
    return cc.MAIN_MENU_STATE


