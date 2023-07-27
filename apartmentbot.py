from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time

APARTMENTS_URL = "https://www.apartments.com/"
DRIVER_PATH = "C:/Users/stefa/Downloads/chromedriver_win32/chromedriver.exe"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdFNqSD0XQziBTmDcNpYNQXRiJ8xznQ6jSBPyYNhgMEIcxfqg/viewform"


class ApartmentBot:

    def __init__(self):
        self.names_list = []
        self.prices_list = []
        self.url_list = []
        self.serv = Service(DRIVER_PATH)
        self.options = webdriver.ChromeOptions() # options to avoid captchas
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option("useAutomationExtension", False)
        self.driver = webdriver.Chrome(service=self.serv, options=self.options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def apartment_lookup(self):
        city_entry = input("Please enter a city to lookup: ")
        min_entry = input("Please enter a minimum price value: ")
        max_entry = input("Please enter a maximum price value: ")
        self.driver.get(url=APARTMENTS_URL) # open url after getting entries
        time.sleep(3.5)
        search_box = self.driver.find_element(By.ID, "quickSearchLookup")
        search_box.send_keys(city_entry)
        time.sleep(1.5)
        go_button = self.driver.find_element(By.CLASS_NAME, "go")
        go_button.click()
        time.sleep(4)
        range_button = self.driver.find_element(By.ID, "rentRangeLink")
        range_button.click()
        time.sleep(2)
        min_range = self.driver.find_element(By.ID, "min-input")
        min_range.send_keys(min_entry)
        max_range = self.driver.find_element(By.ID, "max-input")
        max_range.send_keys(max_entry)
        range_button.click()
        time.sleep(3)

    def scrape_data(self):
        names = self.driver.find_elements(By.CLASS_NAME, "js-placardTitle")
        prices = self.driver.find_elements(By.CLASS_NAME, "property-pricing")
        links = self.driver.find_elements(By.CLASS_NAME, "property-link")

        for i in range(0, len(names)):
            self.names_list.append(names[i].text)
            self.prices_list.append(prices[i].text)
            self.url_list.append(links[i].get_attribute("href"))

    def submit_data(self):

        for i in range(0, len(self.names_list)):
            self.driver.get(url=FORM_URL) # swap to google forms after scraping data
            time.sleep(2)

            form_inputs = self.driver.find_elements(By.CLASS_NAME, "whsOnd.zHQkBf")
            form_button = self.driver.find_element(By.CLASS_NAME, "UQuaGc")

            time.sleep(2)
            form_inputs[0].send_keys(self.names_list[i])
            time.sleep(1)
            form_inputs[1].send_keys(self.prices_list[i])
            time.sleep(1)
            form_inputs[2].send_keys(self.url_list[i])
            time.sleep(1)
            form_button.click()
            time.sleep(1.5)

        self.driver.close()
