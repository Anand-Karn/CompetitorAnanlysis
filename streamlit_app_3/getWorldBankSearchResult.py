import requests
from bs4 import BeautifulSoup, Tag
import pandas as pd

def getMoPNews(kw):
    url = 'https://www.worldbank.org/en/search?q='+kw+"&currentTab=1"
    page = requests.get(url, verify=False)
    print(page, page.status_code)

    soup = BeautifulSoup(page.text, 'html.parser')
    #print(soup.prettify())
    listNews = list()
    listLinks = list()    
    
    news2 = soup.find(class_='col-md-10 col-lg-10 col-xs-12 col-sm-12')
    news2 = soup.find("ul", {"class": "list-group result-group"})
    #print( str(news2))

    for item in news2.findAll('li'):
        #print(item.text)
        pass
    

    for i, val in enumerate(news2.findAll('li')):
        dscr=""
        print(i,'->',val.text)
        lll =val.text.splitlines()# split based on newline character                
        for y in lll:
            dscr += " " + y

        listNews.append(' '.join(dscr.split()))
        links = val.findAll('a')
        for a in links:           
            listLinks.append(a['href'])


    #print(listLinks)

    df = pd.DataFrame(list(zip(listNews,  listLinks)),
               columns = ['Description',  'Link'])
    return df

if __name__ == "__main__":
    df = getMoPNews('Discoms')
    print(df)