from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
import pandas as pd
from bs4 import BeautifulSoup

def getEprocureData(keyword="wind"):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome("D:/SOFTWARE DEVELOPMENT/python/streamlit_app_3/chromedriver_win32/chromedriver.exe", options = options)
    #driver.maximize_window()
    driver.get("https://eprocure.gov.in/eprocure/app")
    driver.find_element_by_name("SearchDescription").send_keys(keyword) 
    driver.find_element_by_name("Go").send_keys(Keys.ENTER)
    tbl = driver.find_element_by_class_name("list_table").get_attribute('outerHTML')
    df  = pd.read_html(tbl)
    df = df[0].iloc[:,0:6]
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    gdp_table = soup.find("table", attrs={"class": "list_table"})
    
    #close the browser  
    driver.close()  
    return df.dropna(axis=0, thresh=4)
    """
    dscr=""
    lll = gdp_table.splitlines()# split based on newline character                
    for y in lll:
        dscr += " " + y #construct description without newline character


    return ' '.join(dscr.split()) 
    """
    
if __name__ == "__main__":    
    df=getEprocureData("wind")
    print(df)