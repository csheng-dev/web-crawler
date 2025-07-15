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
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
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
    for p in range(2, 8): # crawl page 2 to page 8
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

        # click on the next page
        
        try:
            button_next = browser.find_elements(By.CLASS_NAME, "gsc-cursor-page")[p]
            browser.execute_script("arguments[0].scrollIntoView(true);", button_next)
            time.sleep(30)
            button_next.click()
        #except IndexError:
        except (ElementClickInterceptedException, IndexError) as e:
            print("no clickable")
            break
    time.sleep(60)
    browser.close()
    file_name = '/Users/sheng/Library/CloudStorage/OneDrive-Personal/project/webcrawl/web_1_' + key_words[i] + '.csv'
    df = pd.DataFrame({
        'Title': title,
        'Link': link
    })
    df.to_csv(file_name, index = False)


