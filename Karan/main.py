from re import search
import requests
import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd

option=webdriver.ChromeOptions
option.binary_location='C:\Program Files\Google\Chrome\Application\chrome.exe'
location = 'C:/Users/karan/Downloads/chromedriver_win32/chromedriver'
driver = webdriver.Chrome(location)
driver.get('https://www.sbipensionfunds.com/historical-nav/')

def automation():
    frompath='//*[@id="f_date_p1"]'
    topath='//*[@id="f_date_p2"]'
    searchdata="/html/body/section/div/div/div/div/div/div/div/table/tbody/tr/td[5]/input"

    driver.find_element_by_xpath(frompath).send_keys("15-05-2009")
    driver.find_element_by_xpath(topath).send_keys(date.today().strftime("%d-%m-%Y"))
    driver.find_element_by_xpath(searchdata).click()
    driver.implicitly_wait(10)
    datafind()

def datafind():
    L=[]
    bs = BeautifulSoup(driver.page_source,'html5lib')
    table= bs.find("table",class_="table table-hover table-condensed table-bordered")
    rows= table.find_all("tr")

    for i in rows:
        data= i.find_all("td")
        L1=[]
        for j in data:
            L1.append(j.text.strip())
        L.append(L1)

    csvmode= pd.DataFrame(L)
    csvmode.to_csv('Mazic.csv',index=False)

automation()
print("Process Done")
driver.quit()




