from __future__ import annotations

import time

from src.Marugo.services.instagram.menu import Menu


class Follow:
    def __init__(self, robot, logger):
        self.robot = robot
        self.logger = logger
        self.menu = Menu()
        self.new_followers = None

    def refresh_menu_xpaths(self):
        self.menu_xpaths = self.menu.get_xpaths(self.robot)

    def click_notification(self):
        self.logger.info("Click notification button")

        self.refresh_menu_xpaths()
        notification_xpath= self.menu_xpaths.notifications
        self.robot.click_element(notification_xpath)

        self.logger.info("Notification button clicked")

    def check_for_new_followers(self):
        new_followers_xpath = "//div[@class='x6s0dn4 x1q4h3jn x78zum5 x1y1aw1k xxbr6pl xwib8y2 xbbxn1n x87ps6o x1wq6e7o x1di1pr7 x1h4gsww xux34ky x1ypdohk x1l895ks']"
        self.new_followers = self.robot.get_webelements(new_followers_xpath)


    def follow_who_follow_me(self):

        for follower in self.new_followers:
            follow_button ="//button[@class='_acan _acap _acas _aj1-']"
            follow_button_status = follower.get_element_status(follow_button)
            if follow_button_status.get("visible") == True:
                follow_button_element = follower.find_element(By.XPATH, follow_button)
                self.robot.click_element_if_visible(follow_button_element)
            else:
                self.logger.info("Follow button not available")

    def start(self):
        self.logger.info("Try to Follow who follow me")
        self.click_notification()
        time.sleep(2)
        self.check_for_new_followers()
        self.follow_who_follow_me()
        self.logger.info("Follow who follow me done")
