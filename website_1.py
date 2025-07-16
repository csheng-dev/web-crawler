# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 18:31:26 2025

@author: user
"""

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import time
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
import pandas as pd

# setting for the simulated browser


# create a list to store all results
result = []
key_words = ['skatepark', 'skate', 'bikepark', 'pumptrack park', 'action sport park']


for i in range(0, len(key_words)):
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    browser = webdriver.Chrome(options=option)
    browser.execute_cdp_cmd(
        'Page.addScriptToEvaluateOnNewDocument',
        {
            'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined});'
        }
    )
    
    
    browser.get('https://www.openpetition.de/suche')
    # print(browser.page_source)

    time.sleep(20)

    input = browser.find_element(By.NAME, 'search')


    
    # input a key word
    input.send_keys(key_words[i])

    time.sleep(20)

    button = browser.find_element(By.CSS_SELECTOR, 'td.gsc-search-button')
    button
    button.click()

    #browser.current_url
    #browser.page_source

    title = []
    link = []
    for p in range(1, 8): # crawl page 2 to page 8
        print(p)
        time.sleep(20)

        doc = pq(browser.page_source)
        
        
        # get the titles of all results on the current page
        
        content = doc('div.gs-title a.gs-title').items()
        cnt = 0
        for t in content:
            cnt += 1
            if cnt % 2 == 1 and cnt < 20:
                title.append(t.text())
                link.append(t.attr('data-ctorig'))
        
        #titles.remove('Online-petition')
        #titles.remove('Online-Petition')
        # use a function to clean the titles: clean_title()
        # function input: list of original titles
        # function output: list of clean titles
        
    
        time.sleep(40)
        
        # click on the next page - version 2.0
        
        try:
            # Wait until the button list is populated
            WebDriverWait(browser, 60).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "gsc-cursor-page"))
            )

            # Get all buttons and check if p is in range
            buttons = browser.find_elements(By.CLASS_NAME, "gsc-cursor-page")
            if p >= len(buttons):
                print("Index out of range")
                break

            button_next = buttons[p]

            # Wait until it's clickable
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable(button_next))

            # Scroll to it
            browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", button_next)

            # Short sleep for layout stabilizing (1–2s is usually enough)
            time.sleep(10)

            # Try clicking
            try:
                button_next.click()
            except ElementClickInterceptedException:
                # Try JS click as fallback
                browser.execute_script("arguments[0].click();", button_next)

        except (TimeoutException, IndexError) as e:
            print("no clickable:", e)
            break
        
        
    time.sleep(60)
    browser.close()
    file_name = '/Users/sheng/Library/CloudStorage/OneDrive-Personal/project/webcrawl/web_1_' + key_words[i] + '.csv'
    df = pd.DataFrame({
        'Title': title,
        'Link': link
    })
    df.to_csv(file_name, index = False)


