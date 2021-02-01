from telegram.ext import CallbackContext
from telegram import Update
from functools import partial

from bot.constants import SURVEYS_KEY

import bot.manage as manage
import bot.conv_constants as cc
import bot.keyboards as kb

def pick_survey(update: Update, context: CallbackContext, returning = False) -> int:
	if not returning:
		surveys = context.bot_data[SURVEYS_KEY]:
		context.chat_data['surveys_out'] = ["{}. {}\n".format(idx, survey['title']) for idx, survey in enumerate(surveys)]
	update.message.reply_text('Выберите опрос\n\n{}'.format(context.chat_data['surveys_out']))
	update.message.reply_text('Для выбора напишите номер нужного опроса', reply = kb.MAIN_MENU_KB)
	return cc.PICK_SURVEY_STATE

def pick_part(update: Update, context: CallbackContext) -> int:
	try:
		context.chat_data['idx'] = int(update.message.text)
		try:
			context.chat_data['current_survey'] = context.bot_data[SURVEYS_KEY][context.chat_data['idx']-1]
			update.message.reply_text('Что вы хотите отредактировать?', reply = kb.PICK_PART_KB)
	return cc.PICK_PART_STATE