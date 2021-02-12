from telegram.ext import CallbackContext
from telegram import Update
from functools import partial

from bot.constants import SURVEYS_KEY

import bot.root as root
import bot.conv_constants as cc
import bot.keyboards as kb

def pick_part(update: Update, context: CallbackContext, source: str) -> int:
	query = update.callback_query
	query.answer()
	if source == 'compose':
		context.chat_data['edit_end'] = cc.END_COMPOSE
	elif source == 'manage':
		context.chat_data['edit_end'] = cc.END_MANAGE
	context.bot.send_message(
			chat_id = update.effective_chat.id,
			text = 'Что вы хотите отредактировать?', 
			reply_markup = kb.PICK_PART_KB
		)
	return cc.PICK_PART_STATE

def title(update: Update, context: CallbackContext) -> int:
	query = update.callback_query
	query.answer()
	query.edit_message_text(
			text = 'Текущее название: {}'.format(context.chat_data['current_survey']['title']), 
			reply_markup = kb.EDIT_TITLE_KB
		)
	return cc.EDIT_TITLE_STATE

def desc(update: Update, context: CallbackContext) -> int:
	query = update.callback_query
	query.answer()
	query.edit_message_text(
			text = 'Текущее описание: {}'.format(context.chat_data['current_survey']['desc']), 
			reply_markup = kb.EDIT_DESC_KB
		)
	return cc.EDIT_DESC_STATE

def questions(update: Update, context: CallbackContext) -> int:
	query = update.callback_query
	query.answer()
	questions_out = ''
	for idx, question in enumerate(context.chat_data['current_survey']):
		questions_out.append('{}. {}'.format(idx, question['question']))
	try:
	query.edit_message_text(
			text = 'Текущее описание: {}'.format(context.chat_data['current_survey']['desc']), 
		)
	return cc.PICK_QUESTION_STATE

def save_changes(update: Update, context: CallbackContext) -> int: