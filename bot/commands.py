import os
import sys
import re
import logging
import gettext
import email_validator
import copy

from functools import partial, wraps
from threading import Thread
from configparser import ConfigParser

from telegram import Update
from telegram.ext import CallbackContext, Updater
from telegram.error import BadRequest

import bot.botcommands as bcmds
import bot.constants as consts
import bot.conv_constants as cc
import bot.root as root
import bot.keyboards as kbs

_ = gettext.gettext
kb = None

logger = logging.getLogger(__name__)


def restricted(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in context.bot_data[consts.ADMINS_KEY]:
            logger.warning(
                _(
                    "Пользователь {id} хотел использовать администраторскую команду {command}"
                ).format(id=user_id, command=update.message.text)
            )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=_("Команда доступна только администраторам!\nСвяжитесь с администратором для получения доступа")
            )
            return
        return func(update, context, *args, **kwargs)

    return wrapped


async def show_id(update: Update, __: CallbackContext) -> None:
    await update.message.reply_text(update.message.from_user.id)


async def show_chat_id(update: Update, __: CallbackContext) -> None:
    await update.message.reply_text(update.effective_chat.id)


async def show_current_survey(update: Update, context: CallbackContext) -> None:
    try:
        current = context.chat_data["current_survey"]
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
        out = _("В настоящее время не обрабатывается опрос")
    await update.message.reply_text(out)


async def set_lang(update: Update, context: CallbackContext, lang: str) -> None:
    query = update.callback_query
    await query.answer()
    if "settings" not in context.user_data:
        context.user_data["settings"] = copy.deepcopy(
            context.bot_data[consts.DEFAULTS_KEY]
        )
    context.user_data["settings"]["lang"] = lang
    try:
        global _
        global kb
        kb = kbs.Keyboards(context.user_data["settings"]["lang"])
        locale = gettext.translation(
            "commands",
            localedir="locales",
            languages=[context.user_data["settings"]["lang"]],
        )
        locale.install()
        _ = locale.gettext
    except ModuleNotFoundError:
        context.user_data["settings"]["lang"] = None
        logger.error(
            "User {} picked an invalid language?".format(update.effective_user.id)
        )
    await root.start(update, context)
    return cc.START_STATE


