from telegram.ext import CallbackContext
from telegram import Update
from functools import partial

from bot.constants import SURVEYS_KEY

import bot.manage as manage
import bot.conv_constants as cc
import bot.keyboards as kb

def pick_survey(update: Update, context: CallbackContext, returning = False) -> int:
	if not returning:
		surveys = context.bot_data[SURVEYS_KEY]
		context.chat_data['surveys_out'] = ["{}. {}\n".format(idx, survey['title']) for idx, survey in enumerate(surveys)]
	update.message.reply_text('Выберите опрос\n\n{}\n\nДля выбора напишите номер нужного опроса'.format(context.chat_data['surveys_out']), reply_markup = kb.MAIN_MENU_KB)
	return cc.PICK_SURVEY_STATE

def pick_part(update: Update, context: CallbackContext) -> int:
	query = update.callback_query
	query.answer()
	try:
		context.chat_data['idx'] = int(update.message.text)
		try:
			context.chat_data['current_survey'] = context.bot_data[SURVEYS_KEY][context.chat_data['idx']-1]
			update.message.reply_text('Что вы хотите отредактировать?', reply_markup = kb.PICK_PART_KB)
			return cc.PICK_PART_STATE
		except IndexError:
			update.message.reply_text('Опроса с таким номером не существует! Попробуйте ещё раз')
			return cc.PICK_SURVEY_STATE
	except ValueError:
		update.message.reply_text('Неправильно введён номер! Попробуйте ещё раз')
		return cc.PICK_SURVEY_STATE

def title(update: Update, context: CallbackContext) -> int:
	query = update.callback_query
	query.answer()
	update.message.reply_text('Текущее название: {}'.format(context.chat_data['current_survey']['title']), reply_markup = kb.EDIT_TITLE_KB)
	return cc.EDIT_TITLE_STATE