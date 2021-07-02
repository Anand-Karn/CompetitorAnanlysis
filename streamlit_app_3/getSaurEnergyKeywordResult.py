import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import unquote

from soupsieve.util import lower



def getSaurEnergyKW(keyword='electric-truck'):

#Sec1:- getting number of pages from search results
    url = 'https://www.saurenergy.com/topic/'+keyword+"/page/1"
    page = requests.get(url, verify=False)
    print(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    newsList = list()
    listLinks = list()
    pageNo=1
    while True:
        url = 'https://www.saurenergy.com/topic/'+keyword+"/page/"+str(pageNo)
        page = requests.get(url, verify=False)
        print(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        news = soup.find_all(class_='entry-inner content-list')
        print("Article Size="+ str(len(news)))
        if(len(news)<=0):
            break        
        if(pageNo>2):
            break

        for EachPart in news:
            #get list of hyperlinks
            lll = EachPart.text.splitlines()# split based on newline character                
            dscr=""
            for y in lll:
                dscr += " " + y
            
            #print(EachPart.text)
            newsList.append(' '.join(dscr.split()))
            print(dscr)

            links = EachPart.findAll('a')
            for a in links:                
                listLinks.append(a['href'])
        pageNo +=1

    df = pd.DataFrame(list(zip(newsList, listLinks)), columns = ['Description', 'Link'])
    
    return df
    
    
if __name__ == "__main__":    
    df=getSaurEnergyKW("electric-distribution")

    print(df)

    #url = unquote('1%2C0%2C0')
    #print(url.split(",")[0])