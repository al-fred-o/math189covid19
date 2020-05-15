import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,StaleElementReferenceException

import time

transcripts = pd.read_csv('fox_transcripts.csv')
source = 'FOX'
url = 'https://www.foxnews.com/category/shows/the-five/transcript'

driver = webdriver.Chrome()
driver.get(url)
for i in range(20):
    print("pressing load more button")
    load_more = driver.find_element_by_class_name("button.load-more.js-load-more")
    load_more.click()
    time.sleep(2)

coverpage = driver.page_source

soup1 = BeautifulSoup(coverpage, 'html5lib')
coverpage_news = soup1.find_all('h4', class_ ='title')

print(coverpage_news[4].get_text())

# Scraping 120 articles
number_of_articles = 120
# Empty lists for content, links and titles
news_contents = []
list_links = []
list_titles = []

for n in np.arange(0, number_of_articles):
    
    # Getting the link of the article
    link = coverpage_news[n].find('a')['href']
    link = 'https://www.foxnews.com/' + link
    list_links.append(link)
    
    # Getting the title
    title = coverpage_news[n].find('a').get_text()
    list_titles.append(title)
    
    # Reading the content (it is divided in paragraphs)
    article = requests.get(link)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all('div', class_='article-body')
    x = body[0].find_all('p')
    
    # Unifying the paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        final_article = " ".join(list_paragraphs)
        
    news_contents.append(final_article)
    print(final_article)
    data = {'Source': source, 'Text': final_article}
    transcripts = transcripts.append(data, ignore_index= True)
    print(transcripts)

driver.quit()
transcripts.to_csv(r'fox_transcripts.csv', index=True, header=True)

news_contents = []
list_links = []
list_titles = []

transcripts = pd.read_csv('cnn_transcripts.csv')
source = 'CNN'
start = 0
page = 1

driver = webdriver.Chrome()

num = 0

for i in range(25):
    url = 'https://www.cnn.com/search?q=transcript&size=10&from={}&page={}'.format(start, page)
    print(url)
    driver.get(url)
    time.sleep(3)

    coverpage = driver.page_source

    soup1 = BeautifulSoup(coverpage, 'html5lib')
    coverpage_news = soup1.find_all('h3', class_ ='cnn-search__result-headline')

    print(coverpage_news[0].get_text())

    # Scraping 10 articles per page
    number_of_articles = 10
    # Empty lists for content, links and titles
    

    for n in np.arange(0, number_of_articles):
        num += 1
        print(num)
        if num == 24 or num == 25 or num == 41 or num == 49 or num == 65 or num == 124 or num == 152 or num == 156 or num == 170 or num == 178 or num == 181 or num == 191 or num == 200 or num == 203 or num == 208 or num == 220 or num == 235:
            continue
        
        # Getting the link of the article
        link = coverpage_news[n].find('a')['href']
        link = 'https:' + link
        list_links.append(link)

        print(link)
        
        # Getting the title
        title = coverpage_news[n].find('a').get_text()
        list_titles.append(title)
        
        # Reading the content (it is divided in paragraphs)
        article = requests.get(link)
        article_content = article.content
        soup_article = BeautifulSoup(article_content, 'html5lib')
        try:
            body = soup_article.find_all('div', class_='zn-body__read-all')
            print(body)
            x = body[0].find_all('div', class_='zn-body__paragraph')
        except:
            print("except")
            body = soup_article.find_all('div', class_='Paragraph__component')
            print(body)
            x = body[0].find_all('span')
        
        # Unifying the paragraphs
        list_paragraphs = []
        for p in np.arange(0, len(x)):
            paragraph = x[p].get_text()
            list_paragraphs.append(paragraph)
            final_article = " ".join(list_paragraphs)
            
        news_contents.append(final_article)
        print(final_article)
        data = {'Source': source, 'Text': final_article}
        transcripts = transcripts.append(data, ignore_index= True)
        print(transcripts)
    
    start += 10
    page += 1

driver.quit()
transcripts.to_csv(r'cnn_transcripts.csv', index=True, header=True)
    