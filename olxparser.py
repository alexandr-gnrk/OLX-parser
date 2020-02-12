import json

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from advertisement import Advertisement


class OLXParser():
    """
    The OLXParser object contains contains information
    that using to parse passed URL.
    """

    def __init__(self, search_url):
        self.search_url = search_url
        self.driver = self.init_driver()
        self.ads = list()

    def init_driver(self):
        """ Create and set up driver """
        user_agent = (
            'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
        )
        profile = webdriver.FirefoxProfile()
        # disable images to increase speed
        profile.set_preference('permissions.default.image', 2)
        profile.set_preference('general.useragent.override', user_agent)
        return webdriver.Firefox(
            firefox_profile=profile, 
            executable_path='./geckodriver'
        )

    def parse(self):
        """ Go through the pages. """
        self.driver.get(self.search_url)
        print(f'Start parsing {self.search_url}')
        page = 1
        while True:
            print((f'[ Page {page} ]').center(80, '#'))
            self.parse_search_page()
            # try to find button that leads to next page
            try:
                next_page_elem = self.get_next_page_elem()
            except NoSuchElementException:
                break
            else:
                self.click_link(next_page_elem)
                page += 1

    def parse_search_page(self):
        """ Parse certain search page. """
        ads_on_page = len(self.get_ads_from_page())
        for i in range(ads_on_page):
            ads_num = len(self.ads) + 1
            print(f' Ad #{ads_num} '.center(80, '-'))

            # get the element with link on ad page
            ad_elem = self.get_ads_from_page()[i]
            # delete cookies to make parser undectable
            self.driver.delete_all_cookies()
            self.click_link(ad_elem)
            self.parse_ad_page()
            # back to the main search page
            self.driver.back()

    def parse_ad_page(self):
        """ Parse certain ad page """
        ad = Advertisement()
        ad.title = self.get_ad_title()
        ad.description = self.get_ad_description()
        ad.location = self.get_ad_location()
        ad.details = self.get_ad_details()
        ad.contacts = self.get_ad_contacts()
        ad.url = self.driver.current_url

        print(ad)
        self.ads.append(ad)

    def click_link(self, elem):
        """ Scroll frame to link, and click on it """
        self.scroll_to_elem(elem)
        elem.click()

    def click_btn(self, elem):
        """ Scroll frame to button, and click on it """
        self.scroll_to_elem(elem)
        self.driver.execute_script('arguments[0].click();', elem)

    def scroll_to_elem(self, elem):
        """ Scroll frame to passed element """
        self.driver.execute_script(
            "return arguments[0].scrollIntoView();",
            elem
        )

    def get_ads_from_page(self):
        """ Return all ads elements on page """
        ads_headings_elems = self.driver.find_elements_by_xpath(
            "//a[@class='marginright5 link linkWithHash detailsLink']"
        )
        return ads_headings_elems

    def get_next_page_elem(self):
        """ Extract button that leads to next search page """
        return self.driver.find_element_by_css_selector('a.pageNextPrev')

    def get_ad_title(self):
        """ Extract ad title """
        return self.driver.find_element_by_tag_name('h1').text

    def get_ad_description(self):
        """ Extract ad description """
        return self.driver.find_element_by_id('textContent').text

    def get_ad_location(self):
        """ Extract ad location """
        location = self.driver.find_element_by_css_selector(
            'a.show-map-link:nth-child(1) > strong:nth-child(1)'
        ).text
        return location

    def get_ad_details(self):
        """ Extract ad details """
        details = self.driver.find_element_by_css_selector(
            '.offer-titlebox__details > em'
        ).text
        return details

    def get_ad_contacts(self):
        """ Extract ad contacts """
        # try to find contacts button
        try:
            contact_numbers_elem = self.driver.find_element_by_css_selector(
                'div.contact-button'
            )
        except NoSuchElementException:
            return list()
        # wait while button unclickable
        try:
            WebDriverWait(self.driver, 5).until(ec.element_to_be_clickable(
                 (By.CSS_SELECTOR, 'div.contact-button')
            ))
        except NoSuchElementException:
            return list()

        self.click_btn(contact_numbers_elem)
        # wait while javasript will change information
        try:
            wait = WebDriverWait(self.driver, 30)
            wait.until(
                ec.element_located_selection_state_to_be(
                    (By.CSS_SELECTOR, 'div.contact-button.activated'),
                    False
                )
            )
        except TimeoutException:
            return list()

        contacts = contact_numbers_elem.find_element_by_tag_name(
            'strong'
        ).text.split('\n')
        return contacts

    def save_ads(self, filename='ads.json'):
        """ Save all ads in passed file """
        ads = [ad.to_dict() for ad in self.ads]
        with open(filename, 'w') as file:
            file.write(json.dumps(ads, indent=4, ensure_ascii=False))

    def __del__(self):
        self.driver.quit()
