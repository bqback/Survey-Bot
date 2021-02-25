import gettext
import logging
import configparser
import re

import bot.autofit as autofit

from typing import Dict, List, Union, Tuple

_ = gettext.gettext

logger = logging.getLogger(__name__)

def surv_diff(surv_old: Dict, surv_new: Dict, lang: str) -> str:
    global _
    locale = gettext.translation('utils', localedir = 'locales', languages = [lang])
    locale.install()
    _ = locale.gettext
    if type(surv_old) is dict and type(surv_new) is dict:
        diff_list = ""
        if 'title' in surv_old and 'title' in surv_new:
            if surv_old['title'] != surv_new['title']:
                diff_list += _("Название\n"
                                    "{old} -> {new}\n\n"
                                ).format(old = surv_old['title'], new = surv_new['title'])
        else:
            if 'title' not in surv_old:
                raise KeyError(_("В старом опросе пропало название!"))
            if 'title' not in surv_new:
                raise KeyError(_("В новом опросе пропало название!"))
        if 'desc' in surv_old and 'desc' in surv_new:
            if surv_old['desc'] != surv_new['desc']:
                diff_list += _("Описание\n"
                                    "{old} -> {new}\n\n"
                                ).format(old = surv_old['desc'], new = surv_new['desc'])
        else:
            if 'desc' not in surv_old:
                raise KeyError(_("В старом опросе пропало описание!"))
            if 'desc' not in surv_new:
                raise KeyError(_("В новом опросе пропало описание!"))       
        if 'questions' in surv_old and 'questions' in surv_new:
            for q_idx, old_question in enumerate(surv_old['questions']):
                try:
                    new_question = surv_new['questions'][q_idx]
                    if 'question' in old_question and 'question' in new_question:
                        if old_question['question'] != new_question['question']:
                            diff_list += _("Вопрос №{num}\n"
                                                "{old} -> {new}\n\n"
                                            ).format(num = q_idx+1, old = old_question['question'], new = new_question['question'])
                    if 'multi' in old_question and 'multi' in new_question:
                        if old_question['multi'] != new_question['multi']:
                            old_multi = _("несколько вариантов") if old_question['multi'] else _("один вариант")
                            new_multi = _("несколько вариантов") if new_question['multi'] else _("один вариант")
                            diff_list += _("Число возможных вариантов ответа в вопросе №{num}\n"
                                                "{old} -> {new}\n\n"
                                            ).format(num = q_idx+1, old = old_multi, new = new_multi)
                    if 'answers' in old_question and 'answers' in new_question:
                        for a_idx, old_answer in enumerate(old_question['answers']):
                            try:
                                new_answer = new_question['answers'][a_idx]
                                if old_answer != new_answer:
                                    diff_list += _("Ответ №{a_num} в вопросе №{q_num}\n"
                                                        "{old} -> {new}\n\n"
                                                    ).format(a_num = a_idx+1, q_num = q_idx+1, old = old_answer, new = new_answer)
                            except IndexError:
                                diff_list += _("Удалён или перемещён ответ №{a_num} в вопросе №{q_num}\n"
                                                    "{old} ->\n\n"
                                                ).format(a_num = a_idx+1, q_num = q_idx+1, old = old_answer)
                        if len(old_question['answers']) < len(new_question['answers']):
                            old_len = len(old_question['answers'])
                            new_len = len(new_question['answers'])
                            for a_idx in range(old_len, new_len):
                                new_answer = new_question['answers'][a_idx]
                                diff_list += _("К вопросу №{q_num} добавлен ответ №{a_num}\n"
                                                    " -> {new}\n\n"
                                                ).format(q_num = q_idx+1, a_num = old_len+a_idx+1, new = new_answer)
                except IndexError:
                    diff_list += _("Удалён или перемещён вопрос №{num}"
                                                    "{old} ->\n\n"
                                    ).format(q_num = q_idx+1, old = old_question['question'])
            if len(surv_old['questions']) < len(surv_new['questions']):
                old_len = len(surv_old['questions'])
                new_len = len(surv_new['questions'])
                for q_idx in range(old_len, new_len):
                    new_question = surv_new['questions'][a_idx]
                    diff_list += _("Добавлен вопрос №{num}\n"
                                        " -> {new}\n\n"
                                    ).format(num = q_idx+1, new = new_question['question'])
                    new_multi = _("несколько вариантов") if new_question['multi'] else _("один вариант")
                    diff_list += _("Число возможных вариантов ответа в вопросе №{num}\n"
                                        " -> {new}\n\n"
                                    ).format(num = q_idx+1, new = new_multi)
                    for a_idx, new_answer in enumerate(new_question['answers']):
                        diff_list += _("К вопросу №{q_num} добавлен ответ №{a_num}\n"
                                            " -> {new}\n\n"
                                        ).format(q_num = q_idx+1, a_num = a_idx+1, new = new_answer)
        else:
            if 'questions' not in surv_old:
                raise KeyError(_("В старом опросе пропали вопросы!"))
            if 'questions' not in surv_new:
                raise KeyError(_("В новом опросе пропали вопросы!"))
        if diff_list:
            diff_list = _("Список изменений:\n\n") + diff_list
        return diff_list
    else:
        if type(surv_old) is not dict:
            raise TypeError(_("Старый опрос передан в неправильном формате!"))
        if type(surv_new) is not dict:
            raise TypeError(_("Новый опрос передан в неправильном формате!"))

