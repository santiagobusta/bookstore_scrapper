
"""
    Book Store Scrapper
    link_scrapper.py

    இڿڰۣ-ڰۣ—
    ~Created by:    Santiago Bustamante (｡•̀ᴗ-)✧
    ~e-mail:        santiago.bustamanteq@gmail.com

    ~Start date: 2022/01/13
    ~Last mod:   2022/02/07
    இڿڰۣ-ڰۣ—

    ChromDriver version works for Google Chrome 133, the latest stable version up to last mod date

"""

import numpy as np
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import openpyxl

if __name__ == "__main__":
    
    links_df = pd.DataFrame({}, columns=["link"])

    homepage = "https://books.toscrape.com/"
    service = webdriver.ChromeService(executable_path="./chromedriver-win64/chromedriver.exe")
    chrome_options = webdriver.ChromeOptions()  # Class for managing Chrome options
    # chrome_options.add_argument("--headless")
    #chrome_options.add_argument("--disable-single-click-autofill")
    #chrome_options.add_argument("--disable-autofill-keyboard-accessory-view[8]")
    #chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    #chrome_options.add_experimental_option('useAutomationExtension', False)
    prefs = {"profile.default_content_setting_values.notifications": False}  # Disable chrome notifications
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=service, options=chrome_options)  # Initialize webdriver, works for Google Chrome version 133

    for page in range(1,51):
        driver.get(homepage+"catalogue/page-{:d}.html".format(page)) # Enter catalogue page

        soup = BeautifulSoup(driver.page_source, "html.parser")

        all_hrefs = [[link.get("href")] for link in soup.find_all("a") if 
                     not ( re.findall("^category/book", link.get("href")) or re.findall("^page", link.get("href")) ) ]

        all_hrefs = all_hrefs[2::2] # Ignore firts two elements, and since every link is repeated once skip one element of every two

        links_df = pd.concat([links_df, pd.DataFrame(all_hrefs, columns=["link"])], ignore_index=True)

    links_df.to_excel("book_links.xlsx", index=False)
