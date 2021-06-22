from telegram import ReplyKeyboardMarkup, KeyboardButton
from .replykeyboardtypes import *


class ReplyKeyboard(object):
    def __init__(self, keyb_type, lang, data=None):
        self.__type = keyb_type
        self.__lang = lang
        self.__data = data

    def __create_reply_keyboard(self):
        reply_keyboard = [
            [KeyboardButton(button[f'text_{self.__lang}'])]
            for button in reply_keyboard_types[self.__type].values()
        ]
        if self.__type == phone_number_keyboard:
            reply_keyboard[0][0].request_contact = True
        return ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    def get_markup(self) -> ReplyKeyboardMarkup:
        return self.__create_reply_keyboard()
