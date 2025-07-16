#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 22:31:07 2025

@author: sheng
"""

import random


proxies = [
    "http://179.60.53.25:999",                    # open proxy
    "http://147.75.34.105:443",
    "http://72.10.164.178:28247",
    "http://38.147.98.190:8080",
    "http://200.174.198.86:8888",
    "http://5.161.131.126:8081"    
]


# Choose one proxy at random
proxy = random.choice(proxies)


for i in range(20):  # simulate 10 requests
    proxy = random.choice(proxies)
    options = Options()
    options.add_argument(f'--proxy-server={proxy}')
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get("https://example.com")
    # scrape what you need
    driver.quit()