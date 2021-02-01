from typing import Dict, List, Tuple, Union
from functools import partial
import re

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ConversationHandler, CallbackQueryHandler

from bot.manage import manage
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

def _prepare_keyboards(surveys: Dict, titles: List[List[str]], callbacks: List[str]) -> List[InlineKeyboardMarkup]:
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
		keyboards.append(InlineKeyboardMarkup(page))
		page = []
	return keyboards

def _prepare_conversation(titles, keyboards, callbacks):
	pages = range(7, 7+len(titles)-1)
	states = {}
	for i, page in enumerate(pages):
		handlers = []
		for key in sum(keyboards[i]):
			if not re.match('^(PAGE\d*|{})$'.format(cc.RETURN_CB), key.callback_data):
				handlers.append(CallbackQueryHandler(partial(manage.load_survey, title = key.callback_data)))
	conversation = ConversationHandler(
		entry_points = [CallbackQueryHandler(manage.choose_survey, pattern='^{}$'.format(cc.EDIT_SURVEY_CB))],

	)
	return conversation

class SurveyList():
	def __init__(surveys: Dict):
		self.titles, self.callbacks = _prepare_titles(surveys)
		self.keyboards = _prepare_keyboards(surveys, self.titles, self.callbacks)
		self.conversation = _prepare_conversation(self.titles, self.keyboards, self.callbacks)

	
