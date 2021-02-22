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
                    InlineKeyboardButton(_("Название"), callback_data = cc.EDIT_TITLE_CB),
                    InlineKeyboardButton(_("Описание"), callback_data = cc.EDIT_DESC_CB),
                    InlineKeyboardButton(_("Вопросы"), callback_data = cc.EDIT_QUESTIONS_CB)
                ],
                [
                    InlineKeyboardButton(_("Сохранить изменения и выйти"), callback_data = cc.SAVE_AND_EXIT_CB)
                ],
                [
                    InlineKeyboardButton(_("Выйти без сохранения"), callback_data = cc.DISCARD_AND_EXIT_CB)
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
        
        self.EDIT_DESC_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Ввести новое описание"), callback_data = cc.NEW_DESC_CB)
                ],
                [
                    InlineKeyboardButton(_("Сохранить текущее описание"), callback_data = cc.KEEP_CURRENT_DESC_CB)
                ]
            ]
        )

        self.EDIT_QUESTION_PART_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Текст вопроса"), callback_data = cc.EDIT_QUESTION_TEXT_CB)
                ],
                [
                    InlineKeyboardButton(_("Число вариантов ответа"), callback_data = cc.EDIT_MULTI_CB)
                ],
                [
                    InlineKeyboardButton(_("Ответы"), callback_data = cc.EDIT_ANSWERS_CB)
                ],
                [
                    InlineKeyboardButton(_("Удалить вопрос"), callback_data = cc.REMOVE_QUESTION_CB)
                ],
                [
                    InlineKeyboardButton(_("Вернуться назад"), callback_data = cc.RETURN_CB)
                ]
            ]
        )

        self.EDIT_QUESTION_TEXT_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Ввести новый текст вопроса"), callback_data = cc.NEW_QUESTION_TEXT_CB)
                ],
                [
                    InlineKeyboardButton(_("Сохранить текущий текст вопроса"), callback_data = cc.KEEP_CURRENT_QUESTION_TEXT_CB)
                ]
            ]
        )

        self.EDIT_MULTI_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Изменить"), callback_data = cc.NEW_MULTI_CB)
                ],
                [
                    InlineKeyboardButton(_("Оставить как есть"), callback_data = cc.KEEP_CURRENT_MULTI_CB)
                ]
            ]
        )

        self.EDIT_ANSWER_OPTIONS_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Редактировать один из ответов"), callback_data = cc.EDIT_EXISTING_ANSWER_CB)
                ],
                [
                    InlineKeyboardButton(_("Добавить ещё один ответ"), callback_data = cc.ADD_NEW_ANSWER_CB)
                ],
                [
                    InlineKeyboardButton(_("Вернуться назад"), callback_data = cc.RETURN_CB)
                ]
            ]
        )

        self.EDIT_ANSWER_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Редактировать"), callback_data = cc.EDIT_ANSWER_CB),
                    InlineKeyboardButton(_("Удалить"), callback_data = cc.REMOVE_ANSWER_CB)
                ]
            ]
        )

        self.EDIT_AFTER_SAVE_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("К выбору части опроса"), callback_data = cc.TO_PARTS_CB)
                ],
                [
                    InlineKeyboardButton(_("К выбору вопроса"), callback_data = cc.TO_QUESTIONS_CB)
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
                ],
                [
                    InlineKeyboardButton(_("Вернуться в главное меню"), callback_data = cc.RETURN_TO_MAIN_CB)
                ]
            ]
        )

        self.MANAGE_SURVEY_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Редактировать опрос"), callback_data = cc.EDIT_SURVEY_MANAGE_CB),
                    InlineKeyboardButton(_("Удалить опрос"), callback_data = cc.MANAGE_DELETE_SURVEY_CB),
                ],
                [
                    InlineKeyboardButton(_("Показать опрос"), callback_data = cc.PRINT_SURVEY_CB)
                ],
                [
                    InlineKeyboardButton(_("Вернуться в главное меню"), callback_data = cc.RETURN_TO_MAIN_CB)
                ]
            ]
        )

        self.MANAGE_AFTER_DELETE_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Вернуться к выбору опроса"), callback_data = cc.CHOOSE_SURVEY_CB),
                    InlineKeyboardButton(_("Вернуться в главное меню"), callback_data = cc.RETURN_TO_MAIN_CB),
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

        self.POLL_PREVIEW_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Выбрать чат для проведения опроса"), callback_data = cc.PICK_CHAT_CB),
                    InlineKeyboardButton(_("Выбрать другой опрос"), callback_data = cc.CHOOSE_SURVEY_CB)
                ],
                [
                    InlineKeyboardButton(_("Вернуться в главное меню"), callback_data = cc.RETURN_TO_MAIN_CB)
                ]
            ]
        )

        self.SET_CAP_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Использовать рекомендованное"), callback_data = cc.USE_RECOMMENDED_CB),
                    InlineKeyboardButton(_("Установить своё"), callback_data = cc.SET_OWN_CAP_CB)
                ],
                [
                    InlineKeyboardButton(_("Вернуться в главное меню"), callback_data = cc.RETURN_TO_MAIN_CB)
                ]
            ]
        )

        self.CUSTOM_CAP_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Использовать"), callback_data = cc.USE_CUSTOM_CB),
                    InlineKeyboardButton(_("Ввести заново"), callback_data = cc.ENTER_AGAIN_CB)
                ],
                [
                    InlineKeyboardButton(_("Использовать рекомендованное"), callback_data = cc.USE_RECOMMENDED_CB)
                ],
                [
                    InlineKeyboardButton(_("Вернуться в главное меню"), callback_data = cc.RETURN_TO_MAIN_CB)
                ]
            ]
        )

        self.POLL_CONFIRM_KB = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_("Начать опрос"), callback_data = cc.START_SURVEY_CB)
                ],
                [
                    InlineKeyboardButton(_("Выбрать другой опрос"), callback_data = cc.CHANGE_SURVEY_CB),
                    InlineKeyboardButton(_("Выбрать другой чат"), callback_data = cc.CHANGE_CHAT_CB),
                    InlineKeyboardButton(_("Изменить значение"), callback_data = cc.CHANGE_CAP_CB),
                ],
                [
                    InlineKeyboardButton(_("Вернуться в главное меню"), callback_data = cc.RETURN_TO_MAIN_CB)
                ]
            ]
        )