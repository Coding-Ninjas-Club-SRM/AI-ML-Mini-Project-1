from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from csv import writer

driver = webdriver.Chrome("D:\chromedriver")
source =driver.get("https://www.sbipensionfunds.com/historical-nav/")

FromDate=driver.find_element(By.ID,"f_date_p1")
ToDate=driver.find_element(By.ID,"f_date_p2")
Search=driver.find_element(By.NAME,"mysubmit")
ActionChains(driver).move_to_element(FromDate).click().send_keys("15-05-2009").perform()
ActionChains(driver).move_to_element(ToDate).click().send_keys("20-10-2021").perform()
ActionChains(driver).move_to_element(Search).click().perform()
soup = BeautifulSoup(driver.page_source,'html.parser')


with open("SBIscraper.csv","w") as s:
  thewriter = writer(s)
  
  for trow in soup.find_all("tr"):
    data=[] 
    for tdata in trow.find_all("td"):
        data.append(tdata.text.rstrip())
    if(data):
        print("Data: {}".format(','.join(data)))
        thewriter.writerow(data)