import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import unquote



def getMNRE(keyword='solar'):

#Sec1:- getting number of pages from search results
    urls = ['https://mnre.gov.in/public-information/notifications','https://mnre.gov.in/public-information/news','https://mnre.gov.in/public-information/events','https://mnre.gov.in/public-information/current-notice','https://mnre.gov.in/public-information/office-orders']
    urls+=['https://mnre.gov.in/public-information/citizen-charter','https://mnre.gov.in/public-information/circulars']
    quotes=[]
    for url in urls:
        page = requests.get(url, verify=False)
    #print(page, page.status_code)
        soup = BeautifulSoup(page.text, 'html.parser')
        table = soup.findAll('div',attrs = {'class':'card'})
        for row in table:
            try:
                
           
                quote = {}
                cir_dt=row.button.text.rsplit('(IST)\r\n',1)[0]
                cir_text=row.button.text.rsplit('(IST)\r\n',1)[1]
                #quote['date']=cir_dt
                if keyword.upper() in cir_text.upper()):
                    
                    quote['Description']=cir_text.strip()
                    quote['Link'] = row.a['href']
                #quote['img'] = row.img['src']
                    quotes.append(quote)
                
            except:
                pass

    
    #print(table)
    df = pd.DataFrame(quotes)
    #print(df)
    return df

    
if __name__ == "__main__":    
    df = getNITIKW('Implementation')
    print(df)
    url = unquote('1%2C0%2C0')
    print(url.split(",")[0])