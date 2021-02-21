import gettext
import logging

from uuid import uuid4

from telegram.ext import CallbackContext
from telegram import Update
from functools import partial

import bot.constants as consts
import bot.root as root
import bot.conv_constants as cc
import bot.keyboards as kbs

_ = gettext.gettext
kb = None

logger = logging.getLogger(__name__)

def get_title(update: Update, context: CallbackContext, mode = 'compose') -> int:
    query = update.callback_query
    query.answer()
    global kb
    global _
    kb = kbs.Keyboards(context.user_data['lang'])
    locale = gettext.translation('compose', localedir = 'locales', languages = [context.user_data['lang']])
    locale.install()
    _ = locale.gettext
    if mode == 'compose':
        if 'current_survey' not in context.chat_data or query.data == cc.NO_CB:
            context.chat_data['current_survey'] = {'id': str(uuid4())}
            context.chat_data['current_step'] = 'get_title'
            context.chat_data['current_state'] = cc.GET_TITLE_STATE
            query.edit_message_text(
                    text = _("Введите краткое название опроса.\nЭто название будет отображаться в списке опросов при управлении или запуске опроса.")
                )
        else:
            query.edit_message_text(
                    text = _("Обнаружен незавершённый опрос.\nХотите продолжить его создание?"),
                    reply_markup = kb.YES_NO_KB
                )
    if mode == 'edit':
        query.edit_message_text(
                    text = _("Введите краткое название опроса.\nЭто название будет отображаться в списке опросов при управлении или запуске опроса.")
                )
    return cc.GET_TITLE_STATE

def save_title(update: Update, context: CallbackContext) -> int:
    context.chat_data['current_survey']['title'] = update.message.text
    update.message.reply_text(update.message.text)
    update.message.reply_text(_("Хотите сохранить это название?"), reply_markup = kb.SAVE_TITLE_KB)
    return cc.SAVE_TITLE_STATE

def get_desc(update: Update, context: CallbackContext, mode = 'compose') -> int:
    query = update.callback_query
    query.answer()
    global kb
    global _
    kb = kbs.Keyboards(context.user_data['lang'])
    locale = gettext.translation('compose', localedir = 'locales', languages = [context.user_data['lang']])
    locale.install()
    _ = locale.gettext
    if mode == 'compose':
        context.chat_data['current_step'] = 'get_desc'
        context.chat_data['current_state'] = cc.GET_DESC_STATE
    query.edit_message_text(
            text = _("Введите описание опроса.\nЭто описание будет отправляться перед опросом для ознакомления.")
        )
    return cc.GET_DESC_STATE

def save_desc(update: Update, context: CallbackContext) -> int:
    context.chat_data['current_survey']['desc'] = update.message.text
    update.message.reply_text(update.message.text)
    update.message.reply_text(_("Хотите сохранить это описание?"), reply_markup = kb.SAVE_DESC_KB)
    return cc.SAVE_DESC_STATE

def get_question(update: Update, context: CallbackContext, mode = 'compose', returning = False) -> int:
    query = update.callback_query
    query.answer()
    global kb
    global _
    kb = kbs.Keyboards(context.user_data['lang'])
    locale = gettext.translation('compose', localedir = 'locales', languages = [context.user_data['lang']])
    locale.install()
    _ = locale.gettext
    if mode == 'compose':
        context.chat_data['current_step'] = 'get_question'
        context.chat_data['current_state'] = cc.GET_QUESTION_STATE
        if 'questions' not in context.chat_data['current_survey']:
            context.chat_data['current_survey']['questions'] = []
        if returning:
            context.chat_data['current_survey']['questions'].pop()
        query.edit_message_text(
                text = _("Введите текст вопроса №{num}").format(num = len(context.chat_data['current_survey']['questions'])+1)
            )
    elif mode == 'edit':
        q_idx = context.chat_data['q_idx']
        query.edit_message_text(
                text = _("Введите текст вопроса №{num}").format(num = q_idx + 1)
            )
    return cc.GET_QUESTION_STATE

def save_question(update: Update, context: CallbackContext, mode = 'compose') -> int:
    if mode == 'compose':
        context.chat_data['current_survey']['questions'].append({'question': update.message.text})      
    elif mode == 'edit':
        context.chat_data['question'] = update.message.text
    update.message.reply_text(update.message.text)
    update.message.reply_text(_("Хотите сохранить этот вопрос?"), reply_markup = kb.SAVE_QUESTION_KB)
    return cc.SAVE_QUESTION_STATE      
    