def num_list(stuff: List, key = None) -> str:
    out = ""
    if key is None:
        for idx, item in enumerate(stuff):
            out += f'{idx+1}. {item}\n'
    else:
        for idx, item in enumerate(stuff):
            out += f'{idx+1}. {item[key]}\n'
    return out

def validate_index(index: str, stuff: Union[List, Dict]) -> int:
    idx = int(index) - 1
    if idx not in range(len(stuff)):
        raise IndexError()
    else:
        return idx

def print_survey(survey: Dict) -> str:
    out = f"{survey['title']}\n\n{survey['desc']}"
    for question in survey['questions']:
        out += f"\n\n{question['question']}"
        if question['multi']:
            out += _(" (можно выбрать несколько вариантов)")
        else:
            out += _(" (можно выбрать только один вариант)")
        for idx, answer in enumerate(question['answers']):
            out += f"\n\t{idx+1}. {answer}"
    return out

def parse_cfg(filename: str) -> Tuple[str]:
    config = configparser.ConfigParser(comment_prefixes = '/', allow_no_value = True)
    config.read_file(open(filename))

    token = config['bot']['token']
    pickle = config['bot']['pickle']
    chat_list = config['bot']['chats']
    if re.match(' ', chat_list):
        chat_list.replace(' ', '')
        config['bot']['chats'] = chat_list
        config.write(open('bot.ini', 'w'))
    try:
        chats = [int(chat_id) for chat_id in config['bot']['chats'].split(',')]
    except ValueError:
        raise ValueError("Chat list contains invalid data! Make sure it's either an int or a list of ints")
    admin_list = config['bot']['admins']
    if re.match(' ', admin_list):
        admin_list.replace(' ', '')
        config['bot']['admins'] = admin_list
        config.write(open('bot.ini', 'w'))
    try:
        admins = [int(admin_id) for admin_id in config['bot']['admins'].split(',')]
    except ValueError:
        raise ValueError("Admin list contains invalid data! Make sure it's either an int or a list of ints")
    
    defaults = dict(filter(lambda entry: not re.match('^#.+$', entry[0]), config.items('defaults')))

    for key, value in defaults.items():
        if key == 'timeout':
            defaults[key] = float(defaults[key])

    log_file = config['log']['filename']
    log_size = int(config['log']['log_size']) * 1024
    log_backups = int(config['log']['log_backups'])

    sheets_file = config['sheets']['file']

    return (token, pickle, chats, admins,
            defaults, log_file, log_size, log_backups,
            sheets_file)

def submit_data(answers, questions, flag, file):
    logger.info(_("Отправляю данные"))
    client = service_account(filename = file)
    logger.info(_("Установлено соединение с Google Sheets"))
    spreadsheet = client.open('Опросы ГКБ в Телеграме')
    logger.info(_("Открыта книга"))
    time = datetime.now().strftime('%Y/%m/%d %H.%M.%S')
    spreadsheet.add_worksheet(time, 1, len(questions) + 1, index = 0)
    logger.info(_("Создана таблица"))
    sh = spreadsheet.get_worksheet(0)
    logger.info(_("Выбрана таблица"))
    sh.update([['Имя'] + questions])
    logger.info(_("Расставлены названия для столбцов"))
    for uid, values in answers.items():
        logger.info(_("Записываются данные для пользователя {} ({})").format(uid, values['name']))
        sh.append_row([values.get(key) for key in values.keys()])
        logger.info(_("Данные записаны"))
    autofit.columns(spreadsheet)
    logger.info(_("Столбцы отрегулированы"))
    flag = False