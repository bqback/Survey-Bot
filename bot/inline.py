from uuid import uuid4

from telegram import Update, InlineQueryResultArticle
from telegram.ext import CallbackContext

from bot.constants import (SURVEYS_KEY, SURVEY_TITLE_KEY, SURVEY_DESCRIPTION_KEY, SURVEYS_NONE,
                           SURVEYS_MANAGE_BUTTON, SURVEYS_MANAGE)

def surveys(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    if not context.bot_data[SURVEYS_KEY].items():
        results = [InlineQueryResultArticle(id = uuid4(), 
                                            title = survey[SURVEY_TITLE_KEY],
                                            input_message_content = InputTextMessageContent(survey[SURVEY_DESCRIPTION_KEY]))
                   for survey in context.bot_data[SURVEYS_KEY].items()]
    else:
        results = InlineQueryResultArticle(id = uuid4(), 
                                           title = SURVEYS_NONE,
                                           input_message_content = InputTextMessageContent(''))
    update.inline_query.answer(results, switch_pm_text = SURVEYS_MANAGE_BUTTON, switch_pm_parameter = SURVEYS_MANAGE)