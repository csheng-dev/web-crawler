#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  6 22:22:49 2025

@author: sheng
"""
import pandas as pd

def clean(titles):
    try:
        titles.remove('Online-petition')
    except ValueError:
        pass
    try:
        titles.remove('Online-Petition')
    except ValueError:
        pass
    try:
        titles.remove('Online petition')
    except ValueError:
        pass 
    try:
        titles.remove('Online-Petition')
    except ValueError:
        pass 
    
    return(titles)

key_words = ['skatepark', 'skate', 'bikepark', 'pumptrack park', 'action sport park']
for i in range(len(key_words)):
    file_name = '/Users/sheng/Library/CloudStorage/OneDrive-Personal/project/webcrawl/web_1_' + key_words[i] + '.txt'
    #df = pd.read_csv(file_name, encoding="utf-8")
    #titles = df[0].tolist()
    with open(file_name, 'r', encoding='utf-8') as f:
        titles = f.read().splitlines()
    result = clean(titles)
    print(i)
    print(result)
    file_name = '/Users/sheng/Library/CloudStorage/OneDrive-Personal/project/webcrawl/webcrawl_result/web_1_' + key_words[i] + '.txt'
    with open(file_name, 'w') as file:
        for item in result:
            file.write(f"{item}\n")


 