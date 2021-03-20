import os
import time

import mongoengine
import schedule

from config import Config

mongoengine.connect(Config.MONGO_DATABASE, host=Config.MONGO_URI)


def job():
    print("Starting crawling...")
    os.system("scrapy crawl vk_dating_photos")
    print("Finished crawling.")

    print("Starting training...")
    # TODO: train and update model
    print("Finished training.")


schedule.every(6).hours.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
