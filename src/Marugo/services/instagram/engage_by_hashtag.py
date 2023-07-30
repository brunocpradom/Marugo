from __future__ import annotations

import time

from src.Marugo.services.instagram import (
    SEARCH_RESULTS,
    SEARCH_RESULTS_HASHTAG_FOLLOW,
    SEARCH_RESULTS_POSTS,
    SEARCH_RESULTS_POSTS_COMMENTS,
    SEARCH_RESULTS_POSTS_FOLLOW,
    SEARCH_RESULTS_POSTS_LIKE,
    SEARCH_RESULTS_PUBLISH_COMMENT,
)
from src.Marugo.services.instagram.menu import Menu


class EngageByHashtag:

    def __init__(self, robot,logger):
        self.posts_links : list = list()
        self.menu : Menu = Menu()
        self.robot = robot
        self.logger = logger
        xpath : str = None

    def refresh_menu_xpaths(self):
        menu_xpaths = self.menu.get_xpaths(self.robot)
        self.xpath = menu_xpaths.search

    def click_search_button(self):
        time.sleep(1)
        self.logger.info("Clicking on search button")

        self.refresh_menu_xpaths()
        self.robot.click_element(self.xpath)
        time.sleep(2)

        self.logger.info("Search button clicked")

    def search(self, search_term):
        self.logger.info(f"Searching for : {search_term}")

        search_input_xpath = "//input[@placeholder='Pesquisar']"
        search_input_status = self.robot.get_element_status(search_input_xpath)

        if search_input_status.get("visible") == False:
            self.click_search_button()

        self.robot.input_text(search_input_xpath, search_term)
        time.sleep(3) #Wait for the search results

        self.logger.info(f"Search for : {search_term} done")

    def click_first_result(self):
        self.logger.info("Clicking on first result")

        search_elements = self.robot.get_webelements(SEARCH_RESULTS)
        first_result = search_elements[0]
        self.robot.click_element_when_clickable(first_result)
        time.sleep(7)

        self.logger.info("First result clicked")

    def get_posts_links(self):
        self.logger.info("Getting posts links")
        time.sleep(2)
        posts_elements_status = self.robot.get_element_status(SEARCH_RESULTS_POSTS)
        if posts_elements_status.get("visible") == False:
            time.sleep(3)
        posts = self.robot.get_webelements(SEARCH_RESULTS_POSTS)
        for post in posts:
            post_link = post.get_attribute("href")
            self.posts_links.append(post_link)

        self.logger.info("Posts links gotten")

    def check_if_posts_already_liked(self) -> bool:
        "const divElement = document.querySelector('div.x6s0dn4 x78zum5 xdt5ytf xl56j7k'); "
        javascript_code = """
            const svgElement = document.querySelector('.xp7jhwk svg');
            const titleElement = svgElement.querySelector('title');
            const titleValue = titleElement.textContent;
            return titleValue;
        """
        title_value = self.robot.driver.execute_script(javascript_code)
        if title_value.lower() == "curtir":
            return False
        else:
            return True

    def like_posts(self):
        self.logger.info("Liking post")

        time.sleep(3)
        like_element_status = self.robot.get_element_status(SEARCH_RESULTS_POSTS_LIKE)
        if self.check_if_posts_already_liked() == False:
            self.robot.click_element_when_clickable(SEARCH_RESULTS_POSTS_LIKE)
            self.logger.info("Post liked")
        else:
            self.logger.warning("Post already liked")


    def follow_hashtag(self):
        follow_element_status = self.robot.get_element_status(SEARCH_RESULTS_HASHTAG_FOLLOW)
        if follow_element_status.get("visible") == True:
            self.robot.click_element_when_clickable(SEARCH_RESULTS_HASHTAG_FOLLOW)
            self.logger.info("Hash tag followed")
        else:
            self.logger.warning("Hash tag already followed")

    def follow_profile(self):
        self.logger.info("Following post")

        time.sleep(3)
        follow_element_status = self.robot.get_element_status(SEARCH_RESULTS_POSTS_FOLLOW)
        if follow_element_status.get("visible") == True:
            self.robot.click_element_when_clickable(SEARCH_RESULTS_POSTS_FOLLOW)
            self.logger.info("Posts followed")
        else:
            self.logger.warning("Post already followed")


    def leave_comment(self):
        #todo - create a list of comments - choose randomly
        self.logger.info("Leaving comment")

        time.sleep(3)
        self.robot.input_text(SEARCH_RESULTS_POSTS_COMMENTS, "❤️")
        self.robot.click_element_when_clickable(SEARCH_RESULTS_PUBLISH_COMMENT)

        self.logger.info("Comment left")

    def start(self, hashtag):
        self.logger.info(f"Engaging by hashtag : {hashtag}")

        self.click_search_button()
        self.search(hashtag)
        self.click_first_result()
        self.get_posts_links()
        self.follow_hashtag()

        for link in self.posts_links:
            self.robot.go_to(link)
            self.follow_profile()
            self.like_posts()
            #self.leave_comment()

        self.logger.info(f"Engaging by hashtag : {hashtag} done")
