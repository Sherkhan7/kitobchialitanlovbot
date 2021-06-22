from telegram import TelegramError
from globalvariables import *


def delete_items_in_user_data(data, *args):
    for key in args:
        if key in data:
            del data[key]


def wrap_tags(*args):
    listed_args = list(args)
    symbol = ' ' if len(args) > 1 else ''

    for index, value in enumerate(listed_args):
        listed_args[index] = str(listed_args[index])
    return f'<b>{symbol.join(listed_args)}</b>'


def delete_message_by_message_id(context, user):
    user_data = context.user_data
    if MESSAGE_ID in user_data:
        try:
            context.bot.delete_message(user[TG_ID], user_data[MESSAGE_ID])
        except TelegramError:
            try:
                context.bot.edit_message_reply_markup(user[TG_ID], user_data[MESSAGE_ID])
            except TelegramError:
                pass
        finally:
            del user_data[MESSAGE_ID]
