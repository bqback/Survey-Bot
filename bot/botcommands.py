import gettext
from bot.longbotcommand import LongBotCommand


_ = gettext.gettext


class BotCommands:
    def __init__(self, lang: str):

        global _

        locale = gettext.translation(
            "botcommands", localedir="locales", languages=[lang]
        )
        locale.install()
        _ = locale.gettext

        self.bot_commands = [
            LongBotCommand(
                "add_admin",
                _(
                    "[Адм.] Добавляет нового администратора/администраторов с указанными ID"
                ),
                _(
                    "[Адм.] Добавляет нового администратора или администраторов с указанными ID в INI-файл\n"
                    "Большая часть команд (в т. ч. запуск и управление опросами) доступна только администраторам\n"
                    "После использования команды используйте команду /update_admins для обновления активного списка\n"
                    "ID должны быть разделены пробелами, кавычками или точками с запятыми\n"
                    "Пример: /add_admin 11111111 22222222"
                ),
            ),
            LongBotCommand(
                "add_chat",
                _("[Адм.] Добавляет новый чат/чаты с указанными ID"),
                _(
                    "[Адм.] Добавляет новый чат или чаты с указанными ID в INI-файл\n"
                    "Чтобы запустить опрос в чате, его предварительно нужно добавить, используя эту команду\n"
                    "Добавить можно только те чаты, где состоит этот бот\n"
                    "Для получения ID чата используйте команду /show_chat_id\n"
                    "После использования команды используйте команду /update_chats для обновления активного списка\n"
                    "ID должны быть разделены пробелами, кавычками или точками с запятыми\n\n"
                    "Пример: /add_chat -11111111 -22222222"
                ),
            ),
            LongBotCommand(
                "help",
                _("/help command: Выводит подробную справку по команде"),
                _("Выводит подробную справку по команде\n\n" "Пример: /help help"),
            ),
            LongBotCommand(
                "restart",
                _("[Адм.] Перезапускает бота"),
                _(
                    "[Адм.] Перезапускает бота\n"
                    "Происходит перезагрузка бота (аналогично простому запуску)\n"
                    "Позволяет применять внесённые в файлы бота изменения с помощью самого же бота\n\n"
                    "Пример: /restart"
                ),
            ),
            LongBotCommand(
                "remove_admin",
                _("[Адм.] Удаляет администратора/администраторов с указанными ID"),
                _(
                    "[Адм.] Удаляет администратора или администраторов с указанными ID из INI-файла\n"
                    "Большая часть команд (в т. ч. запуск и управление опросами) доступна только администраторам\n"
                    "После использования команды используйте команду /update_admins для обновления активного списка\n"
                    "ID должны быть разделены пробелами, кавычками или точками с запятыми\n\n"
                    "Пример: /add_admin 11111111 22222222"
                ),
            ),
            LongBotCommand(
                "remove_chat",
                _("[Адм.] Удаляет чат/чаты с указанными ID"),
                _(
                    "[Адм.] Удаляет чат или чаты с указанными ID из INI-файла\n"
                    "Для получения ID чата используйте команду /show_chat_id\n"
                    "После использования команды используйте команду /update_chats для обновления активного списка\n"
                    "ID должны быть разделены пробелами, кавычками или точками с запятыми\n\n"
                    "Пример: /add_chat -11111111 -22222222"
                ),
            ),
            LongBotCommand(
                "reset_ongoing",
                _("[Адм.] Сбрасывает флаг 'сейчас идёт опрос'"),
                _(
                    "[Адм.] Сбрасывает флаг 'сейчас идёт опрос'\n"
                    "Флаг устанавливается ботом при запуске и окончании опроса\n"
                    "При перезапуске бота во время опроса флаг остаётся в неправильном положении, "
                    "что препятствует запуску нового опроса\n\n"
                    "Пример: /reset_ongoing"
                ),
            ),
            LongBotCommand(
                "rotate_log",
                _("[Адм.] Сохраняет текущий лог и запускает новый"),
                _(
                    "[Адм.] Сохраняет текущий лог и запускает новый\n"
                    "Файл автоматически заменяется по достижению указанного в INI-файле размера и при перезапуске бота,"
                    "однако можно это сделать по желанию с помощью этой команды\n\n"
                    "Пример: /rotate_log"
                ),
            ),
            LongBotCommand(
                "show_chat_id",
                _("Показывает ID текущего чата"),
                _(
                    "Показывает ID чата, в котором использована команда\n"
                    "ID чата нужен для команд /add_chat и /remove_chat\n"
                    "В личных сообщениях ID чата совпадает с ID пользователя\n\n"
                    "Пример: /show_chat_id"
                ),
            ),
            LongBotCommand(
                "show_current_survey",
                _("[Адм.] Выводит все данные обрабатываемого в данный момент опроса"),
                _(
                    "[Адм.] Выводит все данные обрабатываемого в данный момент опроса\n"
                    "Позволяет проверить, правильно ли сохраняются вводимые данные\n\n"
                    "Пример: /show_current_survey"
                ),
            ),
            LongBotCommand(
                "show_id",
                _("Показывает ID пользователя, использовавшего команду"),
                _(
                    "Показывает ID пользователя, использовавшего команду\n"
                    "ID чата нужен для команд /add_admin и /remove_admin\n\n"
                    "Пример: /show_id"
                ),
            ),
        ]
