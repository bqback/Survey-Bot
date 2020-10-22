from uuid import uuid4

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CallbackContext

from bot.constants import (SURVEYS_KEY, SURVEY_TITLE_KEY, SURVEY_DESCRIPTION_KEY, SURVEYS_MANAGE_BUTTON,
                           SURVEYS_MANAGE_ARG)

def surveys(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    if len(context.bot_data[SURVEYS_KEY].items()) > 0:
        results = [InlineQueryResultArticle(id = uuid4(), 
                                            title = survey[SURVEY_TITLE_KEY],
                                            input_message_content = InputTextMessageContent(survey[SURVEY_DESCRIPTION_KEY]))
                   for survey in context.bot_data[SURVEYS_KEY].items()]
    else:
        results = []
    update.inline_query.answer(results, switch_pm_text = SURVEYS_MANAGE_BUTTON, switch_pm_parameter = SURVEYS_MANAGE_ARG)