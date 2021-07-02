import requests
from bs4 import BeautifulSoup
import pandas as pd

def getSPWNews():
    url = 'https://www.solarpowerworldonline.com/category/industry-news'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    page = requests.get(url, headers=headers)
    print(page, page.status_code)

    soup = BeautifulSoup(page.text, 'html.parser')
    #print(soup.prettify())

    listDates = list()
    news = soup.find_all(class_='entry-meta')
    for i, val in enumerate(news):
        #print(i,'->',val.text)
        listDates.append(val.text)

    listNews = list()
    listLinks = list()
    news2 = soup.find_all(class_='entry-title')
    for i, val in enumerate(news2):
        print(i,'->',val.text)
        listNews.append(val.text)
        links = val.findAll('a')
        for a in links:
            #print('https://www.iea.org'+a['href'])
            listLinks.append(a['href'])


    #print(listLinks)

    df = pd.DataFrame(list(zip(listNews, listDates, listLinks)),
               columns = ['Description', 'Type' , 'Link'])
    return df

if __name__ == "__main__":
    df = getSPWNews()
    print(df)
    