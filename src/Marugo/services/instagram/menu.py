from __future__ import annotations

import time

from RPA.Browser.Selenium import By
from RPA.Browser.Selenium import Selenium

from src.Marugo.dto.menu import MenuOptionsXpaths
from src.Marugo.services.instagram import(
    MENU_OPTIONS,
    MENU_OPTIONS_CHOICES,
)

class Menu:
    """
        This class implement functionality to interact with the menu of instagram
        It's necessary to refresh the state of the menu every time the user change the page.
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
            menu_options[menu[index]] = f"//span[@aria-describedby='{aria_describedby}']"
        return menu_options

    def get_xpaths(self, robot : Selenium) -> MenuOptionsXpaths :
        time.sleep(3)
        menu_option_status = robot.get_element_status(MENU_OPTIONS)

        if menu_option_status.get("visible") == False:
            time.sleep(4)
            
        element = robot.get_webelement(menu_options)
        elements = element.find_elements(By.XPATH, MENU_OPTIONS_CHOICES)

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