def get_multi(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    global kb
    global _
    kb = kbs.Keyboards(context.user_data['lang'])
    locale = gettext.translation('compose', localedir = 'locales', languages = [context.user_data['lang']])
    locale.install()
    _ = locale.gettext
    query.edit_message_text(
            text = _("У этого вопроса должно быть несколько вариантов ответа?"), 
            reply_markup = kb.YES_NO_KB
        )
    return cc.GET_MULTIANS_STATE

def save_multi(update: Update, context: CallbackContext, multi: bool, mode = 'compose') -> int:
    query = update.callback_query
    query.answer()
    if mode == 'compose':
        context.chat_data['current_survey']['questions'][-1]['multi'] = multi
        if multi:
            text = _("В этом вопросе можно будет выбрать несколько вариантов ответа")
        else:
            text = _("В этом вопросе можно будет выбрать только один вариант ответа")
        text += _("\n\nПерейти к вводу ответов?")
        query.edit_message_text(
                text = text, 
                reply_markup = kb.SAVE_MULTI_KB
            )
    elif mode == 'edit':
        context.chat_data['multi'] = multi
        if multi:
            text = _("В этом вопросе можно будет выбрать несколько вариантов ответа")
        else:
            text = _("В этом вопросе можно будет выбрать только один вариант ответа")
        text += _("\n\nСохранить?")
        query.edit_message_text(
                text = text, 
                reply_markup = kb.SAVE_MULTI_KB
            )
    return cc.SAVE_MULTIANS_STATE

def get_answer(update: Update, context: CallbackContext, mode = 'compose', returning = False) -> int:
    query = update.callback_query
    query.answer()
    global kb
    global _
    kb = kbs.Keyboards(context.user_data['lang'])
    locale = gettext.translation('compose', localedir = 'locales', languages = [context.user_data['lang']])
    locale.install()
    _ = locale.gettext
    if mode == 'compose':
        context.chat_data['current_step'] = 'get_answer'
        context.chat_data['current_state'] = cc.GET_ANSWER_STATE
        if 'answers' not in context.chat_data['current_survey']['questions'][-1]:
            context.chat_data['current_survey']['questions'][-1]['answers'] = []
        if returning:
            context.chat_data['current_survey']['questions'][-1]['answers'].pop()
        query.edit_message_text(
                text = _("Введите текст ответа №{a_num} к вопросу №{q_num}"
                    ).format(a_num = len(context.chat_data['current_survey']['questions'][-1]['answers'])+1,
                            q_num = len(context.chat_data['current_survey']['questions']))
            )
    elif mode == 'edit':
        q_idx = context.chat_data['q_idx']
        a_idx = context.chat_data['a_idx']
        query.edit_message_text(
                text = _("Введите текст ответа №{a_num} к вопросу №{q_num}"
                    ).format(a_num = a_idx+1,
                            q_num = q_idx+1)
            )
    return cc.GET_ANSWER_STATE

def save_answer(update: Update, context: CallbackContext, mode = 'compose') -> int:
    if mode == 'compose':
        context.chat_data['current_survey']['questions'][-1]['answers'].append(update.message.text)
    elif mode == 'edit':
        context.chat_data['answers'] = update.message.text
    update.message.reply_text(update.message.text)
    update.message.reply_text(_("Хотите сохранить этот ответ?"), reply_markup = kb.SAVE_ANSWER_KB)
    return cc.SAVE_ANSWER_STATE

def checkpoint(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(
            text = _("Выберите действие"),
            reply_markup = kb.NEXT_ANSWER_KB
        )
    return cc.SAVE_ANSWER_STATE

def review(update: Update, context: CallbackContext, returning = False) -> int:
    query = update.callback_query
    if query is not None:
        query.answer()
        context.bot.send_message(
                chat_id= update.effective_chat.id,
                text = _("Проверьте, правильно ли составлен опрос")
            )
    else:
        query.edit_message_text(
                text = _("Проверьте, правильно ли составлен опрос")
            )
    context.chat_data['current_step'] = 'review'
    context.chat_data['current_state'] = cc.REVIEW_STATE
    if not returning:
        surv = context.chat_data['current_survey']
        questions_out = ""
        for question in surv['questions']:
            questions_out += question['question']
            if question['multi']:
                questions_out += _(" (можно выбрать несколько вариантов)")
            else:
                questions_out += _(" (можно выбрать только один вариант)")
            for idx, answer in enumerate(question['answers']):
                questions_out += f"\n\t{idx+1}. {answer}"
            questions_out += "\n\n"
        context.chat_data['survey_out'] = f"{surv['title']}\n\n{surv['desc']}\n\n{questions_out}"
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
    context.bot_data[consts.SURVEYS_KEY].append(surv)
    del context.chat_data['current_survey']
    del context.chat_data['survey_out']
    root.start(update, context)
    return cc.END

def return_to_step(update: Update, context: CallbackContext) -> int:
    argsdict = {'update': update, 'context': context}
    globals()[context.chat_data['current_step']](**argsdict)
    return context.chat_data['current_state']