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

def pick_part(update: Update, context: CallbackContext, source = None, idx = None) -> int:
    query = update.callback_query
    query.answer()
    global _
    global kb
    kb = kbs.Keyboards(context.user_data['lang'])
    locale = gettext.translation('edit', localedir = 'locales', languages = [context.user_data['lang']])
    locale.install()
    _ = locale.gettext
    if idx is None:
        idx = context.chat_data['s_idx']
        context.chat_data['current_survey'] = context.bot_data[consts.SURVEYS_KEY][idx]
    if source == 'compose':
        context.chat_data['edit_end'] = cc.END_COMPOSE
    elif source == 'manage':
        context.chat_data['edit_end'] = cc.END_MANAGE
    if 'base_ver' not in context.chat_data:
        context.chat_data['base_ver'] = context.chat_data['current_survey']
    if context.chat_data['base_ver'] != context.chat_data['current_survey']:
        changes = utils.surv_diff(context.chat_data['base_ver'], context.chat_data['current_survey'], context.user_data['lang'])
    else:
        changes = ""
    query.edit_message_text(
            text = _("Выбран опрос '{title}'\n\n").format(title = context.chat_data['current_survey']['title']) + 
                       changes + 
                    _("\nЧто вы хотите отредактировать?"), 
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

def pick_question(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    context.chat_data.pop('q_idx', None)
    q_list = [question['question'] for question in context.chat_data['current_survey']['questions']]
    questions_out = utils.num_list(q_list)
    query.edit_message_text(
            text = _("Список вопросов: \n\n{list}\nДля выбора вопроса отправьте его номер в списке"
                ).format(list = questions_out),
            reply_markup = kb.RETURN_FROM_FIRST_STEP_KB
        )
    return cc.PICK_QUESTION_STATE

def question(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    if query is None:
        questions = context.chat_data['current_survey']['questions']
        if 'q_idx' not in context.chat_data:
            try:
                idx = utils.validate_index(update.message.text, questions)
                context.chat_data['q_idx'] = idx
                context.chat_data['current_question'] = questions[idx]
                update.message.reply_text(
                        text = _("Что вы хотите отредактировать?"),
                        reply_markup = kb.EDIT_QUESTION_PART_KB
                    )
                return cc.PICK_QUESTION_PART_STATE
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
    else:
        query.answer()
        query.edit_message_text(
                text = _("Что вы хотите отредактировать?"),
                reply_markup = kb.EDIT_QUESTION_PART_KB
            )
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

def remove_question_confirm(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(
            text = _("{question}\n\nВы уверены, что хотите удалить этот вопрос?"
                ).format(question = context.chat_data['current_question']['question']),
            reply_markup = kb.YES_NO_KB
        )
    return cc.REMOVE_QUESTION_CONFIRM_STATE

def remove_question(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    idx = context.chat_data['q_idx']
    del context.chat_data['current_question']['questions'][idx]
    del context.chat_data['q_idx']
    query.edit_message_text(
            text = _("Вопрос был удалён")
        )
    q_list = [question['question'] for question in context.chat_data['current_survey']['questions']]
    questions_out = utils.num_list(q_list)
    context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = _("Список вопросов: \n{list}\n\nДля выбора ответа отправьте его номер в списке"
                ).format(list = questions_out),
            reply_markup = kb.RETURN_FROM_FIRST_STEP_KB
        )
    return cc.PICK_QUESTION_STATE

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
    return cc.EDIT_ANSWERS_STATE

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
    query = update.callback_query
    if query is None:
        answers = context.chat_data['current_question']['answers']
        if 'a_idx' not in context.chat_data:
            try:
                idx = utils.validate_index(update.message.text, answers)
                context.chat_data['a_idx'] = idx
                context.chat_data['current_answer'] = answers[idx]
                update.message.reply_text(
                        text = _("Выберите действие"),
                        reply_markup = kb.EDIT_ANSWER_KB
                    )
                return cc.EDIT_ANSWER_STATE
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
        else:
            update.message.reply_text(
                    text = _("Выберите действие"),
                    reply_markup = kb.EDIT_ANSWER_KB
                )
            return cc.EDIT_ANSWER_STATE
    else:
        query.answer()
        query.edit_message_text(
                text = _("Выберите действие"),
                reply_markup = kb.EDIT_ANSWER_KB
            )
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

def save_result(update: Update, context: CallbackContext, result: str) -> int:
    query = update.callback_query
    query.answer()
    q_idx = context.chat_data['q_idx']
    del context.chat_data['q_idx']
    if result == 'question':
        context.chat_data['current_survey']['questions'][q_idx][result] = context.chat_data[result]
        del context.chat_data[result]
        query.edit_message_text(
                text = _("Новый текст вопроса сохранён\n\nКуда вы хотите перейти?"),
                reply_markup = kb.EDIT_AFTER_SAVE_KB
            )
    if result == 'multi':
        context.chat_data['current_survey']['questions'][q_idx][result] = context.chat_data[result]
        del context.chat_data[result]
        query.edit_message_text(
                text = _("Новое число вариантов ответа сохранено\n\nКуда вы хотите перейти?"),
                reply_markup = kb.EDIT_AFTER_SAVE_KB
            )
    if result == 'answers':
        a_idx = context.chat_data['a_idx']
        del context.chat_data['a_idx']
        context.chat_data['current_survey']['questions'][q_idx][result][a_idx] = context.chat_data[result]
        query.edit_message_text(
                text = _("Новый ответ сохранён\n\nКуда вы хотите перейти?"),
                reply_markup = kb.EDIT_AFTER_SAVE_KB
            )
    return cc.EDIT_AFTER_SAVE_STATE

def save_confirm(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    changes = utils.surv_diff(context.chat_data['base_ver'], context.chat_data['current_survey'], context.user_data['lang'])
    query.edit_message_text(
            text = changes + _("\n\nВы уверены, что хотите сохранить эти изменения?"),
            reply_markup = kb.YES_NO_KB
        )
    return cc.SAVE_CONFIRM_STATE

def discard_confirm(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    changes = utils.surv_diff(context.chat_data['base_ver'], context.chat_data['current_survey'], context.user_data['lang'])
    query.edit_message_text(
            text = changes + _("\n\nВы уверены, что хотите избавиться от этих изменений?"),
            reply_markup = kb.YES_NO_KB
        )
    return cc.DISCARD_CONFIRM_STATE

def discard_changes(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    end_state = context.chat_data['edit_end']
    del context.chat_data['edit_end']
    del context.chat_data['base_ver']
    del context.chat_data['current_survey']
    if end_state == cc.END_MANAGE:
        query.edit_message_text(
                text = _("Изменения удалены!\n\nВыберите действие"),
                reply_markup = kb.MANAGE_SURVEYS_KB
            )
    if end_state == cc.END_COMPOSE:
        query.edit_message_text(
                text = _("Изменения удалены!"),
            )
    return end_state

def save_changes(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    end_state = context.chat_data['edit_end']
    del context.chat_data['edit_end']
    if end_state == cc.END_MANAGE:
        if 's_idx' in context.chat_data:
            idx = context.chat_data['s_idx']
            del context.chat_data['s_idx']
        else:
            survey_id = context.chat_data['current_survey']['id']
            idx = next((index for (index, d) in enumerate(context.bot_data[consts.SURVEY_KEY]) if d["id"] == survey_id), None)
        context.bot_data[consts.SURVEYS_KEY][idx] = context.chat_data['current_survey']
        del context.chat_data['current_survey']
        del context.chat_data['base_ver']
        query.edit_message_text(
                text = _("Изменения сохранены!\n\nВыберите действие"),
                reply_markup = kb.MANAGE_SURVEYS_KB
            )
    if end_state == cc.END_COMPOSE:
        del context.chat_data['base_ver']
        query.edit_message_text(
                text = _("Изменения сохранены!"),
            )
    return end_state
    