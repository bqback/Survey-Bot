from typing import Union, List

from telegram import Update
from telegram.ext import CallbackContext

import bot.conv_constants as cc

from bot.constants import ADMINS_KEY, SURVEYS_MANAGE_ARG, START_ARGLESS
from bot.keyboards import INITIAL_STATE_KB


def start(update: Update, context: CallbackContext) -> None:
    try:
        if context.args[0] == SURVEYS_MANAGE_ARG:
            user = update.effective_user
            update.message.reply_text('Добро пожаловать, {}!'.format(user.first_name), reply_markup = INITIAL_STATE_KB)
            return cc.START_STATE
    except IndexError:
        update.message.reply_text(START_ARGLESS)

def show_id(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.from_user.id)

def update_admins(update: Update, context: CallbackContext, admins: Union[int, List[int]]) -> None:
    context.bot_data[ADMINS_KEY] = admins
    update.message.reply_text('Admin list updated!')

def show_current_survey(update: Update, context: CallbackContext) -> None:
    try:
        current = context.chat_data['current_survey']
        title_error, desc_error, question_error = False, False, False
        try:
            print('Название текущего опроса: {}'.format(current['title']))
        except KeyError:
            title_error = True
            print('У текущего опроса нет названия (Чё)')
        try:
            print('Описание текущего опроса: {}'.format(current['desc']))
        except KeyError:
            desc_error = True
            print('У текущего опроса нет описания (Чё)')
        try:
            for question in current['questions']:
                print('{} ({})'.format(question['question'], ))
        except KeyError:
            desc_error = True
            print('У текущего опроса нет описания (Чё)')
    except KeyError:
        print('В настоящее время не обрабатывается опрос')
    