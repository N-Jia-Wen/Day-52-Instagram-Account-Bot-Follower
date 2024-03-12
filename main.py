from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
import time
import os

SIMILAR_ACCOUNT = "londonappbrewery"
EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]


class InstaFollower:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(chrome_options)

    def login(self):
        self.driver.get("https://www.instagram.com/")
        time.sleep(2)
        inputs = self.driver.find_elements(By.TAG_NAME, "input")
        enter_email = inputs[0]
        enter_password = inputs[1]
        enter_email.send_keys(EMAIL)
        enter_password.send_keys(PASSWORD, Keys.ENTER)
        time.sleep(5)

        reject_popup = self.driver.find_element(By.CLASS_NAME, "_ac8f")
        reject_popup.click()
        time.sleep(1)

        reject_notif = self.driver.find_element(By.CLASS_NAME, "_a9_1")
        reject_notif.click()
        time.sleep(1)

    def find_followers(self):
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}/")
        time.sleep(3)
        account_followers = self.driver.find_element(By.PARTIAL_LINK_TEXT, "followers")
        account_followers.click()
        time.sleep(5)

        # Taken from stackoverflow:

        followers = self.driver.find_element(By.CLASS_NAME, "_aano")
        for i in range(10):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers)
            time.sleep(4)

    def follow(self):
        follow_button_list = self.driver.find_elements(By.CSS_SELECTOR, "._aano button")
        for follow_button in follow_button_list:
            try:
                follow_button.click()

            except ElementClickInterceptedException:
                cancel_action = self.driver.find_element(by=By.XPATH, value="//button[contains(text(), 'Cancel')]")
                cancel_action.click()
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", follow_button)

            finally:
                time.sleep(1)


follow_bot = InstaFollower()
follow_bot.login()
follow_bot.find_followers()
follow_bot.follow()
