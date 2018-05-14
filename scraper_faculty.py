import pandas as pd
import requests
import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from shutil import copy2 as copy
import time

class ScraperFaculty(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.emails = []
        try:
            os.remove('./cu_research_faculty.txt')
            os.remove('./cu_research_faculty_remaining.txt')
        except OSError:
            pass 
    
    def scrape(self):
        url = "https://experts.colorado.edu/people?source=%7B%22query%22%3A%7B%22match_all%22%3A%7B%7D%7D%2C%22sort%22%3A%5B%7B%22_score%22%3A%7B%22order%22%3A%22desc%22%7D%7D%5D%2C%22from%22%3A0%2C%22size%22%3A2986%7D"
        self.driver.get(url)
        time.sleep(5)
        wait = WebDriverWait(self.driver, 100).until(EC.visibility_of_element_located((By.TAG_NAME, "tbody")))

        table_id = self.driver.find_element(By.ID, 'facetview_results')
        rows = table_id.find_elements(By.TAG_NAME, "tr")

        with open("./cu_research_faculty.txt","a+") as f:
            for row in rows:
                try:
                    div = row.find_element_by_xpath('.//div[@class="person-info"]/div[2]')
                    regexp = re.compile(r'Email:')
                    if regexp.search(div.text):
                        print div.text.split(' ')[1]
                        self.emails.append(div.text.split(' ')[1])
                        f.write(div.text.split(' ')[1] + '\n')
                except Exception as ex:
                    print ex # do whatever you want for debugging.
        
        copy('./cu_research_faculty.txt', './cu_research_faculty_remaining.txt')
        return self.emails

    def __enter__(self):
        return self
    
    def __exit__(self, *args, **kwargs):
        self.quit()

    def quit(self):
        if self.driver:
            self.driver.quit()

# with ScraperFaculty() as scraper:
#     scraper.scrape()