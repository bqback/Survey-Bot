import gettext

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import bot.conv_constants as cc

_ = gettext.gettext

LANG_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('🇷🇺', callback_data = cc.RU_CB),
                    InlineKeyboardButton('🇺🇸', callback_data = cc.EN_CB)
                ]
            ]
        )

class Keyboards():
    def __init__(self, lang: str):

        global _

        locale = gettext.translation('keyboards', localedir = 'locales', languages = [lang])
        locale.install()
        _ = locale.gettext

        self.INITIAL_STATE_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Начать опрос"), callback_data = cc.START_SURVEY_CB),
                    InlineKeyboardButton(_("Управлениe опросами"), callback_data = cc.MANAGE_SURVEYS_CB)
                ],
                [
                    InlineKeyboardButton(_("Настройки"), callback_data = cc.SETTINGS_CB)
                ]
            ]
        )
        
        self.MAIN_MENU_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Вернуться в главное меню"), callback_data = cc.RETURN_TO_MAIN_CB)
                ]
            ]
        )
        
        self.START_SURVEY_NONE_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Создать опрос"), callback_data = cc.CREATE_SURVEY_CB),
                    InlineKeyboardButton(_("Вернуться назад"), callback_data = cc.RETURN_CB)
                ]
            ]
        )
        
        self.SAVE_TITLE_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Сохранить название"), callback_data = cc.SAVE_TITLE_CB),
                    InlineKeyboardButton(_("Ввести название заново"), callback_data = cc.ENTER_AGAIN_CB)
                ]
            ]
        )
        
        self.SAVE_DESC_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Сохранить описание"), callback_data = cc.SAVE_DESC_CB),
                    InlineKeyboardButton(_("Ввести описание заново"), callback_data = cc.ENTER_AGAIN_CB)
                ]
            ]
        )
        
        self.SAVE_QUESTION_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Сохранить вопрос"), callback_data = cc.SAVE_QUESTION_CB),
                    InlineKeyboardButton(_("Ввести вопрос заново"), callback_data = cc.ENTER_AGAIN_CB)
                ]
            ]
        )
        
        self.SAVE_MULTI_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Да"), callback_data = cc.YES_CB),
                    InlineKeyboardButton(_("Выбрать заново"), callback_data = cc.ENTER_AGAIN_CB)
                ]
            ]
        )
        
        self.SAVE_ANSWER_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Сохранить ответ"), callback_data = cc.SAVE_ANSWER_CB),
                    InlineKeyboardButton(_("Ввести ответ заново"), callback_data = cc.ENTER_AGAIN_CB)
                ]
            ]
        )
        
        self.NEXT_ANSWER_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Добавить ещё один ответ"), callback_data = cc.NEXT_ANSWER_CB),
                    InlineKeyboardButton(_("Перейти к следующему вопросу"), callback_data = cc.NEXT_QUESTION_CB)
                ],
                [
                    InlineKeyboardButton(_("Закончить и перейти к проверке опроса"), callback_data = cc.FINISH_CREATING_CB),
                ]
            ]
        )
        
        self.REVIEW_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Закончить создание и сохранить опрос"), callback_data = cc.CREATION_COMPLETE_CB)
                ],
                [
                    InlineKeyboardButton(_("Отредактировать опрос"), callback_data = cc.EDIT_SURVEY_COMPOSE_CB)
                ],
                [
                    InlineKeyboardButton(_("Начать заново"), callback_data = cc.START_OVER_SURVEY_CB)
                ]
            ]
        )
        
        self.PICK_PART_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Редактировать название"), callback_data = cc.EDIT_TITLE_CB),
                    InlineKeyboardButton(_("Редактировать описание"), callback_data = cc.EDIT_DESC_CB),
                    InlineKeyboardButton(_("Редактировать вопросы"), callback_data = cc.EDIT_QUESTIONS_CB)
                ],
                [
                    InlineKeyboardButton(_("Сохранить изменения и выйти"), callback_data = cc.SAVE_AND_EXIT_CB)
                ],
                [
                    InlineKeyboardButton(_("Выйти в главное меню"), callback_data = cc.RETURN_TO_MAIN_CB)
                ]
            ]
        )
        
        self.EDIT_TITLE_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Ввести новое название"), callback_data = cc.NEW_TITLE_CB)
                ],
                [
                    InlineKeyboardButton(_("Сохранить текущее название"), callback_data = cc.KEEP_CURRENT_TITLE_CB)
                ]
            ]
        )
        
        self.EDIT_TITLE_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Ввести новое описание"), callback_data = cc.NEW_DESC_CB)
                ],
                [
                    InlineKeyboardButton(_("Сохранить текущее описание"), callback_data = cc.KEEP_CURRENT_DESC_CB)
                ]
            ]
        )
        
        self.RETURN_FROM_FIRST_STEP_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Вернуться назад"), callback_data = cc.RETURN_CB)
                ]
            ]
        )
        
        self.RETURN_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Вернуться на предыдущий шаг"), callback_data = cc.RETURN_CB),
                    InlineKeyboardButton(_("Начать заново"), callback_data = cc.RETURN_START_OVER_CB),
                    InlineKeyboardButton(_("Выйти в главное меню"), callback_data = cc.RETURN_TO_MAIN_CB)
                ]
            ]
        )
        
        self.MANAGE_SURVEYS_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Создать новый опрос"), callback_data = cc.CREATE_SURVEY_CB),
                    InlineKeyboardButton(_("Выбрать из существующих"), callback_data = cc.CHOOSE_SURVEY_CB),
                ]
            ]
        )
        
        self.YES_NO_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Да"), callback_data = cc.YES_CB),
                    InlineKeyboardButton(_("Нет"), callback_data = cc.NO_CB)
                ]
            ]
        )

        self.SETTINGS_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Язык"), callback_data = cc.SETTINGS_LANG_CB)
                ]
            ]
        )