import requests
from bs4 import BeautifulSoup
import pandas as pd

def getMoPNews():
    url = 'https://www.seci.co.in/view/publish/tender?tender=all'
    page = requests.get(url, verify=False)
    print(page, page.status_code)

    soup = BeautifulSoup(page.text, 'html.parser')
    #print(soup.prettify())


    gdp_table = soup.find("table", attrs={"id": "example"})
    gdp_table_data = gdp_table.tbody.find_all("tr")  

    # Get all the headings of Lists
    tbl=[]
    for tr in gdp_table_data:
        headings = []
        for td in tr.find_all("td"):
            # remove any newlines and extra spaces from left and right
            headings.append(td.text)
            #pass
        tbl.append(headings)
        print(headings)

    print(tbl)

"""
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
"""

def getSECITender():
    url = 'https://www.seci.co.in/view/publish/tender?tender=all'
    page = requests.get(url, verify=False)
    print(page, page.status_code)

    soup = BeautifulSoup(page.text, 'html.parser')
    #print(soup.prettify())


    gdp_table = soup.find("table", attrs={"id": "example"})
    print(gdp_table)
    df = pd.read_html(str(gdp_table))[0]
    #df = df[1:]
    #print(df.iloc[:,:].head())
    return df


if __name__ == "__main__":
    #df = getMoPNews()
    getSECITender()