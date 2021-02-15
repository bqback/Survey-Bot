import gettext

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

def get_title(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    global text
    global kb
    if not text:
        text = importlib.import_module(f"locale.{context.user_data['lang']}")
        kb = kbs.Keyboards(context.user_data['lang'])
    if 'current_survey' not in context.chat_data:
        context.chat_data['current_survey'] = {'id': str(uuid4())}
    context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = f"{text.ENTER_TITLE}"
        )
    return cc.GET_TITLE_STATE

def save_title(update: Update, context: CallbackContext) -> int:
    context.chat_data['current_survey']['title'] = update.message.text
    update.message.reply_text(update.message.text)
    update.message.reply_text(f"{text.SAVE_TITLE_TEXT}", reply_markup = kb.SAVE_TITLE_KB)
    return cc.SAVE_TITLE_STATE

def get_desc(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = f"{text.ENTER_DESC}"
        )
    return cc.GET_DESC_STATE

def save_desc(update: Update, context: CallbackContext) -> int:
    context.chat_data['current_survey']['desc'] = update.message.text
    update.message.reply_text(update.message.text)
    update.message.reply_text(f"{text.SAVE_DESC_TEXT}", reply_markup = kb.SAVE_DESC_KB)
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
            text = f"{text.ENTER_QUESTION}{len(context.chat_data['current_survey']['questions'])+1}"
        )
    return cc.GET_QUESTION_STATE

def save_question(update: Update, context: CallbackContext) -> int:
    context.chat_data['current_survey']['questions'].append({'question': update.message.text})
    update.message.reply_text(update.message.text)
    update.message.reply_text(f"{text.SAVE_QUESTION_TEXT}", reply_markup = kb.SAVE_QUESTION_KB)
    return cc.GET_MULTIANS_STATE

def get_multi(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = f"{text.ENTER_MULTI}", 
            reply_markup = kb.YES_NO_KB
        )
    return cc.RECORD_MULTIANS_STATE

def save_multi(update: Update, context: CallbackContext, multi: bool) -> int:
    query = update.callback_query
    query.answer()
    context.chat_data['current_survey']['questions'][-1]['multi'] = multi
    if multi:
        query.edit_message_text(f"{text.MULTI_TRUE}")
    else:
        query.edit_message_text(f"{text.MULTI_FALSE}")
    context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = f"{text.START_ANSWERS}", 
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
            text = f"{text.ENTER_ANSWER}{len(context.chat_data['current_survey']['questions'][-1]['answers'])+1}"
        )
    return cc.GET_ANSWER_STATE

def record_answer(update: Update, context: CallbackContext) -> int:
    context.chat_data['current_survey']['questions'][-1]['answers'].append(update.message.text)
    update.message.reply_text(update.message.text)
    update.message.reply_text(f'{text.SAVE_ANSWER_TEXT}', reply_markup = kb.SAVE_ANSWER_KB)
    return cc.RECORD_ANSWER_STATE

def save_answer(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = f"{text.CHOOSE_ACTION}",
            reply_markup = kb.NEXT_ANSWER_KB
        )
    return cc.SAVE_ANSWER_STATE

def review(update: Update, context: CallbackContext, returning = False) -> int:
    query = update.callback_query
    query.answer()
    context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = f"{text.REVIEW_SURVEY}"
        )
    if not returning:
        surv = context.chat_data['current_survey']
        questions_out = ""
        for question in surv['questions']:
            questions_out.append(question['question'])
            if question['multi']:
                questions_out.append(f" {text.MULTI_CHOICE}")
            else:
                questions_out.append(f" {text.SINGLE_CHOICE}")
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
            text = f'{text.CHOOSE_ACTION}', 
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