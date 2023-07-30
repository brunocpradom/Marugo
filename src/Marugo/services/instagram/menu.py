from __future__ import annotations

import time

from RPA.Browser.Selenium import By
from RPA.Browser.Selenium import Selenium

from src.Marugo.dto.menu import MenuOptionsXpaths

class Menu:
    """
        This class implement functionality to interact with the menu of instagram
        It's necessary to refresh the state of the menu every time the user change the page.
        But I'm still find the possibles ways to do it. The first approach is to get all
        the aria-describedby of the menu options. The aria-describedby is a unique id for
        looking for the element. But I found a situation where, after refreshing the page,
        They put less spans tags in the dom. The first time I look for it, the notification
        option has two span tags.
    """
    _menu_options_1 = {
            0 : "instagram",
            1 : "home",
            2 : "search",
            3 : "explore",
            4 : "reels",
            5 : "messages",
            6 : "notifications",
            7 : "notifications",
            8 : "create",
            9 : "profile",
            10 : "settings",
        }
    _menu_options_2 = {
            0 : "instagram",
            1 : "home",
            2 : "search",
            3 : "explore",
            4 : "reels",
            5 : "messages",
            6 : "notifications",
            7 : "create",
            8 : "profile",
            9 : "settings",
        }

    def _get_menu_options(self, elements):
        menu_options = {}
        if len(elements) == 10:
            menu = self._menu_options_2
        elif len(elements) == 11:
            menu = self._menu_options_1

        for index, el in enumerate(elements):
            aria_describedby = el.get_attribute("aria-describedby")
            complete_xpath = f"//span[@aria-describedby='{aria_describedby}']"
            menu_options[menu[index]] = f"//span[@aria-describedby='{aria_describedby}']"
        return menu_options

    def get_xpaths(self, robot : Selenium) -> MenuOptionsXpaths :
        time.sleep(3)
        menu_options = "//div[@class='x1iyjqo2 xh8yej3']"
        menu_option_status = robot.get_element_status(menu_options)

        while menu_option_status.get("visible") == False:
            #todo - implement a timeout-maybe a function that deal with it
            time.sleep(1)
            menu_option_status = robot.get_element_status(menu_options)

        element = robot.get_webelement(menu_options)
        menu_options_xpath = "//span[@class='x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j']"
        elements = element.find_elements(By.XPATH, menu_options_xpath)

        menu_options = self._get_menu_options(elements)

        return MenuOptionsXpaths(
            instagram=menu_options["instagram"],
            home=menu_options["home"],
            search=menu_options["search"],
            explore=menu_options["explore"],
            reels=menu_options["reels"],
            messages=menu_options["messages"],
            notifications=menu_options["notifications"],
            create=menu_options["create"],
            profile=menu_options["profile"],
            settings=menu_options["settings"],
        )


# def get_menu_options(self):
#         """
#             This method will return a dictionary with the menu options and the xpath
#             of each option. The idea is to run this method everytime the user change
#             the page. Instagram change the xpath of the menu options everytime the user
#             change the page. So, this method will get the xpath of the menu options
#         """
#         _menu_options = {
#             0 : "instagram",
#             1 : "home",
#             2 : "search",
#             3 : "explore",
#             4 : "reels",
#             5 : "messages",
#             6 : "notifications",
#             7 : "notifications",
#             8 : "create",
#             9 : "profile",
#             10 : "settings",
#         }
#         menu_options = {}
#         element = self.robot.get_webelement("//div[@class='x1iyjqo2 xh8yej3']")
#         menu_options_xpath = "//span[@class='x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j']"
#         elements = element.find_elements(By.XPATH, menu_options_xpath)

#         for index, el in enumerate(elements):
#             aria_describedby = el.get_attribute("aria-describedby")
#             complete_xpath = f"//span[@aria-describedby='{aria_describedby}']"
#             menu_options[_menu_options[index]] = f"//span[@aria-describedby='{aria_describedby}']"

#         return MenuOptionsXpaths(
#             home=menu_options["home"],
#             search=menu_options["search"],
#             explore=menu_options["explore"],
#             reels=menu_options["reels"],
#             messages=menu_options["messages"],
#             notifications=menu_options["notifications"],
#             create=menu_options["create"],
#             profile=menu_options["profile"],
#             settings=menu_options["settings"],
#         )
