import gettext
import logging

from telegram.ext import CallbackContext
from telegram import Update
from functools import partial

from bot.constants import SURVEYS_KEY

import bot.root as root
import bot.constants as consts
import bot.conv_constants as cc
import bot.keyboards as kbs
import bot.utils as utils

_ = gettext.gettext
kb = None

logger = logging.getLogger(__name__)

def pick_part(update: Update, context: CallbackContext, source: str, idx = None) -> int:
    query = update.callback_query
    query.answer()
    global _
    global kb
    kb = kbs.Keyboards(context.user_data['lang'])
    locale = gettext.translation('edit', localedir = 'locales', languages = [context.user_data['lang']])
    locale.install()
    _ = locale.gettext
    if idx is not None:
        context.chat_data['s_idx'] = idx
    if source == 'compose':
        context.chat_data['edit_end'] = cc.END_COMPOSE
    elif source == 'manage':
        context.chat_data['edit_end'] = cc.END_MANAGE
    context.chat_data['base_ver'] = context.chat_data['current_survey']
    if 'base_ver' not in context.chat_data:
        context.chat_data['base_ver'] = context.chat_data['current_survey']
    if context.chat_data['base_ver'] != context.chat_data['current_survey']:
        changes = utils.surv_diff(context.chat_data['base_ver'], context.chat_data['current_survey'])
    else:
        changes = ""
    context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = changes + _("Что вы хотите отредактировать?"), 
            reply_markup = kb.PICK_PART_KB
        )
    return cc.PICK_PART_STATE

def title(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(
            text = _("Текущее название: {title}").format(title = context.chat_data['current_survey']['title']), 
            reply_markup = kb.EDIT_TITLE_KB
        )
    return cc.EDIT_TITLE_STATE

def desc(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(
            text = _("Текущее описание: {desc}").format(desc = context.chat_data['current_survey']['desc']), 
            reply_markup = kb.EDIT_DESC_KB
        )
    return cc.EDIT_DESC_STATE

def questions(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    context.chat_data.pop('q_idx', None)
    q_list = [question['question'] for question in context.chat_data['current_survey']['questions']]
    questions_out = utils.num_list(q_list)
    query.edit_message_text(
            text = _("Список текущих вопросов: \n{list}\n\nДля выбора вопроса отправьте его номер в списке").format(list = questions_out) 
        )
    return cc.PICK_QUESTION_STATE

def question(update: Update, context: CallbackContext) -> int:
    # query = update.callback_query
    # query.answer()
    questions = context.chat_data['current_survey']['questions']
    if 'q_idx' not in context.chat_data:
        try:
            idx = utils.validate_index(update.message.text, questions)
            context.chat_data['q_idx'] = idx
            context.chat_data['current_question'] = questions['q_idx']
        except IndexError:
            update.message.reply_text(
                        text = _("Введённого номера нет в списке! Попробуйте ещё раз"),
                    )
            return cc.PICK_QUESTION_STATE
        except ValueError:
            update.message.reply_text(
                        text = _("Неправильно введён номер! Попробуйте ещё раз"),
                    )
            return cc.PICK_QUESTION_STATE
    update.message.reply_text(
            text = _("Что вы хотите отредактировать?"),
            reply_markup = kb.EDIT_QUESTION_KB
        )
    # query.edit_message_text(
    #         text = _("Что вы хотите отредактировать?"),
    #         reply_markup = kb.EDIT_QUESTION_KB
    #     )
    return cc.PICK_QUESTION_PART_STATE

def question_text(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    question = context.chat_data['current_question']
    query.edit_message_text(
            text = _("Текущий текст вопроса: {question}").format(question = context.chat_data['current_question']['question']),
            reply_markup = kb.EDIT_QUESTION_TEXT_KB
        )
    return cc.EDIT_QUESTION_TEXT_STATE

def multi(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    question = context.chat_data['current_question']
    multi = _("несколько вариантов") if question['multi'] else _("один вариант")
    query.edit_message_text(
            text = _("В этом вопросе пользователи могут выбрать {multi} ответа").format(multi = multi),
            reply_markup = kb.EDIT_MULTI_KB
        )
    return cc.EDIT_MULTI_STATE

def answers(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(
            text = _("Выберите действие"),
            reply_markup = kb.EDIT_ANSWER_OPTIONS_KB
        )
    return cc.EDIT_ANSWER_OPTIONS_STATE

def pick_answer(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    question = context.chat_data['current_question']
    answers_out = utils.num_list(question['answers'])
    query.edit_message_text(
            text = _("Список ответов к текущему вопросу: \n{list}\n\nДля выбора ответа отправьте его номер в списке"
                ).format(list = answers_out),
            reply_markup = kb.RETURN_FROM_FIRST_STEP_KB
        )
    return cc.PICK_ANSWER_STATE

def answer(update: Update, context: CallbackContext) -> int:
    # query = update.callback_query
    # query.answer()
    answers = context.chat_data['current_question']['answers']
    if 'a_idx' not in context.chat_data:
        try:
            idx = utils.validate_index(update.message.text, answers)
            context.chat_data['a_idx'] = idx
            context.chat_data['current_answer'] = answers[idx]
        except IndexError:
            update.message.reply_text(
                        text = _("Введённого номера нет в списке! Попробуйте ещё раз"),
                    )
            return cc.PICK_ANSWER_STATE
        except ValueError:
            update.message.reply_text(
                        text = _("Неправильно введён номер! Попробуйте ещё раз"),
                    )
            return cc.PICK_ANSWER_STATE
    update.message.reply_text(
            text = _("Выберите действие"),
            reply_markup = kb.EDIT_ANSWER_KB
        )
    # query.edit_message_text(
    #         text = _("Что вы хотите отредактировать?"),
    #         reply_markup = kb.EDIT_QUESTION_KB
    #     )
    return cc.EDIT_ANSWER_STATE

def remove_answer_confirm(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(
            text = _("{answer}\n\nВы уверены, что хотите удалить этот ответ?"
                ).format(answer = context.chat_data['current_answer']),
            reply_markup = kb.YES_NO_KB
        )
    return cc.REMOVE_ANSWER_CONFIRM_STATE

def remove_answer(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    idx = context.chat_data['a_idx']
    del context.chat_data['current_question']['answers'][idx]
    del context.chat_data['a_idx']
    query.edit_message_text(
            text = _("Ответ был удалён")
        )
    question = context.chat_data['current_question']
    answers_out = utils.num_list(question['answers'])
    context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = _("Список ответов к текущему вопросу: \n{list}\n\nДля выбора ответа отправьте его номер в списке"
                ).format(list = answers_out),
            reply_markup = kb.RETURN_FROM_FIRST_STEP_KB
        )
    return cc.PICK_ANSWER_STATE

def save_changes(update: Update, context: CallbackContext) -> int:
    end_state = context.chat_data['edit_end']
    del context.chat_data['edit_end']
    if 's_idx' in context.chat_data:
        idx = context.chat_data['s_idx']
    else:
        survey_id = context.chat_data['current_survey']['id']
        idx = next((index for (index, d) in enumerate(context.bot_data[consts.SURVEY_KEY]) if d["id"] == survey_id), None)
    context.bot_data[consts.SURVEY_KEY][idx] = context.chat_data['current_survey']
    del context.chat_data['current_survey']
    return end_state