from telegram import ParseMode
from telegram.ext import Updater, PicklePersistence, Defaults

from config import *
from handlers import *
from errorhandler import error_handler


def main():
    my_persistence = PicklePersistence(PICKLE_FILE_NAME, single_file=False, store_chat_data=False)
    defaults = Defaults(parse_mode=ParseMode.HTML, disable_web_page_preview=True)

    updater = Updater(TOKEN, persistence=my_persistence, defaults=defaults)

    updater.dispatcher.add_handler(registration_conversation_handler)

    updater.dispatcher.add_handler(message_handler)

    updater.dispatcher.add_handler(callback_query_handler)

    # adding error handler
    updater.dispatcher.add_error_handler(error_handler)

    # updater.start_polling()
    updater.start_webhook(port=PORT, url_path=TOKEN, webhook_url=BASE_URL + TOKEN)

    updater.idle()


if __name__ == '__main__':
    main()
