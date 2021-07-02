from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
import pandas as pd

def getEprocureData(keyword="wind"):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome("D:/SOFTWARE DEVELOPMENT/python/streamlit_app_3/chromedriver_win32/chromedriver.exe", options = options)
    #driver.maximize_window()
    driver.get("https://eprocure.gov.in/eprocure/app")
    driver.find_element_by_name("SearchDescription").send_keys("wind") 
    driver.find_element_by_name("Go").send_keys(Keys.ENTER)
    tbl = driver.find_element_by_class_name("list_table").get_attribute('outerHTML')
    df  = pd.read_html(tbl)
    #close the browser  
    driver.close()  
    return df