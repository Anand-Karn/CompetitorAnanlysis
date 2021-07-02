import requests
from bs4 import BeautifulSoup
import pandas as pd

def getMoPNews(kw):
    url = 'https://powermin.gov.in/en/search/node/'+kw
    page = requests.get(url, verify=False)
    print(page, page.status_code)

    soup = BeautifulSoup(page.text, 'html.parser')
    #print(soup.prettify())
    listNews = list()
    listLinks = list()    
    
    news2 = soup.find_all(class_='search-result')
    for i, val in enumerate(news2):
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
    df = getMoPNews('thermal')
    print(df)