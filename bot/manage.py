from uuid import uuid4

from telegram.ext import CallbackContext
from telegram import Update

from bot.constants import SURVEYS_NONE, SURVEYS_KEY
from bot.keyboards import (INITIAL_STATE, START_SURVEY_NONE, RETURN_FROM_FIRST_STEP, YES_NO,
						  RETURN_KEYBOARD)

import bot.conv_constants as cc

def start(update: Update, context: CallbackContext)	-> int:
	query = update.callback_query
	user = update.effective_user
	query.answer()
	query.edit_message_text(
        	'Добро пожаловать, {}!'.format(user.first_name), reply_markup = INITIAL_STATE
    )
    context.chat_data['last_handler'] = 'start'
	return cc.START

def start_survey(update: Update, context: CallbackContext) -> int:
	query = update.callback_query
	query.answer()
	bot_data = context.bot_data
	if len(context.bot_data[SURVEYS_KEY].items()) > 0:
		return
	else:
		query.edit_message_text(
        	text = SURVEYS_NONE, reply_markup = START_SURVEY_NONE
    	)
    context.chat_data['last_handler'] = 'start_survey'
	return cc.START_SURV

def get_description(update: Update, context: CallbackContext) -> int:
	query = update.callback_query
	user = update.effective_user
	query.answer()
	try:
		context.bot_data[SURVEYS_KEY].pop(context.chat_data['current_survey'])
	except KeyError:
		pass
	survey_id = uuid4()
	context.bot_data[SURVEYS_KEY][survey_id] = dict()
	context.chat_data['current_survey'] = survey_id
	query.edit_message_text(
        	text = 'Введите краткое название опроса.\n\
        			Это название будет отображаться в списке опросов при управлении или запуске опроса',
        	reply_markup = RETURN_FROM_FIRST_STEP
    )
    context.chat_data['last_handler'] = 'get_description'
	return cc.GET_DESC

def save_description(update: Update, context: CallbackContext) -> int:
	query = update.callback_query
	user = update.effective_user
	sid = context.chat_data['current_survey']
	query.answer()
	update.message.reply_text('Название сохранено!')
	update.message.reply_text('Введите описание опроса, которое будет показываться пользователям в начале опроса',
							   reply_markup = RETURN_KEYBOARD)
	context.chat_data['last_handler'] = 'save_description'
	return cc.SAVE_DESC

def manage_surveys(update: Update, context: CallbackContext) -> int:
	return 34239

def to_prev_step(update: Update, context: CallbackContext) -> int:
	argsdict = {'update': update, 'context': context}
	return globals()[context.chat_data['last_handler']](**argsdict)

def confirm_start_over(update: Update, context: CallbackContext) -> int:
	query = update.callback_query
	user = update.effective_user
	query.answer()
	query.edit_message_text(
        	text = cc.CONFIRM_START_OVER,
        	reply_markup = YES_NO
    )
    return START_OVER

def confirm_return_to_main(update: Update, context: CallbackContext) -> int:
	query = update.callback_query
	user = update.effective_user
	query.answer()
	query.edit_message_text(
        	text = cc.CONFIRM_RETURN_TO_MAIN,
        	reply_markup = YES_NO
    )
    return MAIN_MENU


