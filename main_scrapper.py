
"""
    Book Store Scrapper
    main_scrapper.py

    இڿڰۣ-ڰۣ—
    ~Created by:    Santiago Bustamante (｡•̀ᴗ-)✧
    ~e-mail:        santiago.bustamanteq@gmail.com

    ~Start date: 2022/02/07
    ~Last mod:   2022/02/07
    இڿڰۣ-ڰۣ—

    ChromDriver version works for Google Chrome 133, the latest stable version up to last mod date

    exec(open("main_scrapper.py").read())

"""

import numpy as np
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import openpyxl

if __name__ == "__main__":

    books_df = pd.DataFrame({}, columns=["link", "title", "type", "upc", "price", "in_stock", "rating", "tax", "no_tax_price",  "no_reviews", "description"])

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

    driver = webdriver.Chrome(service=service, options=chrome_options)  # Initialize webdriver

    hrefs = pd.read_excel("book_links.xlsx").values[:,0]

    star_rating_dict = {
        "One" : 1,
        "Two" : 2,
        "Three" : 3,
        "Four" : 4,
        "Five" : 5,
    }

    for href in hrefs[:]: # limiting to the first 20 books for testing

        link = homepage+"catalogue/"+href

        driver.get(link)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")

        product_main = soup.find("div", {"class": "col-sm-6 product_main"})

        title = product_main.find("h1").get_text()

        price = float(product_main.find("p", {"class":"price_color"}).get_text()[1:])

        instock = int(re.findall("\d.",
                         product_main.find("p", {"class":"instock availability"}).get_text())[0])
        
        star_rating = star_rating_dict[product_main.find_all("p")[-1]["class"][1]]

        try:
            description = soup.find("div", {"id": "product_description"}).find_next("p").get_text()
        except AttributeError:
            description = ""

        table_rows = soup.find("table").find_all("tr")

        upc = table_rows[0].find("td").get_text() 

        Type = table_rows[1].find("td").get_text()

        notax_price = float(table_rows[2].find("td").get_text()[1:])

        tax = float(table_rows[4].find("td").get_text()[1:])

        no_reviews = int(table_rows[6].find("td").get_text())

        df = pd.DataFrame([[link,title,Type, upc, price, instock, star_rating, tax, notax_price, no_reviews, description]], columns=books_df.columns)

        books_df = pd.concat([books_df, df], ignore_index=True)

    books_df.to_excel("book_database.xlsx", index=False)
