import requests
from bs4 import BeautifulSoup
import pandas as pd

def getMoPNews():
    url = 'https://powermin.gov.in/en/announcements'
    page = requests.get(url, verify=False)
    print(page, page.status_code)

    soup = BeautifulSoup(page.text, 'html.parser')
    #print(soup.prettify())

    listDates = list()
    news = soup.find_all(class_='date')
    for i, val in enumerate(news):
        #print(i,'->',val.text)
        listDates.append(val.text)

    listNews = list()
    listLinks = list()
    news2 = soup.find_all(class_='col-md-10')
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
    df = getMoPNews()
    