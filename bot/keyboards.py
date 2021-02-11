from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import bot.conv_constants as cc

INITIAL_STATE_KB = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(cc.START_SURVEY, callback_data = cc.START_SURVEY_CB),
			InlineKeyboardButton(cc.MANAGE_SURVEYS, callback_data = cc.MANAGE_SURVEYS_CB)
		]
	]
)

MAIN_MENU_KB = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(cc.RETURN_TO_MAIN, callback_data = cc.RETURN_TO_MAIN_CB)
		]
	]
)

START_SURVEY_NONE_KB = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(cc.CREATE_SURVEY, callback_data = cc.CREATE_SURVEY_CB),
			InlineKeyboardButton(cc.RETURN, callback_data = cc.RETURN_CB)
		]
	]
)

SAVE_TITLE_KB = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(cc.SAVE_TITLE, callback_data = cc.SAVE_TITLE_CB),
			InlineKeyboardButton(cc.ENTER_AGAIN, callback_data = cc.ENTER_AGAIN_CB)
		]
	]
)

SAVE_DESC_KB = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(cc.SAVE_DESC, callback_data = cc.SAVE_DESC_CB),
			InlineKeyboardButton(cc.ENTER_AGAIN, callback_data = cc.ENTER_AGAIN_CB)
		]
	]
)

SAVE_QUESTION_KB = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(cc.SAVE_QUESTION, callback_data = cc.SAVE_QUESTION_CB),
			InlineKeyboardButton(cc.ENTER_AGAIN, callback_data = cc.ENTER_AGAIN_CB)
		]
	]
)

SAVE_MULTI_KB = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(cc.SAVE_MULTI, callback_data = cc.SAVE_MULTI_CB),
			InlineKeyboardButton(cc.ENTER_AGAIN, callback_data = cc.ENTER_AGAIN_CB)
		]
	]
)

SAVE_ANSWER_KB = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(cc.SAVE_ANSWER, callback_data = cc.SAVE_ANSWER_CB),
			InlineKeyboardButton(cc.ENTER_AGAIN, callback_data = cc.ENTER_AGAIN_CB)
		]
	]
)

NEXT_ANSWER_KB = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(cc.NEXT_ANSWER, callback_data = cc.NEXT_ANSWER_CB),
			InlineKeyboardButton(cc.NEXT_QUESTION, callback_data = cc.NEXT_QUESTION_CB)
		],
		[
			InlineKeyboardButton(cc.FINISH_CREATING, callback_data = cc.FINISH_CREATING_CB),
		]
	]
)

REVIEW_KB = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(cc.CREATION_COMPLETE, callback_data = cc.CREATION_COMPLETE_CB)
		],
		[
			InlineKeyboardButton(cc.EDIT_SURVEY, callback_data = cc.EDIT_SURVEY_CB),
			InlineKeyboardButton(cc.START_OVER_SURVEY, callback_data = cc.START_OVER_SURVEY_CB)
		]
	]
)

PICK_PART_KB = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(cc.EDIT_TITLE, callback_data = cc.EDIT_TITLE_CB),
			InlineKeyboardButton(cc.EDIT_DESC, callback_data = cc.EDIT_DESC_CB),
			InlineKeyboardButton(cc.EDIT_QUESTIONS, callback_data = cc.EDIT_QUESTIONS_CB)
		],
		[
			InlineKeyboardButton(cc.CHOOSE_ANOTHER, callback_data = cc.CHOOSE_ANOTHER_CB)
		],
		[
			InlineKeyboardButton(cc.RETURN_TO_MAIN, callback_data = cc.RETURN_TO_MAIN_CB)
		]
	]
)

EDIT_TITLE_KB = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(cc.NEW_TITLE, callback_data = cc.NEW_TITLE_CB)
		],
		[
			InlineKeyboardButton(cc.KEEP_CURRENT_TITLE, callback_data = cc.KEEP_CURRENT_TITLE_CB)
		]
	]
)

EDIT_TITLE_KB = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(cc.NEW_DESC, callback_data = cc.NEW_DESC_CB)
		],
		[
			InlineKeyboardButton(cc.KEEP_CURRENT_DESC, callback_data = cc.KEEP_CURRENT_DESC_CB)
		]
	]
)

RETURN_FROM_FIRST_STEP_KB = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(cc.RETURN, callback_data = cc.RETURN_CB)
		]
	]
)

RETURN_KB = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(cc.RETURN, callback_data = cc.RETURN_CB),
			InlineKeyboardButton(cc.RETURN_START_OVER, callback_data = cc.RETURN_START_OVER_CB),
			InlineKeyboardButton(cc.RETURN_TO_MAIN, callback_data = cc.RETURN_TO_MAIN_CB)
		]
	]
)

MANAGE_SURVEYS_KB = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(cc.CREATE_SURVEY, callback_data = cc.CREATE_SURVEY_CB),
			InlineKeyboardButton(cc.CHOOSE_SURVEY, callback_data = cc.CHOOSE_SURVEY_CB),
		]
	]
)

YES_NO_KB = InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton(cc.YES, callback_data = cc.YES_CB),
			InlineKeyboardButton(cc.NO, callback_data = cc.NO_CB)
		]
	]
)