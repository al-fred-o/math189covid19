import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

url = 'https://www.foxnews.com/category/shows/the-five/transcript'
r1 = requests.get(url)
coverpage = r1.content

soup1 = BeautifulSoup(coverpage, 'html5lib')
coverpage_news = soup1.find_all('h4', class_ ='title')

print(coverpage_news[4].get_text())

# Scraping the first 5 articles
number_of_articles = 5
# Empty lists for content, links and titles
news_contents = []
list_links = []
list_titles = []

for n in np.arange(0, number_of_articles):
    
    # Getting the link of the article
    link = coverpage_news[n].find('a')['href']
    link = 'https://www.foxnews.com/' + link
    list_links.append(link)

    print(list_links)
    
    # Getting the title
    title = coverpage_news[n].find('a').get_text()
    list_titles.append(title)

    print(list_titles)
    
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