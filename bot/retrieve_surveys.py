from typing import Dict, List, Tuple, Union

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

import bot.conv_constants as cc

def _prepare_titles(surveys: Dict) -> Tuple[List[List[str]], List[str]]:
	titles = []
	page = []
	callbacks = []
	for i in range(len(surveys)):
		page.append('{}. '.format(i+1) + surveys[i]['title'])
		if len(page) == 10:
			titles.append(page)
			callbacks.append('PAGE{}'.format(i+1))
			page = []
	return (titles, callbacks)

def _prepare_keyboards(surveys: Dict, titles: List[List[str]], callbacks: List[str]) -> List[List[Union[InlineKeyboardButton, List[InlineKeyboardButton]]]]:
	keyboards = []
	kb_page = []
	row = []
	for pagenum, page in enumerate(titles):
		for i in range(len(page)):
			row.append(
					InlineKeyboardButton(str(i), callback_data = surveys[i]['title'])
			)
			if len(row) == 5:
				kb_page.append(row)
				row = []		
				if i % 10 == 0 && len(titles) > 1:
					if pagenum == 0:
						kb_page.append(
							InlineKeyboardButton('Следующие 10', callback_data = callbacks[pagenum+1])
						)
					elif pagenum == len(titles) - 1:
						kb_page.append(
							InlineKeyboardButton('Предыдущие 10', callback_data = callbacks[pagenum-1])
						)
					else:
						kb_page.append(
							[
								InlineKeyboardButton('Следующие 10', callback_data = callbacks[pagenum+1]),
								InlineKeyboardButton('Предыдущие 10', callback_data = callbacks[pagenum-1])
							]	
						)
		page.append(InlineKeyboardButton(cc.RETURN, callback_data = cc.RETURN_CB))	
		keyboards.append(page)
		page = []
	return keyboards

class SurveyList():
	def __init__(surveys: Dict):
		self.titles, self.callbacks = _prepare_titles(surveys)
		self.keyboards = _prepare_keyboards(surveys, self.titles, self.callbacks)

	
