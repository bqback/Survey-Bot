import os
import sys
import re
import logging
import gettext

from functools import partial
from threading import Thread
from typing import Union, List
from configparser import ConfigParser

from telegram import Update
from telegram.ext import CallbackContext, Updater
from telegram.error import BadRequest

import bot.constants as consts
import bot.conv_constants as cc
import bot.root as root
import bot.keyboards as kbs

_ = gettext.gettext
kb = None

logger = logging.getLogger(__name__)


def show_id(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.from_user.id)


def show_chat_id(update: Update, context: CallbackContext) -> None:
    print(update.effective_chat)
    update.message.reply_text(update.effective_chat.id)


def add_chat(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 0:
        config = ConfigParser(comment_prefixes="/", allow_no_value=True)
        config.read_file(open("bot.ini"))
        chats = config["bot"]["chats"]
        chat_list = chats.split(",")
        for chat in context.args:
            chat = re.sub("[^-0-9 ]+", "", chat)
            if chat not in chat_list:
                try:
                    context.bot.get_chat(int(chat))
                    chats += ",{}".format(chat)
                    update.message.reply_text(
                        _("Чат {id} был добавлен!").format(id=chat)
                    )
                except BadRequest:
                    update.message.reply_text(
                        _(
                            "Бота нет в чате {id}! Добавьте его в этот чат, затем попробуйте снова"
                        ).format(id=chat)
                    )
            else:
                update.message.reply_text(
                    _("Чат {id} уже есть в списке!").format(id=chat)
                )
        config["bot"]["chats"] = chats.strip(",")
        config.write(open("bot.ini", "w"))
        chats = [int(chat_id) for chat_id in config["bot"]["chats"].split(",")]
        context.bot_data[consts.CHATS_KEY] = chats
        update.message.reply_text(_("Список чатов был обновлён!"))
    else:
        update.message.reply_text(
            _("Для использования команды нужно указать список добавляемых чатов!")
        )


def remove_chat(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 0:
        config = ConfigParser(comment_prefixes="/", allow_no_value=True)
        config.read_file(open("bot.ini"))
        chats = config["bot"]["chats"]
        chat_list = chats.split(",")
        for chat in context.args:
            chat = re.sub("[^0-9 ]+", "", chat)
            if chat in chat_list:
                chat_list.remove(chat)
                update.message.reply_text(_("Чат {id} был удалён!").format(id=chat))
            else:
                update.message.reply_text(_("Чата {id} нет в списке!").format(id=chat))
        config["bot"]["chats"] = ",".join(chat_list)
        config.write(open("bot.ini", "w"))
        chats = [int(chat_id) for chat_id in config["bot"]["chats"].split(",")]
        context.bot_data[consts.CHATS_KEY] = chats
        update.message.reply_text(_("Список чатов был обновлён!"))
    else:
        update.message.reply_text(
            _("Для использования команды нужно указать список удаляемых чатов!")
        )

def add_admin(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 0:
        config = ConfigParser(comment_prefixes="/", allow_no_value=True)
        config.read_file(open("bot.ini"))
        admins = config["bot"]["admins"]
        admin_list = admins.split(",")
        for admin in context.args:
            admin = re.sub("[^0-9 ]+", "", admin)
            if admin not in admin_list:
                admins += ",{id}".format(id=admin)
                update.message.reply_text(
                    _("Администратор {id} был добавлен!").format(id=admin)
                )
            else:
                update.message.reply_text(
                    _("Администратор {id} уже есть в списке!").format(id=admin)
                )
        config["bot"]["admins"] = admins.strip(",")
        config.write(open("bot.ini", "w"))
        admins = [int(admin_id) for admin_id in config["bot"]["admins"].split(",")]
        context.bot_data[consts.ADMINS_KEY] = admins
        update.message.reply_text(_("Список администраторов был обновлён!"))
    else:
        update.message.reply_text(
            _(
                "Для использования команды нужно указать список добавляемых администраторов!"
            )
        )


def remove_admin(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 0:
        config = ConfigParser(comment_prefixes="/", allow_no_value=True)
        config.read_file(open("bot.ini"))
        admins = config["bot"]["admins"]
        admin_list = admins.split(",")
        for admin in context.args:
            admin = re.sub("[^0-9 ]+", "", admin)
            if admin in admin_list:
                admin_list.remove(admin)
                update.message.reply_text(
                    _("Администратор {id} был удалён!").format(id=admin)
                )
            else:
                update.message.reply_text(
                    _("Администратора {id} нет в списке!").format(id=admin)
                )
                admins = 
        config["bot"]["admins"] = ",".join(admin_list)
        config.write(open("bot.ini", "w"))
        admins = [int(admin_id) for admin_id in config["bot"]["admins"].split(",")]
        context.bot_data[consts.ADMINS_KEY] = admins
        update.message.reply_text(_("Список администраторов был обновлён!"))
    else:
        update.message.reply_text(
            _(
                "Для использования команды нужно указать список удаляемых администраторов!"
            )
        )


def restart(update: Update, context: CallbackContext, updater: Updater) -> None:
    update.message.reply_text(_("Перезапуск..."))
    Thread(target=partial(stop_and_restart, updater=updater)).start()


def stop_and_restart(updater: Updater) -> None:
    updater.stop()
    sys.argv[0] = '"' + sys.argv[0] + '"'
    os.execl(sys.executable, sys.executable, *sys.argv)


def rotate_log(update: Update, context: CallbackContext) -> None:
    logger.info(
        _("Начат новый лог-файл по запросу {id}").format(id=update.effective_user.id)
    )
    logger.info("\n---------\nLog closed on %s.\n---------\n" % time.asctime())
    logger.handlers[0].doRollover()


def show_current_survey(update: Update, context: CallbackContext) -> None:
    try:
        current = context.chat_data["current_survey"]
        print(current)
        out = ""
        try:
            out += _("Название текущего опроса:\n{title}\n\n").format(
                title=current["title"]
            )
        except KeyError:
            out += _("У текущего опроса нет названия\n\n")
        try:
            out += _("Описание текущего опроса:\n{desc}\n\n").format(
                desc=current["desc"]
            )
        except KeyError:
            out += _("У текущего опроса нет описания\n\n")
        try:
            out += _("Вопросы:\n")
            for question in current["questions"]:
                multi = _("неск. вариантов") if question["multi"] else _("один вариант")
                out += _("\n{question} ({multi})").format(
                    question=question["question"], multi=multi
                )
                try:
                    for answer in question["answers"]:
                        out += "\n\t{answer}".format(answer=answer)
                except KeyError:
                    out += _("У этого вопроса нет ответов\n")
        except KeyError:
            out += _("У текущего опроса нет вопросов\n\n")
    except KeyError:
        out += _("В настоящее время не обрабатывается опрос")
    update.message.reply_text(out)


def set_lang(update: Update, context: CallbackContext, lang: str) -> None:
    query = update.callback_query
    query.answer()
    context.user_data["lang"] = lang
    try:
        global _
        global kb
        kb = kbs.Keyboards(context.user_data["lang"])
        locale = gettext.translation(
            "commands", localedir="locales", languages=[context.user_data["lang"]]
        )
        locale.install()
        _ = locale.gettext
    except ModuleNotFoundError:
        context.user_data["lang"] = None
        logger.error(
            "User {} picked an invalid language?".format(update.effective_user.id)
        )
    root.start(update, context)
    return cc.START_STATE


def reset_ongoing(update: Update, context: CallbackContext) -> None:
    context.bot_data["poll_ongoing"] = False
    del context.bot_data["ongoing"]


def help(update: Update, context: CallbackContext) -> None:
    #         BotCommand("restart", _("[Адм.] Restarts the bot")),
    #         BotCommand("remove_admin", _("[ADMIN] Removes an admin or a list of admins. separated by a space, comma or semicolon")),
    #         BotCommand("rotate_log", _("[ADMIN] Backs up current log and starts a new one")),
    #         BotCommand("show_current_survey", _("Displays everything contained in the current survey")),
    #         BotCommand("show_id", _("Replies with id of the user")),
    #         BotCommand("update_admins", _("[ADMIN] Updates the list of admin ids"))
    # if len(context.args) > 0:
    #     commands = context.bot.commands
    #     target = context.args[0]
    #     update.message.reply_text('/{command}\n\n{desc}'.format())
    # else:
    #     update.message.reply_text(_("Для использования команды нужно указать команду, о которой Вы хотите узнать больше\n"
    #                                 "Например /help show_id"))
    for command in context.bot.commands:
        update.message.reply_text(
            "/{command}\n\n{desc}".format(
                command=command.command, desc=command.long_description
            )
        )
