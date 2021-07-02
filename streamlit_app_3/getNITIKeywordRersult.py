import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import unquote



def getNITIKW(keyword='solar'):

#Sec1:- getting number of pages from search results
    url = 'http://niti.gov.in/search/node?keys='+keyword
    page = requests.get(url, verify=False)
    #print(page, page.status_code)
    soup = BeautifulSoup(page.text, 'html.parser')

    lastPage=0
    #here we used css class selector 'pager__item pager__item--last' for item having link for last page
    for EachPart in soup.select('li[class*="pager__item pager__item--last"]'):
        #get list of hyperlinks
        links = EachPart.findAll('a')
        for a in links:
            #used split function part of string after 'page='
            # https://niti.gov.in/search/node?q=search/node&keys=india&page=34
            lastPageStr = a['href'].split("page=",1)[1]
            lastPage=unquote(lastPageStr).split(",")[0]
    #print("Last Page in the list is = ", lastPage)
#End of Section 1 to fetch number of pages

#Section 2 : Construct Dataframe which contains texts and hyperlinks addresses
    listNews = list()#text for hyperlink
    listLinks = list()#url for hyperlinks

    count=0
    #iterator for each page, in case of multiple pages
    while (count<=int(lastPage)):
        #construct page wise url
        tmpUrl = url + "&page="+str(count)
        page = requests.get(tmpUrl, verify=False)
        #print(page, page.status_code, ", PageNum=", count,", URL="+tmpUrl)

        soup = BeautifulSoup(page.text, 'html.parser')

        #here all searched results are in ordered list based on css class selector
        for EachPart in soup.select('ol[class*="search-results node_search-results"]'):
            #print(EachPart)
            #now Ordered list contains search results in 'li' html tag
            abc = EachPart.findAll('li')
            #iterate over each <li> item
            for xyz in abc:
                #now reconstruct item description, if we directlt use .text, we will get
                # text having multiple spaces and new line characters
                txt = xyz.findAll('p')
                dscr = ""                
                for b in txt:
                    lll = b.text.splitlines()# split based on newline character                
                    for y in lll:
                        dscr += " " + y #construct description without newline character
                    #print("---", ' '.join(dscr.split()))
                
                #Add link description to list
                #used split and join to replace more than one space with single space
                listNews.append(' '.join(dscr.split()))
                
                #now fetch hyperlinks for current 'li' item
                links = xyz.findAll('a')
                for a in links:
                    #print("--<a href='"+a['href']+"'>"+  ' '.join(dscr.split())  +"</a>")
                    listLinks.append(a['href'])
                                    
        count += 1
    
    #finally construct dataframe and return the same
    df = pd.DataFrame(list(zip(listNews, listLinks)), columns = ['Description', 'Link'])
    
    return df

    
if __name__ == "__main__":    
    df = getNITIKW('wind')
    print(df)
    url = unquote('1%2C0%2C0')
    print(url.split(",")[0])