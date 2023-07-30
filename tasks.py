#from robocorp.tasks import task
from __future__ import annotations

from loguru import logger as loguru_logger
from RPA.Browser.Selenium import Selenium

from src.Marugo.config import get_credentials
from src.Marugo.services.instagram.engage_by_hashtag import EngageByHashtag
from src.Marugo.services.instagram.instagram import Instagram

# @task
# def minimal_task():
#     message = "Hello"
#     message = message + " World!"


def main():
    robot = Selenium()
    config = get_credentials()
    logger = loguru_logger
    insta = Instagram(config, robot, logger)
    insta.open_browser()
    insta.login()

    for hashtag in config.hashtags:
        engage = EngageByHashtag(robot, logger)
        engage.start(hashtag)

    insta.logout()
    insta.close_browser()

if __name__ == "__main__":
    main()
