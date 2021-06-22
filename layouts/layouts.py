from helpers import wrap_tags
from languages import LANGS
from layouts.layoutdicts import *


def get_invalid_fullname_text(lang):
    if lang == LANGS[0]:
        text = "Ism va Familya xato formatda yuborildi !\n" \
               "Qaytadan quyidagi formatda yuboring"
        example = "Misol: Sherzodbek Esanov yoki Sherzodbek"
    else:
        text = 'Полное имя отправлено в неправильном формате !\n\n' \
               'Пожалуйста, пришлите мне свое полное имя в формате ниже'
        example = "Пример: Иван Иванов или Иван"
    return f'❗ {text}:\n\n{wrap_tags(example)}'


def get_phone_number_error_text(lang):
    if lang == LANGS[0]:
        text = "Telefon raqami xato formatda yuborildi"

    # if lang == LANGS[1]:
    #     text = "Номер телефона введен в неправильном формате"
    #
    # if lang == LANGS[2]:
    #     text = "Телефон рақами хато форматда юборилди"

    return text


def get_phone_number_layout(lang):
    """ Layout view
        Telefon raqamini quyidagi formatda yuboring

        Misol: +998 XX xxx xx xx yoki XX xxx xx xx
    """
    return f"{PHONE_NUMBER_LAYOUT_DICT[lang][1]}:\n\n" \
           f"{PHONE_NUMBER_LAYOUT_DICT[lang][2]}: " \
           f"{wrap_tags('+998 XX xxx xx xx')} {PHONE_NUMBER_LAYOUT_DICT[lang][3]} {wrap_tags('XX xxx xx xx')}"
