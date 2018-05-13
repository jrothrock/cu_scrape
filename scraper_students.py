import pandas as pd
import requests
import os
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from shutil import copy2 as copy

# Proof of concept. It's also possible to get emails from the student directory by inputting half a lastname, and scraping all available students.
    # not a bad way to verify the person too... This current way would just end up with more bounces - which would probably lead to more junk mail.

class ScraperStudent(object):
    def __init__(self, cookie=None, driver=webdriver.Chrome, scroll_pause=0.1, scroll_increment=300, timeout=10):
        if not cookie:
            raise ValueError(
                    'Must pass a cookie string to the ScraperStudent')
 
        self.driver = driver()
        self.scroll_pause = scroll_pause
        self.scroll_increment = scroll_increment
        self.timeout = timeout
        self.driver.get('http://www.linkedin.com')
        self.driver.set_window_size(1200, 1000)
        self.emails = []
        self.driver.add_cookie({
            'name': 'li_at',
            'value': cookie,
            'domain': '.linkedin.com'
        })
        try:
            os.remove('./cu_students.txt')
            os.remove('./cu_students_remaining.txt')
        except OSError:
            pass 

    def scrape_people(self,f):
        self.scroll_to_bottom()
        names = self.driver.find_elements(By.CSS_SELECTOR, ".name")
        regexp = re.compile(r'.')
        for name in names:
            try:
                if name.text != "LinkedIn Member" and '.' not in name.text and ' ' in name.text:
                    string_parts = name.text.replace('-','').split(' ')
                    email = string_parts[0] + '.' + string_parts[-1] + '@colorado.edu'
                    print email
                    self.emails.append(email)
                    f.write(email + '\n')
            except Exception as ex:
                print ex
                
    def scrape(self, url="https://www.linkedin.com/search/results/index/?keywords=Student%20at%20University%20of%20Colorado%20Boulder&origin=GLOBAL_SEARCH_HEADER"):
        self.driver.get(url)
        WebDriverWait(self.driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR,".name")))

        try:
            count = int(self.driver.find_element_by_class_name("search-results__total").text.split(' ')[1].replace(',', ''))
        except Exception as ex:
            print ex
            count = 99999
            pass

        throttle = 2
        amount = 3 # max amount of pages we want to go.
        start = 2

        with open("./cu_students.txt","a+") as f:
            self.scrape_people(f)
            while start < (count / 10) and start < amount:
                for attempt in range(3):
                    try:
                        button = self.driver.find_element_by_xpath("//li[@class='page-list']//button[contains(.,'" + str(start) + "')]")
                        start += 1
                        button.click()
                        WebDriverWait(self.driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".name")))
                        self.scrape_people(f)
                        time.sleep(throttle)
                    except Exception as ex:
                        print ex
                        self.scroll_to_bottom()
                    else:
                        break
        copy("./cu_students.txt", "./cu_students_remaining.txt")
        return self.emails


    def scroll_to_bottom(self):
        """Scroll to the bottom of the page
        Params:
            - scroll_pause_time {float}: time to wait (s) between page scroll increments
            - scroll_increment {int}: increment size of page scrolls (pixels)
        """

        current_height = 0
        while True:
            # Scroll down to bottom
            new_height = self.driver.execute_script(
                "return Math.min({}, document.body.scrollHeight)".format(current_height + self.scroll_increment))
            if (new_height == current_height):
                break
            self.driver.execute_script(
                "window.scrollTo(0, Math.min({}, document.body.scrollHeight));".format(new_height))
            current_height = new_height
            # Wait to load page
            time.sleep(self.scroll_pause)

    def __enter__(self):
        return self
    
    def __exit__(self, *args, **kwargs):
        self.quit()

    def quit(self):
        if self.driver:
            self.driver.quit()

# with ScraperStudent() as scraper:
    # scraper.scrape()