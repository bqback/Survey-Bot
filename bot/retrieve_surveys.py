from typing import Dict, List

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

class SurveyList():
	def __init__(surveys: Dict):
		titles = _prepare_titles(surveys)

	def _prepare_keyboards(surveys: Dict, titles: Dict):
	keyboard = []
	row = []
	for page in titles:
		for i in range(len(page)):
			row.append(
					InlineKeyboardButton(str(i), callback_data = surveys[i]['title'])
			)
			if len(row) == 5:
				keyboard.append(row)
				row = []
		else:
			if i < 10:
				keyboard

	def _prepare_titles(surveys: Dict):
	titles = []
	page = []
	for i in range(len(surveys)):
		page.append('{}. '.format(i+1) + surveys[i]['title'])
		if len(page) == 10:
			titles.append(page)
			page = []
