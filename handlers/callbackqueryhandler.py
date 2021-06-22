from telegram import Update, TelegramError
from telegram.ext import CallbackQueryHandler, CallbackContext

from DB import *
from globalvariables import *
from config import *


def inline_keyboards_handler_callback(update: Update, context: CallbackContext):
    # with open('jsons/callback_query.json', 'w') as callback_query_file:
    #     callback_query_file.write(callback_query.to_json())
    user = get_user(update.effective_user.id)
    callback_query = update.callback_query

    if callback_query.data == 'get_id':
        chat_member = context.bot.get_chat_member(CHANNEL_ID, user[TG_ID])
        not_member_alert_text = "Avval kanalga a'zo bo'ling ❗"
        id_text = f"🆔 Maxsus raqam: {user[ID]}"
        alert_text = not_member_alert_text if chat_member.status != 'member' else id_text
        try:
            callback_query.answer(alert_text, show_alert=True)
        except TelegramError:
            pass
        return


callback_query_handler = CallbackQueryHandler(inline_keyboards_handler_callback)