async def help(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 0:
        try:
            __ = (await context.bot.get_my_commands())[0].long_description
        except AttributeError:
            bcmd = bcmds.BotCommands(context.user_data["settings"]["lang"])
            await context.bot.set_my_commands(bcmd.bot_commands)
        if context.args[0] != "all":
            commands = await context.bot.get_my_commands()
            target = context.args[0]
            command = list(filter(lambda cmd: cmd.command == target, commands))
            if len(command) > 0:
                await update.message.reply_text(
                    "/{command}\n\n{desc}".format(
                        command=command[0].command, desc=command[0].long_description
                    )
                )
            else:
                await update.message.reply_text(_("Команда не найдена! Попробуйте ещё раз"))
        else:
            for command in await context.bot.get_my_commands():
                await update.message.reply_text(
                    "/{command}\n\n{desc}".format(
                        command=command.command, desc=command.long_description
                    )
                )
    else:
        await update.message.reply_text(
            _(
                "Для использования команды нужно указать команду, о которой Вы хотите узнать больше\n"
                "Например /help show_id\n\n"
                "Для вывода всех доступных команд используйте /help all"
            )
        )


@restricted
async def add_chat(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 0:
        config = ConfigParser(comment_prefixes="/", allow_no_value=True)
        config.read_file(open("bot.ini"))
        chats = config["bot"]["chats"]
        chat_list = chats.split(",")
        for chat in context.args:
            chat = re.sub("[^-0-9 ]+", "", chat)
            if chat not in chat_list:
                try:
                    await context.bot.get_chat(int(chat))
                    chats += ",{}".format(chat)
                    await update.message.reply_text(
                        _("Чат {id} был добавлен!").format(id=chat)
                    )
                except BadRequest:
                    await update.message.reply_text(
                        _(
                            "Бота нет в чате {id}! Добавьте его в этот чат, затем попробуйте снова"
                        ).format(id=chat)
                    )
            else:
                await update.message.reply_text(
                    _("Чат {id} уже есть в списке!").format(id=chat)
                )
        config["bot"]["chats"] = chats.strip(",")
        config.write(open("bot.ini", "w"))
        chats = [int(chat_id) for chat_id in config["bot"]["chats"].split(",")]
        context.bot_data[consts.CHATS_KEY] = chats
        await update.message.reply_text(_("Список чатов был обновлён!"))
    else:
        await update.message.reply_text(
            _("Для использования команды нужно указать список добавляемых чатов!")
        )


@restricted
async def remove_chat(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 0:
        config = ConfigParser(comment_prefixes="/", allow_no_value=True)
        config.read_file(open("bot.ini"))
        chats = config["bot"]["chats"]
        chat_list = chats.split(",")
        for chat in context.args:
            chat = re.sub("[^0-9 ]+", "", chat)
            if chat in chat_list:
                chat_list.remove(chat)
                await update.message.reply_text(_("Чат {id} был удалён!").format(id=chat))
            else:
                await update.message.reply_text(_("Чата {id} нет в списке!").format(id=chat))
        config["bot"]["chats"] = ",".join(chat_list)
        config.write(open("bot.ini", "w"))
        chats = [int(chat_id) for chat_id in config["bot"]["chats"].split(",")]
        context.bot_data[consts.CHATS_KEY] = chats
        await update.message.reply_text(_("Список чатов был обновлён!"))
    else:
        await update.message.reply_text(
            _("Для использования команды нужно указать список удаляемых чатов!")
        )


@restricted
async def add_admin(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 0:
        config = ConfigParser(comment_prefixes="/", allow_no_value=True)
        config.read_file(open("bot.ini"))
        admins = config["bot"]["admins"]
        admin_list = admins.split(",")
        for admin in context.args:
            admin = re.sub("[^0-9 ]+", "", admin)
            if admin not in admin_list:
                admins += ",{id}".format(id=admin)
                await update.message.reply_text(
                    _("Администратор {id} был добавлен!").format(id=admin)
                )
            else:
                await update.message.reply_text(
                    _("Администратор {id} уже есть в списке!").format(id=admin)
                )
        config["bot"]["admins"] = admins.strip(",")
        config.write(open("bot.ini", "w"))
        admins = [int(admin_id) for admin_id in config["bot"]["admins"].split(",")]
        context.bot_data[consts.ADMINS_KEY] = admins
        await update.message.reply_text(_("Список администраторов был обновлён!"))
    else:
        await update.message.reply_text(
            _(
                "Для использования команды нужно указать список добавляемых администраторов!"
            )
        )


@restricted
async def remove_admin(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 0:
        config = ConfigParser(comment_prefixes="/", allow_no_value=True)
        config.read_file(open("bot.ini"))
        admins = config["bot"]["admins"]
        admin_list = admins.split(",")
        for admin in context.args:
            admin = re.sub("[^0-9 ]+", "", admin)
            if admin in admin_list:
                admin_list.remove(admin)
                await update.message.reply_text(
                    _("Администратор {id} был удалён!").format(id=admin)
                )
            else:
                await update.message.reply_text(
                    _("Администратора {id} нет в списке!").format(id=admin)
                )
        config["bot"]["admins"] = ",".join(admin_list)
        config.write(open("bot.ini", "w"))
        admins = [int(admin_id) for admin_id in config["bot"]["admins"].split(",")]
        context.bot_data[consts.ADMINS_KEY] = admins
        await update.message.reply_text(_("Список администраторов был обновлён!"))
    else:
        await update.message.reply_text(
            _(
                "Для использования команды нужно указать список удаляемых администраторов!"
            )
        )


def stop_and_restart(updater: Updater) -> None:
    updater.stop()
    sys.argv[0] = '"' + sys.argv[0] + '"'
    os.execl(sys.executable, sys.executable, *sys.argv)


@restricted
async def restart(update: Update, context: CallbackContext, updater: Updater) -> None:
    await update.message.reply_text(_("Перезапуск..."))
    Thread(target=partial(stop_and_restart, updater=updater)).start()


@restricted
def rotate_log(update: Update, __: CallbackContext) -> None:
    logger.info(
        _("Начат новый лог-файл по запросу {id}").format(id=update.effective_user.id)
    )
    logger.info("\n---------\nLog closed on %s.\n---------\n" % time.asctime())
    logger.handlers[0].doRollover()


@restricted
async def reset_ongoing(update: Update, context: CallbackContext) -> None:
    context.bot_data["poll_ongoing"] = False
    del context.bot_data["ongoing"]
    await update.message.reply_text(_("Флаг сброшен"))


@restricted
async def set_gsheets_owner(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 0:
        email = context.args[0]
        try:
            valid = email_validator.validate_email(email)
            email = valid.email
            context.bot_data[consts.SHEETS_KEY]["email"] = email
            await update.message.reply_text(_("Адрес почты изменён"))
        except email_validator.EmailNotValidError as e:
            await update.message.reply_text(str(e))
    else:
        await update.message.reply_text(
            _(
                "Для использования команды нужно указать почтовый ящик\n"
                "Например /set_gsheets_owner test@example.com"
            )
        )
