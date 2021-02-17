import gettext
import logging

from typing import Dict, List, Union

_ = gettext.gettext

logger = logging.getLogger(__name__)

def surv_diff(surv_old: Dict, surv_new: Dict, lang: str) -> str:
    global _
    locale = gettext.translation('utils', localedir = 'locales', languages = [context.user_data['lang']])
    locale.install()
    _ = locale.gettext
    if type(surv_old) is dict and type(surv_new) is dict:
        diff_list = ""
        if 'title' in surv_old and 'title' in surv_new:
            if surv_old['title'] != surv_new['title']:
                diff_list.append(_("Название\n"
                                    "{old} -> {new}\n\n"
                                ).format(old = surv_old['title'], new = surv_new['title'])
                    )
        else:
            if 'title' not in surv_old:
                raise KeyError(_("В старом опросе пропало название!"))
            if 'title' not in surv_new:
                raise KeyError(_("В новом опросе пропало название!"))
        if 'desc' in surv_old and 'desc' in surv_new:
            if surv_old['desc'] != surv_new['desc']:
                diff_list.append(_("Описание\n"
                                    "{old} -> {new}\n\n"
                                ).format(old = surv_old['desc'], new = surv_new['desc'])
                    )
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
                            diff_list.append(_("Вопрос №{num}\n"
                                                "{old} -> {new}\n\n"
                                            ).format(num = q_idx+1, old = old_question['question'], new = new_question['question'])
                                )
                    if 'multi' in old_question and 'multi' in new_question:
                        if old_question['multi'] != new_question['multi']:
                            old_multi = _("несколько вариантов") if old_question['multi'] else _("один вариант")
                            new_multi = _("несколько вариантов") if new_question['multi'] else _("один вариант")
                            diff_list.append(_("Число возможных вариантов ответа в вопросе №{num}\n"
                                                "{old} -> {new}\n\n"
                                            ).format(num = q_idx+1, old = old_multi, new = new_multi)
                                )
                    if 'answers' in old_question and 'answers' in new_question:
                        for a_idx, old_answer in enumerate(old_question['answers']):
                            try:
                                new_answer = new_question['answers'][a_idx]
                                if old_answer != new_answer:
                                    diff_list.append(_("Ответ №{a_num} в вопросе №{q_num}\n"
                                                        "{old} -> {new}\n\n"
                                                    ).format(a_num = a_idx+1, q_num = q_idx+1, old = old_answer, new = new_answer)
                                        )
                            except IndexError:
                                diff_list.append(_("Удалён или перемещён ответ №{a_num} в вопросе №{q_num}\n"
                                                    "{old} ->\n\n"
                                                ).format(a_num = a_idx+1, q_num = q_idx+1, old = old_answer)
                                    )
                        if len(old_question['answers']) < len(new_question['answers']):
                            old_len = len(old_question['answers'])
                            new_len = len(new_question['answers'])
                            for a_idx in range(old_len, new_len):
                                new_answer = new_question['answers'][a_idx]
                                diff_list.append(_("К вопросу №{q_num} добавлен ответ №{a_num}\n"
                                                    " -> {new}\n\n"
                                                ).format(q_num = q_idx+1, a_num = old_len+a_idx+1, new = new_answer)
                                    )
                except IndexError:
                    diff_list.append(_("Удалён или перемещён вопрос №{num}"
                                                    "{old} ->\n\n"
                                    ).format(q_num = q_idx+1, old = old_question['question'])
                        )
            if len(surv_old['questions']) < len(surv_new['questions']):
                old_len = len(surv_old['questions'])
                new_len = len(surv_new['questions'])
                for q_idx in range(old_len, new_len):
                    new_question = surv_new['questions'][a_idx]
                    diff_list.append(_("Добавлен вопрос №{num}\n"
                                        " -> {new}\n\n"
                                    ).format(num = q_idx+1, new = new_question['question'])
                        )
                    new_multi = _("несколько вариантов") if new_question['multi'] else _("один вариант")
                    diff_list.append(_("Число возможных вариантов ответа в вопросе №{num}\n"
                                        " -> {new}\n\n"
                                    ).format(num = q_idx+1, new = new_multi)
                        )
                    for a_idx, new_answer in enumerate(new_question['answers']):
                        diff_list.append(_("К вопросу №{q_num} добавлен ответ №{a_num}\n"
                                            " -> {new}\n\n"
                                        ).format(q_num = q_idx+1, a_num = a_idx+1, new = new_answer)
                            )
        else:
            if 'questions' not in surv_old:
                raise KeyError(_("В старом опросе пропали вопросы!"))
            if 'questions' not in surv_new:
                raise KeyError(_("В новом опросе пропали вопросы!"))
        if not diff_list:
            diff_list = _("Список изменений:\n\n") + diff_list
        return diff_list
    else:
        if type(surv_old) is not dict:
            raise TypeError(_("Старый опрос передан в неправильном формате!"))
        if type(surv_new) is not dict:
            raise TypeError(_("Новый опрос передан в неправильном формате!"))

def num_list(stuff: List) -> str:
    out = ""
    for idx, item in enumerate(stuff):
        out.append(f'{idx+1}. {item}\n')
    return out

def validate_index(index: str, stuff: Union[List, Dict]) -> int:
    idx = int(index - 1)
    if idx not in range(len(stuff)):
        raise IndexError()
    else:
        return idx
