import re

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Filters, MessageHandler, CallbackContext

from DB import *
from globalvariables import *
from helpers import wrap_tags, delete_message_by_message_id
from replykeyboards.replykeyboardtypes import reply_keyboard_types
from replykeyboards.replykeyboardvariables import *


def message_handler_callback(update: Update, context: CallbackContext):
    # with open('jsons/update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    user = get_user(update.effective_user.id)
    user_data = context.user_data

    if user:
        get_id_btn = reply_keyboard_types[client_menu_keyboard]['get_id_btn'][f'text_{user[LANG]}']

        # Settings get_id_btn
        if re.search(f"^({get_id_btn})$", update.message.text):
            text = "ℹ Maxsus raqamni olish uchun avval kanalga a'zo bo'ling. \n\n" \
                   f"❗ Kanalga a'zo bo'lganingizda so'ng\n«✅ Raqamni olish» ni bosing.\n\n" \
                   f"🅰 AD: 🤖 TelegramBot yaratish, buyurtma qilish uchun @sobirsb ga murojaat qilishingiz mumkin !"
            inline_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Kanalga a'zo bo'lish ", 'https://t.me/Kitobchi_ali')],
                [InlineKeyboardButton("✅ Raqamni olish", callback_data='get_id')]
            ])
            delete_message_by_message_id(context, user)
            message = update.message.reply_text(wrap_tags(text), reply_markup=inline_markup)
            user_data[MESSAGE_ID] = message.message_id
            return
        return

    else:
        reply_text = "❗ Siz ro'yxatdan o'tmagansiz !\n" \
                     "Ro'yxatdan o'tish uchun /start ni bosing"
        update.message.reply_text(reply_text)
        return


message_handler = MessageHandler(Filters.text & (~ Filters.command) & (~Filters.update.edited_message)
                                 & (~Filters.update.channel_posts) & (~Filters.reply), message_handler_callback)
