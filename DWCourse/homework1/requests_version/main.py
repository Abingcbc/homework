import requests
import random
from apscheduler.schedulers.blocking import BlockingScheduler
from crawler import crawl, run
from init import read_urls
import threading
import logging
import warnings

warnings.filterwarnings('ignore')

logging.basicConfig(
    level=logging.INFO,
    filename="amazon.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s: %(message)s",
)

read_urls()
# scheduler = BlockingScheduler()
# scheduler.add_job(crawl, 'interval', seconds=1)
# print('----- Start -----')
# scheduler.start()
crawl()