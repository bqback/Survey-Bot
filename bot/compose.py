import gettext
import logging

from uuid import uuid4

from telegram.ext import CallbackContext
from telegram import Update
from functools import partial

from bot.constants import SURVEYS_KEY

import bot.root as root
import bot.conv_constants as cc
import bot.keyboards as kbs

_ = gettext.gettext
kb = None

logger = logging.getLogger(__name__)

def get_title(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    global kb
    global _
    kb = kbs.Keyboards(context.user_data['lang'])
    locale = gettext.translation('compose', localedir = 'locales', languages = [context.user_data['lang']])
    locale.install()
    _ = locale.gettext
    if 'current_survey' not in context.chat_data:
        context.chat_data['current_survey'] = {'id': str(uuid4())}
    context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = _("Введите краткое название опроса.\nЭто название будет отображаться в списке опросов при управлении или запуске опроса.")
        )
    return cc.GET_TITLE_STATE

def save_title(update: Update, context: CallbackContext) -> int:
    context.chat_data['current_survey']['title'] = update.message.text
    update.message.reply_text(update.message.text)
    update.message.reply_text(_("Хотите сохранить это название?"), reply_markup = kb.SAVE_TITLE_KB)
    return cc.SAVE_TITLE_STATE

def get_desc(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = _("Введите описание опроса.\nЭто описание будет отправляться перед опросом для ознакомления.")
        )
    return cc.GET_DESC_STATE

def save_desc(update: Update, context: CallbackContext) -> int:
    context.chat_data['current_survey']['desc'] = update.message.text
    update.message.reply_text(update.message.text)
    update.message.reply_text(_("Хотите сохранить это описание?"), reply_markup = kb.SAVE_DESC_KB)
    return cc.SAVE_DESC_STATE

def get_question(update: Update, context: CallbackContext, returning = False) -> int:
    query = update.callback_query
    query.answer()
    if 'questions' not in context.chat_data['current_survey']:
        context.chat_data['current_survey']['questions'] = []
    if returning:
        context.chat_data['current_survey']['questions'].pop()
    context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = _("Введите текст вопроса №{num}").format(num = len(context.chat_data['current_survey']['questions'])+1)
        )
    return cc.GET_QUESTION_STATE

def save_question(update: Update, context: CallbackContext) -> int:
    context.chat_data['current_survey']['questions'].append({'question': update.message.text})
    update.message.reply_text(update.message.text)
    update.message.reply_text(_("Хотите сохранить этот вопрос?"), reply_markup = kb.SAVE_QUESTION_KB)
    return cc.GET_MULTIANS_STATE

def get_multi(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = _("У этого вопроса должно быть несколько вариантов ответа?"), 
            reply_markup = kb.YES_NO_KB
        )
    return cc.RECORD_MULTIANS_STATE

def save_multi(update: Update, context: CallbackContext, multi: bool) -> int:
    query = update.callback_query
    query.answer()
    context.chat_data['current_survey']['questions'][-1]['multi'] = multi
    if multi:
        query.edit_message_text(_("В этом вопросе можно будет выбрать несколько вариантов ответа"))
    else:
        query.edit_message_text(_("В этом вопросе можно будет выбрать только один вариант ответа"))
    context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = _("Перейти к вводу ответов?"), 
            reply_markup = kb.SAVE_MULTI_KB
        )
    return cc.SAVE_MULTIANS_STATE

def get_answer(update: Update, context: CallbackContext, returning = False) -> int:
    query = update.callback_query
    query.answer()
    if 'answers' not in context.chat_data['current_survey']['questions'][-1]:
        context.chat_data['current_survey']['questions'][-1]['answers'] = []
    if returning:
        context.chat_data['current_survey']['questions'][-1]['answers'].pop()
    context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = _("Введите текст ответа №{num}").format(num = len(context.chat_data['current_survey']['questions'][-1]['answers'])+1)
        )
    return cc.GET_ANSWER_STATE

def record_answer(update: Update, context: CallbackContext) -> int:
    context.chat_data['current_survey']['questions'][-1]['answers'].append(update.message.text)
    update.message.reply_text(update.message.text)
    update.message.reply_text(_("Хотите сохранить этот ответ?"), reply_markup = kb.SAVE_ANSWER_KB)
    return cc.RECORD_ANSWER_STATE

def save_answer(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = _("Выберите действие"),
            reply_markup = kb.NEXT_ANSWER_KB
        )
    return cc.SAVE_ANSWER_STATE

def review(update: Update, context: CallbackContext, returning = False) -> int:
    query = update.callback_query
    query.answer()
    context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = _("Проверьте, правильно ли составлен опрос")
        )
    if not returning:
        surv = context.chat_data['current_survey']
        questions_out = ""
        for question in surv['questions']:
            questions_out.append(question['question'])
            if question['multi']:
                questions_out.append(_(" (можно выбрать несколько вариантов)"))
            else:
                questions_out.append(_(" (можно выбрать только один вариант)"))
            for idx, answer in enumerate(question['answers']):
                questions_out.append(f"\n\t{idx+1}. {answer}")
            questions_out.append("\n\n")
        context.chat_data['survey_out'] = f"{surv['title']}\n{surv['desc']}\n{questions_out}"
    context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = context.chat_data['survey_out']
        )
    context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = _("Выберите действие"), 
            reply_markup = kb.REVIEW_KB
        )
    return cc.REVIEW_STATE

def finish(update: Update, context: CallbackContext, returning = False) -> int:
    query = update.callback_query
    query.answer()
    surv = context.chat_data['current_survey']
    context.bot_data[SURVEYS_KEY].append(surv)
    context.chat_data['current_survey'] = None
    context.chat_data['survey_out'] = None
    root.start(update, context)
    return cc.END