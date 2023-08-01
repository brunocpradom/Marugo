from __future__ import annotations

import time

from RPA.Browser.Selenium import Selenium

from src.Marugo.config import Config
from src.Marugo.services.instagram.menu import Menu
from src.Marugo.services.instagram import(
    USERNAME,
    PASSWORD,
    DONT_ACTIVATE_NOTIFICATIONS,
)

class Instagram:

    url = "https://www.instagram.com/"

    def __init__(self, config : Config, robot : Selenium , logger):
        self.robot = robot
        self.menu = Menu()
        self.logger = logger
        self.config = config
        self.menu_xpaths = None
        self.logger = logger

    def login(self):
        self.logger.info(f"Login for user : {self.config.username}")
        time.sleep(1)
        self.robot.input_text_when_element_is_visible(USERNAME, self.config.username)
        self.robot.input_text_when_element_is_visible(PASSWORD, self.config.password)
        self.robot.press_keys(PASSWORD, "ENTER")

        self.logger.info("Login done")

    def refresh_menu_xpaths(self):
        self.menu_xpaths = self.menu.get_xpaths(self.robot)

    def open_browser(self, headless : bool = False):
        self.logger.info("Open browser for user")
        self.robot.open_available_browser(self.url, headless=headless)
        self.logger.info("Browser opened")

    def close_browser(self):
        self.logger.info("Close browser")
        self.robot.close_all_browsers()
        self.logger.info("Browser closed")

    def click_notification(self):
        self.logger.info("Click notification button")

        self.refresh_menu_xpaths()
        notification_xpath= self.menu_xpaths.notifications
        self.robot.click_element(notification_xpath)

        self.logger.info("Notification button clicked")

    def click_home(self):
        self.logger.info("Click home button")

        self.refresh_menu_xpaths()
        home_xpath=self.menu_xpaths.home
        self.robot.click_element(home_xpath)

        self.logger.info("Home button clicked")

    def click_search_button(self):
        self.logger.info("Click search button")

        self.refresh_menu_xpaths()
        search_xpath=self.menu_xpaths.search
        self.robot.click_element(search_xpath)

        self.logger.info("Search button clicked")

    def click_dont_activate_notifications(self):
        self.robot.click_element_if_visible(DONT_ACTIVATE_NOTIFICATIONS)
