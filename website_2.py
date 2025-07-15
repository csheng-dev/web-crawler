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
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

# setting for the simulated browser



key_words = ['skatepark', 'skate', 'bikepark', 'pumptrack park', 'action sport park']

for i in range(0, len(key_words)):
    # create lists to store result
    result_title = []
    result_signature = []
    result_location = []
    result_startingDate = []
    result_link = []
    
    # start a simulated web browser
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
    
    time.sleep(60)

    browser.get('https://www.change.org/search')
    # print(browser.page_source)

    time.sleep(20)

    # find the search buttun
    input = browser.find_element(By.ID, "search-input")
    
    # input a key word
    input.send_keys(key_words[i])

    time.sleep(20)

    # click the search buttun
    button = browser.find_element(By.CSS_SELECTOR, "#rootApp > div.corgi-1yz7e9k > div.corgi-eme4ej > div > div > div > div.mt-4.md\:mt-16 > div.container.w-full > div > form > button")
    time.sleep(30)
    button.click()

    #browser.current_url
    #browser.page_source


    for p in range(2, 8): # crawl page 2 to page 8
        print('p = ', p)
        time.sleep(20)

        doc = pq(browser.page_source)
        
        # get the info needed on the current page
        titles = doc('a[tabindex="0"][data-discover="true"] span[data-variant="heading"]')
        signatures = doc('span.font-sans.text-size-heading-xxs')  
        locations = doc('p.text-typography-weak')
        starting_dates = text = doc('span.text-typography-weak')
        links = doc('article a.link-overlay').items()        

        base_url = 'www.change.org'

        # store crawled info
        for a in links:
            href = a.attr('href')
            if href:
                # Make full URL 
                full_url = base_url + href if href.startswith("/") else href
                result_link.append(full_url)


        for j in range(len(titles)):
            result_title.append(titles[j].text)
            result_signature.append(signatures[j].text)
            result_location.append(locations[j].text)
            result_startingDate.append(starting_dates[2*j+1].text)
        time.sleep(20)

        # click on the next page
        
        label_name = "Jump to page " + str(p)
        try:
            button_next = browser.find_element(By.XPATH, "//button[@aria-label='" + label_name + "']") 
        except NoSuchElementException:
            break
        button_next.click()
    time.sleep(60)
    browser.close()
    
    # transform the result into dataframe and save it in .csv file
    df = pd.DataFrame({
        "Title": result_title,
        "No. of Signatures": result_signature,
        "Location": result_location,
        "Starting Date": result_startingDate,
        "Link": result_link
    })
    
    # save the result
    file_name = '/Users/sheng/Library/CloudStorage/OneDrive-Personal/project/webcrawl/web_2_' + key_words[i] + '.csv'
    df.to_csv(file_name, index = False)

    

    
print(result)


