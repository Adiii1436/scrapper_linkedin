from csv import DictReader
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import re

class LinkedInScraper:
    def __init__(self, cookies_file='cookies.csv', output_file='search_results.json'):
        self.cookies_file = cookies_file
        self.output_file = output_file
        self.result_data = {}
        self.driver = None

    def initialize_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.set_window_size(1600, 1024)

    def get_cookies(self):
        with open(self.cookies_file, encoding='utf-8-sig') as file:
            dict_reader = DictReader(file)
            return list(dict_reader)

    def remove_hashtags(self, text):
        text = text.replace("#", "")
        text = text.replace("hashtag", "")
        return text.strip()

    def login_with_cookies(self):
        self.driver.get("https://www.linkedin.com/")
        cookies = self.get_cookies()

        for cookie in cookies:
            self.driver.add_cookie(cookie)

        self.driver.refresh()

    def search_posts(self, search_term):
        time.sleep(6)
        search_post = self.driver.find_element(By.XPATH, '//*[@id="global-nav-typeahead"]/input')
        search_post.send_keys(search_term)
        search_post.send_keys(Keys.ENTER)

    def click_posts_filter(self):
        time.sleep(6)
        idx = [1,4]
        for i in idx:
            path = f'//*[@id="search-reusables__filters-bar"]/ul/li[{i}]/button'
            ele = self.driver.find_element(By.XPATH, path)
            if ele.text=="Posts":
                ele.click()
                break

    def scroll_to_load_posts(self, num_scrolls=5):
        for _ in range(num_scrolls):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)

    def extract_data_from_posts(self, search_term):
        try:
            scrollable_div = self.driver.find_element(By.CSS_SELECTOR, 'div.search-results-container')
            options = scrollable_div.find_elements(By.CSS_SELECTOR, 'ul li')
            for i in options:
                try:
                    name = i.find_element(By.CSS_SELECTOR,
                                          'span.update-components-actor__name.hoverable-link-text.t-14.t-bold.t-black > span:nth-child(1) > span')
                    description = i.find_element(By.CSS_SELECTOR,
                                                 'div.feed-shared-update-v2__description-wrapper.mr2 > div > div > span > span > span')
                    element = i.find_element(By.CSS_SELECTOR,
                                            'div.update-components-actor.display-flex.update-components-actor--with-control-menu > div > div > a.app-aware-link.update-components-actor__meta-link')
                    link = element.get_attribute('href')

                    post_data = {
                        "name": name.text,
                        "description": str(self.remove_hashtags(description.text)),
                        "profile_link": link
                    }

                    if search_term not in self.result_data:
                        self.result_data[search_term] = []

                    self.result_data[search_term].append(post_data)

                except NoSuchElementException:
                    pass
        except NoSuchElementException as e:
            print("No posts found.")

    def save_data_to_file(self,search_term):
        existing_data = {}

        try:
            with open(self.output_file, 'r', encoding='utf-8') as json_file:
                existing_data = json.load(json_file)
        except FileNotFoundError:
            pass

        if search_term in existing_data:
            existing_data[search_term].extend(self.result_data[search_term])
        else:
            existing_data.update(self.result_data)

        with open(self.output_file, 'w', encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, ensure_ascii=False, indent=2)

        print(f"Data saved to {self.output_file}")

    def run_scraper(self, search_term, num_scrolls=5):
        self.initialize_driver()
        self.login_with_cookies()
        self.search_posts(search_term)
        self.click_posts_filter()
        self.scroll_to_load_posts(num_scrolls)
        self.extract_data_from_posts(search_term)
        self.save_data_to_file(search_term)

        time.sleep(5)
        self.driver.quit()


