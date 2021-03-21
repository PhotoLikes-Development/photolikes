import logging
import numpy
import PIL

from config import Config

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from common.image_processing import dataurl_from_image, preprocess_image

from model.model_loader import ModelLoader

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
model_loader = ModelLoader()


def handle(update: Update, ctx: CallbackContext) -> None:
    photos_number = len(update.message.photo)

    if not photos_number:
        update.message.reply_text('Please send image to me')
        return

    if photos_number > 1:
        update.message.reply_text('Please send only one photo per message')
        return

    photo = ctx.bot.get_file(update.message.photo[0].file_id)
    model = model_loader.get_instance()
    image_arr = preprocess_image(photo)
    estimation = model.predict(numpy.array([image_arr]))[0]
    lo, mid, hi = estimation

    update.message.reply_text(f'There is {lo * 100}% probability that photo will be low-rated, '
                              f'{mid * 100} average-rated and {hi * 100} high-rated.')


def main() -> None:
    """Start the bot."""
    updater = Updater(Config.TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.photo, handle))
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()