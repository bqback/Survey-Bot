from uuid import uuid4

from telegram.ext import CallbackContext
from telegram import Update
from functools import partial

from bot.constants import SURVEYS_KEY

import bot.manage as manage
import bot.conv_constants as cc
import bot.keyboards as kb

def get_title(update: Update, context: CallbackContext) -> int:
	query = update.callback_query
	query.answer()
	context.chat_data['current_survey'] = {'id': str(uuid4())}
	context.bot.send_message(
			chat_id = update.effective_chat.id,
			text = 'Введите краткое название опроса.\nЭто название будет отображаться в списке опросов при управлении или запуске опроса.'
		)
	return cc.GET_TITLE_STATE

def save_title(update: Update, context: CallbackContext) -> int:
	context.chat_data['current_survey']['title'] = update.message.text
	update.message.reply_text(update.message.text)
	update.message.reply_text('Сохранить название?', reply_markup = kb.SAVE_TITLE_KB)
	return cc.SAVE_TITLE_STATE

def get_desc(update: Update, context: CallbackContext) -> int:
	query = update.callback_query
	query.answer()
	context.bot.send_message(
			chat_id = update.effective_chat.id,
			text = 'Введите описание опроса.\nЭто описание будет отправляться перед опросом для ознакомления.'
		)
	return cc.GET_DESC_STATE

def save_desc(update: Update, context: CallbackContext) -> int:
	context.chat_data['current_survey']['desc'] = update.message.text
	update.message.reply_text(update.message.text)
	update.message.reply_text('Сохранить описание?', reply_markup = kb.SAVE_DESC_KB)
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
			text = 'Введите текст вопроса №{}.'.format(len(context.chat_data['current_survey']['questions'])+1)
		)
	return cc.GET_QUESTION_STATE

def save_question(update: Update, context: CallbackContext) -> int:
	context.chat_data['current_survey']['questions'].append({'question': update.message.text})
	update.message.reply_text(update.message.text)
	update.message.reply_text('Сохранить вопрос?', reply_markup = kb.SAVE_QUESTION_KB)
	return cc.GET_MULTIANS_STATE

def get_multi(update: Update, context: CallbackContext) -> int:
	query = update.callback_query
	query.answer()
	context.bot.send_message(
			chat_id = update.effective_chat.id,
			text = 'У этого вопроса несколько вариантов ответа?', 
			reply_markup = kb.YES_NO_KB
		)
	return cc.RECORD_MULTIANS_STATE

def save_multi(update: Update, context: CallbackContext, multi: bool) -> int:
	query = update.callback_query
	query.answer()
	context.chat_data['current_survey']['questions'][-1]['multi'] = multi
	if multi:
		query.edit_message_text('В этом вопросе можно будет выбрать несколько вариантов ответа')
	else:
		query.edit_message_text('В этом вопросе можно будет выбрать только один вариант ответа')
	context.bot.send_message(
			chat_id = update.effective_chat.id,
			text = 'Перейти к вводу ответов?', 
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
			text = 'Введите текст ответа №{}.'.format(len(context.chat_data['current_survey']['questions'][-1]['answers'])+1)
		)
	return cc.GET_ANSWER_STATE

def record_answer(update: Update, context: CallbackContext) -> int:
	context.chat_data['current_survey']['questions'][-1]['answers'].append(update.message.text)
	update.message.reply_text(update.message.text)
	update.message.reply_text('Сохранить ответ?', reply_markup = kb.SAVE_ANSWER_KB)
	return cc.RECORD_ANSWER_STATE

def save_answer(update: Update, context: CallbackContext) -> int:
	query = update.callback_query
	query.answer()
	context.bot.send_message(
			chat_id = update.effective_chat.id,
			text = 'Выберите действие', 
			reply_markup = kb.NEXT_ANSWER_KB
		)
	return cc.SAVE_ANSWER_STATE

def review(update: Update, context: CallbackContext, returning = False) -> int:
	query = update.callback_query
	query.answer()
	context.bot.send_message(
			chat_id = update.effective_chat.id,
			text = 'Проверьте, правильно ли составлен опрос'
		)
	if not returning:
		surv = context.chat_data['current_survey']
		questions_out = ""
		for question in surv['questions']:
			questions_out.append(question['question'])
			if question['multi']:
				questions_out.append(" (можно выбрать несколько вариантов)")
			else:
				questions_out.append(" (можно выбрать только один вариант)")
			for idx, answer in enumerate(question['answers']):
				questions_out.append("\n{}. {}".format(idx+1, answer))
			questions_out.append("\n\n")
		context.chat_data['survey_out'] = '{}\n{}\n{}'.format(surv['title'], surv['desc'], questions_out)
	context.bot.send_message(
			chat_id = update.effective_chat.id,
			text = context.chat_data['survey_out']
		)
	context.bot.send_message(
			chat_id = update.effective_chat.id,
			text = 'Выберите действие', 
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
	manage.start(update, context)
	return cc.END