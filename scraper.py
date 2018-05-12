import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://experts.colorado.edu/people?source=%7B%22query%22%3A%7B%22match_all%22%3A%7B%7D%7D%2C%22sort%22%3A%5B%7B%22_score%22%3A%7B%22order%22%3A%22desc%22%7D%7D%5D%2C%22from%22%3A0%2C%22size%22%3A2986%7D"

driver = webdriver.Chrome()

# load the url above
driver.get(url)

# =================================
wait = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.TAG_NAME, "tr")))

table_id = driver.find_element(By.ID, 'facetview_results')
rows = table_id.find_elements(By.TAG_NAME, "tr")
emails = []
for row in rows:
    try:
        div = row.find_element_by_xpath('.//div[@class="person-info"]/div[2]')
        regexp = re.compile(r'Email:')
        if regexp.search(div.text):
            print div.text.split(' ')[1]
            emails.append(div.text.split(' ')[1])
    except Exception as ex:
        print ex # do whatever you want for debugging.
    
print emails.length
