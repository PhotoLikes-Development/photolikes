import io
import logging

import numpy
from PIL import Image
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

from common.image_processing import preprocess_image
from config import Config
from model.loaders.filesystem_model_loader import FilesystemModelLoader

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
model_loader = FilesystemModelLoader()


def handle(update: Update, ctx: CallbackContext) -> None:
    photos_number = len(update.message.photo)

    if not photos_number:
        update.message.reply_text('Please send image to me')
        return

    photo_bytes = ctx.bot.get_file(update.message.photo[0].file_id).download_as_bytearray()
    photo = Image.open(io.BytesIO(photo_bytes))
    model = model_loader.get_instance()
    image_arr = preprocess_image(photo)
    estimation = model.predict(numpy.array([image_arr]))[0]
    lo, mid, hi = estimation
    score = 10 * hi + 6 * mid

    update.message.reply_text(f'Your score is *{score:.2f}* out of 10',
                              parse_mode='markdown')


def main() -> None:
    """Start the bot."""
    updater = Updater(Config.TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.all, handle))
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()