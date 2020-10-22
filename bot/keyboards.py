from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import bot.conv_constants as cc

INITIAL_STATE = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(cc.START_SURVEY, callback_data = cc.START_SURVEY_CB),
			InlineKeyboardButton(cc.MANAGE_SURVEYS, callback_data = cc.MANAGE_SURVEYS_CB)
		]
	]
)

START_SURVEY_NONE = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(cc.CREATE_SURVEY, callback_data = cc.CREATE_SURVEY_CB),
			InlineKeyboardButton(cc.RETURN, callback_data = cc.RETURN_CB)
		]
	]
)

RETURN_FROM_FIRST_STEP = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(cc.RETURN, callback_data = cc.RETURN_CB)
		]
	]
)

RETURN_KEYBOARD = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(cc.RETURN, callback_data = cc.RETURN_CB),
			InlineKeyboardButton(cc.RETURN_START_OVER, callback_data = cc.RETURN_START_OVER_CB),
			InlineKeyboardButton(cc.RETURN_TO_MAIN, callback_data = cc.RETURN_TO_MAIN_CB)
		]
	]
)

MULTIPLE_ANSWERS = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton('Один вариант', callback_data = 'ONE'),
			InlineKeyboardButton('Несколько', callback_data = 'MULTIPLE')
		]
	]
)

YES_NO = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(cc.YES, callback_data = cc.YES_CB),
			InlineKeyboardButton(cc.NO, callback_data = cc.NO_CB)
		]
	]
)