import requests
from bs4 import BeautifulSoup

def getIEANew():
    url = 'https://www.iea.org/news'
    page = requests.get(url)
    print(page, page.status_code)

    soup = BeautifulSoup(page.text, 'html.parser')
    #print(soup.prettify())
    """
    news = soup.find_all(class_='m-news-listing__hover', text=True)
    for i, val in enumerate(news):
        print (i, "->",val.text)
    """
    lr = list()
    news = soup.find_all(class_='m-news-listing')
    #print(news)
    for i, val in enumerate(news):
        #print(i,'->',val.text)

        lll = val.text.splitlines()
        

        for val2 in lll:
            ttt = val2.strip()
            if(len(ttt)>0):
                lr.append(val2.strip())
        
        links = val.findAll('a')
        for a in links:
            #print('https://www.iea.org'+a['href'])
            lr.append('https://www.iea.org'+a['href'])
        #print(lr) 
    return lr

