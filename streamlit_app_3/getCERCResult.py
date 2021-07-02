from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep

def getEprocureData(keyword="wind"):
    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    driver = webdriver.Chrome("D:/SOFTWARE DEVELOPMENT/python/streamlit_app_3/chromedriver_win32/chromedriver.exe", options = options)
    driver.maximize_window()
    driver.get("https://cercind.gov.in/search.html")
    driver.find_element_by_id("gsc-i-id1").send_keys(keyword) 
    #driver.find_element_by_class_name("gsc-search-button gsc-search-button-v2").send_keys(Keys.ENTER)
    
    driver.find_element_by_xpath("//button[@class='gsc-search-button gsc-search-button-v2']").click()
    

    print(driver.page_source)

    driver.set_page_load_timeout(30)
    sleep(10)
    listNews = driver.find_elements_by_class_name("gsc-webResult gsc-result")
    print("Total Iterms Fetche=" , len(listNews) )
    for i in listNews:
        print("Store names:"+ i.text)
    driver.close()
    """
    df  = pd.read_html(tbl)
    df = df[0].iloc[:,0:6]
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    gdp_table = soup.find("table", attrs={"class": "list_table"})
    
    #close the browser  
    driver.close()  
    return df.dropna(axis=0, thresh=4)
    """
    
    """
    dscr=""
    lll = gdp_table.splitlines()# split based on newline character                
    for y in lll:
        dscr += " " + y #construct description without newline character


    return ' '.join(dscr.split()) 
    """
    
if __name__ == "__main__":    
    df=getEprocureData("solar")
    #print(df)