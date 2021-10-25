from discord.errors import Forbidden

import time
import schedule
import logging
import logging.handlers
import email_bot
from dataholder import DataHolder
import discord_bot
import crawler
import threading
import asyncio

logging.basicConfig(handlers=[logging.FileHandler(filename="main.log", 
                                                 encoding='utf-8', mode='a+')],
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger('main-service-handler')


if __name__ == "__main__": 
    logger.info("starting service")
    dataHolder = DataHolder()

    crawler_thread = threading.Thread(target=crawler.run, args=(dataHolder,))
    crawler_thread.start()
    logger.info("crawler started")

    loop = asyncio.get_event_loop()
    loop.create_task(discord_bot.run(dataHolder))
    discord_bot_thread = threading.Thread(target=loop.run_forever)
    discord_bot_thread.start()    
    logger.info("discord_bot started")
    