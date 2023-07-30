from __future__ import annotations

import time

from loguru import logger
from RPA.Browser.Selenium import By
from RPA.Browser.Selenium import Selenium

from src.Marugo.config import Config
from src.Marugo.services.instagram.menu import Menu

class Instagram:
    """
        This class implement functinality to interact with instagram webpage

        Considerations:
            - When the user make the first action, like follow someone, instagram will
        ask if you want to activate notifications. Its is necessary to click the "dont
        activate" button. This button is not always available. So, I need to verify if
        the button is available before click it.
    """
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
        self.robot.input_text_when_element_is_visible("name:username", self.config.username)
        self.robot.input_text_when_element_is_visible("name:password", self.config.password)
        self.robot.press_keys("name:password", "ENTER")

        self.logger.info("Login done")

    def logout(self):
        self.logger.info(f"Logout for user : {self.config.username}")

        self.refresh_menu_xpaths()
        self.robot.click_element(self.menu_xpaths.settings)
        time.sleep(2)
        logout_xpath = "//span[text()='Sair']"
        self.robot.click_element(logout_xpath)

        self.logger.info("Logout done")

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

    def follow_who_follow_me(self):
        #? I could verify if the element is available too. Is better than use try/except
        self.logger.info("Try to Follow who follow me")
        self.click_notification()
        time.sleep(2)
        try:
            new_followers_xpath = "//div[@class='x6s0dn4 x1q4h3jn x78zum5 x1y1aw1k xxbr6pl xwib8y2 xbbxn1n x87ps6o x1wq6e7o x1di1pr7 x1h4gsww xux34ky x1ypdohk x1l895ks']"
            new_followers = self.robot.get_webelements(new_followers_xpath)
            for follower in new_followers:
                follow_button ="//button[@class='_acan _acap _acas _aj1-']"
                follow_button_status = follower.get_element_status(follow_button)
                if follow_button_status.get("visible") == True:
                    follow_button_element = follower.find_element(By.XPATH, follow_button)
                    self.robot.click_element_if_visible(follow_button_element)
                else:
                    self.logger.info("Follow button not available")

        except Exception as error:
            self.logger.info(error)

    def click_dont_activate_notifications(self):
        dont_activate_notifications_button = "xpath://button[@class='_a9-- _a9_1']"
        self.robot.click_element_if_visible(dont_activate_notifications_button)

    


    def discovering(self):
        initial_page_xpath="//span[@aria-describedby=':r2:']"
        messages = "//span[@aria-describedby=':rd:']"
        notifications = "//span[@aria-describedby=':rb:']"
        notifications = "//span[@aria-describedby=':r12:']"
        create = "//span[@aria-describedby=':r8:']"
        #@ //div[@class='xx4vt8u xurb0ha x1sxyh0']   # This is the parent div from the left profile sugestions
        #All the profiles that are suggested to follow have this class
        #@  //section[@class='_aalv _akmq']    # This is the section that contains the profiles in the right side
        profile_suggested_to_follow = "//div[@class='x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3']"
        #I think all the follow button from the sugestion page are the same
        follow_button="//button[@class='_acan _acap _acas _aj1-']"

        dont_activate_notifications_button = "xpath://button[@class='_a9-- _a9_1']"

        notificatoes = "//div[.//span[@aria-label='notificacoes']]"

    def look_the_profile_suggestion(self):
        left_profile_sugestion_xpath ="//div[@class='xx4vt8u xurb0ha x1sxyh0']//div[@class='x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3']"
        elements = self.robot.get_webelements(left_profile_sugestion_xpath)
        follow_button=".//button[@class='_acan _acap _acas _aj1-']"
        follow_button_parent =".//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1pi30zi x1swvt13 xwib8y2 x1y1aw1k x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1']"

        for element in elements:
            try:
                el = element.find_element(By.XPATH, follow_button)
                time.sleep(2)
                self.robot.click_element_when_clickable(follow_button)

            except Exception as error:
                self.logger.info(error)
                parent_el = element.find_element(By.XPATH, follow_button_parent)
                self.robot.click_element(parent_el)
                el = element.find_element(By.XPATH, follow_button)
                time.sleep(2)
                self.robot.click_element_when_clickable(follow_button)

    def follow_sugested_profiles(self):
        # This is not appearing anymore
        # It was available only in the first login
        self.click_notification()
        left_profile_sugestions = "//div[@class='xx4vt8u xurb0ha x1sxyh0']//div[@class='x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3']"
        elements = self.robot.find_element(By.XPATH, left_profile_sugestions)
        for element in elements:
            #todo - Here I need to create a random logic that click on the follow button of some profiles, but not from all
            self.robot.click_element("xpath:.//button[@class='_acan _acap _acas _aj1-']")


#def make_search(self, search_term):
    #     self.click_search_button()
    #     search_input_xpath = "//input[@placeholder='Pesquisar']"
    #     self.robot.input_text(search_input_xpath, search_term)
    #     time.sleep(1) #Wait for the search results
    #     #Click the first one
    #     search_elements = self.robot.get_webelements(SEARCH_RESULTS)
    #     first_result = search_elements[0]
    #     self.robot.click_element(first_result)
    #     time.sleep(2)
    #     #navigate throught the posts with this hashtag
    #     posts_links = list()
    #     posts = self.robot.get_webelements(SEARCH_RESULTS_POSTS)
    #     for post in posts:
    #         post_link = post.get_attribute("href")
    #         posts_links.append(post_link)

    #     for link in posts_links:
    #         self.robot.go_to(link)
    #         time.sleep(2)
    #         self.robot.click_element_when_clickable(SEARCH_RESULTS_POSTS_FOLLOW)
    #         time.sleep(1)
    #         self.robot.click_element_when_clickable(SEARCH_RESULTS_POSTS_LIKE)
    #         time.sleep(2)
    #         SEARCH_RESULTS_POSTS_COMMENTS
    #         self.robot.input_text(SEARCH_RESULTS_POSTS_COMMENTS, "❤️")
    #         self.robot.click_element_when_clickable(SEARCH_RESULTS_PUBLISH_COMMENT)

