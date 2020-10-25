from uuid import uuid4

from telegram.ext import CallbackContext
from telegram import Update

from bot.constants import SURVEYS_NONE, SURVEYS_KEY
from bot.keyboards import (INITIAL_STATE_KB, START_SURVEY_NONE_KB, RETURN_FROM_FIRST_STEP_KB, YES_NO_KB,
						  RETURN_KB, MANAGE_SURVEYS_KB)

import bot.conv_constants as cc

def start(update: Update, context: CallbackContext)	-> int:
	query = update.callback_query
	user = update.effective_user
	query.answer()
	query.edit_message_text(
        	'Добро пожаловать, {}!'.format(user.first_name), reply_markup = INITIAL_STATE_KB
    )	
	context.chat_data['last_handler'] = 'start'
	return cc.START_STATE

def start_survey(update: Update, context: CallbackContext) -> int:
	query = update.callback_query
	query.answer()
	bot_data = context.bot_data
	if len(context.bot_data[SURVEYS_KEY].items()) > 0:
		return
	else:
		query.edit_message_text(
        	text = SURVEYS_NONE, reply_markup = START_SURVEY_NONE_KB
    	)
	context.chat_data['last_handler'] = 'start_survey'
	return cc.START_SURVEY_STATE

def get_title(update: Update, context: CallbackContext) -> int:
	query = update.callback_query
	user = update.effective_user
	query.answer()
	context.chat_data['current_survey'] = {'id': uuid4()}
	query.edit_message_text(
        	text = 'Введите краткое название опроса.\nЭто название будет отображаться в списке опросов при управлении или запуске опроса',
        	reply_markup = RETURN_FROM_FIRST_STEP_KB
    )
	context.chat_data['last_handler'] = 'get_title'
	return cc.GET_TITLE_STATE

def save_title(update: Update, context: CallbackContext) -> int:

	context.chat_data['current_survey']['title'] = update.message.text
	update.message.reply_text('Название сохранено!')
	update.message.reply_text('Введите описание опроса, которое будет показываться пользователям в начале опроса',
							   reply_markup = RETURN_KB)
	context.chat_data['last_handler'] = 'save_title'
	return cc.SAVE_TITLE_STATE

def manage_surveys(update: Update, context: CallbackContext) -> int:
	update.message.reply_text('Выберите действие', reply_markup = MANAGE_SURVEYS_KB)

	return cc.MANAGE_SURVEYS_STATE

def to_prev_step(update: Update, context: CallbackContext) -> int:
	argsdict = {'update': update, 'context': context}
	return globals()[context.chat_data['last_handler']](**argsdict)

def confirm_start_over(update: Update, context: CallbackContext) -> int:
	query = update.callback_query
	user = update.effective_user
	query.answer()
	query.edit_message_text(
        	text = cc.CONFIRM_START_OVER,
        	reply_markup = YES_NO_KB
    )
	return cc.START_OVER_STATE

def confirm_return_to_main(update: Update, context: CallbackContext) -> int:
	query = update.callback_query
	user = update.effective_user
	query.answer()
	query.edit_message_text(
        	text = cc.CONFIRM_RETURN_TO_MAIN,
        	reply_markup = YES_NO_KB
    )
	return cc.MAIN_MENU_STATE


