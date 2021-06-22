from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackContext,
    Filters
)

from DB import *
from config import ACTIVE_ADMINS
from globalvariables import *
from helpers import wrap_tags
from validations import *
from layouts import *
from languages import LANGS
from replykeyboards import ReplyKeyboard
from replykeyboards.replykeyboardvariables import *


def do_command(update: Update, context: CallbackContext):
    # with open('update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    user = get_user(update.effective_user.id)
    user_data = context.user_data
    command = update.message.text

    if command == '/start':
        if user:
            text = f'🏠 Asosiy menyu'
            keyboard = client_menu_keyboard
            keyboard = ReplyKeyboard(keyboard, user[LANG]).get_markup()
            update.message.reply_text(text, reply_markup=keyboard)
            return ConversationHandler.END

        else:
            edited_msg_text = 'Iltimos, Ism va Familyangizni kiriting'
            example = 'Misol: Sherzodbek Esanov yoki Sherzodbek'
            edited_msg_text += f'\n\n ℹ {wrap_tags(example)}'
            update.message.reply_text(edited_msg_text)

            user_data[TG_ID] = update.effective_user.id
            user_data[USERNAME] = update.effective_user.username
            user_data[IS_ADMIN] = True if update.effective_user.id in ACTIVE_ADMINS else False
            user_data[STATE] = FULLNAME
            user_data[LANG] = LANGS[0]
            return FULLNAME


def fullname_callback(update: Update, context: CallbackContext):
    user_data = context.user_data
    fullname = validate_fullname(update.message.text)

    if fullname:
        user_data[FULLNAME] = fullname
        text = "«📱 Telefon raqamini yuborish» tugmasini bosing\nyoki\n"
        layout = get_phone_number_layout(user_data[LANG])
        text += layout
        reply_keyboard = ReplyKeyboard(phone_number_keyboard, user_data[LANG]).get_markup()
        update.message.reply_text(text, reply_markup=reply_keyboard)

        user_data[STATE] = PHONE_NUMBER
        return PHONE_NUMBER

    else:
        fullname_error_text = get_invalid_fullname_text(user_data[LANG])
        update.message.reply_text(fullname_error_text, quote=True)

        return


def phone_number_callback(update: Update, context: CallbackContext):
    user_data = context.user_data
    phone_number = update.message.contact.phone_number if update.message.contact else update.message.text
    phone_number = validate_phone_number(phone_number)

    if not phone_number:
        error_text = get_phone_number_error_text(user_data[LANG])
        layout = get_phone_number_layout(user_data[LANG])
        error_text = f'❌ {error_text} !\n' + layout
        update.message.reply_text(error_text, quote=True)

        return

    else:
        user_data[PHONE_NUMBER] = phone_number
        if STATE in user_data:
            user_data.pop(STATE)
        insert_data(user_data, 'users')

        text = f"{user_data[FULLNAME]} !\n" \
               "😀 Registratsiya muvafaqqiyatli yakunlandi 🎉🎉🎉"
        reply_keyboard = ReplyKeyboard(client_menu_keyboard, user_data[LANG]).get_markup()
        update.message.reply_text(text, reply_markup=reply_keyboard)

        user_data.clear()
        return ConversationHandler.END


def general_callback(update: Update, context: CallbackContext):
    pass


registration_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler(['start'], do_command, filters=~Filters.update.edited_message)],

    states={

        FULLNAME: [
            MessageHandler(Filters.text & (~Filters.command) & (~Filters.update.edited_message), fullname_callback)
        ],

        PHONE_NUMBER: [MessageHandler(Filters.contact | Filters.text & (~Filters.command)
                                      & (~Filters.update.edited_message) & (~Filters.reply), phone_number_callback)],

    },
    fallbacks=[MessageHandler(Filters.text & (~Filters.update.edited_message), general_callback)],

    persistent=True,

    name='registration_conversation'
)
