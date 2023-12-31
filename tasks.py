from __future__ import annotations
import time
from datetime import datetime, timedelta

from loguru import logger as loguru_logger
from RPA.Browser.Selenium import Selenium
import schedule
from robocorp.tasks import task

from src.Marugo.config import get_credentials
from src.Marugo.services.instagram.engage_by_hashtag import EngageByHashtag
from src.Marugo.services.instagram.instagram import Instagram

def main():
    try:
        loguru_logger.info("Starting Marugo bot")
        loguru_logger.info(f"Current time : {datetime.now()}")

        robot = Selenium()
        config = get_credentials()
        logger = loguru_logger
        insta = Instagram(config, robot, logger)
        insta.open_browser()
        insta.login()
        time.sleep(2)
        insta.click_dont_activate_notifications()
        for hashtag in config.hashtags:
            time.sleep(1)
            engage = EngageByHashtag(robot, logger)
            engage.start(hashtag)

        insta.close_browser()

        logger.info(f"Next execution : {datetime.now() + timedelta(hours=10)}")
        logger.info("Marugo bot finished")


    except Exception as error:
        logger.error(f"Error on Marugo bot")
        logger.error(error)
        insta.close_browser()

@task
def minimal_task():
    main()


if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    period = int(os.getenv("PERIOD", 2))
    schedule.every(period).hours.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
