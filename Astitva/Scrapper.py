from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from datetime import date
import csv
def Scrapper():
    driver = webdriver.Chrome('D:\GIT\CN\AI-ML-Mini-Project-1-\Astitva\chromedriver.exe')
    driver.get("https://www.sbipensionfunds.com/historical-nav/")
    datefield1=driver.find_element_by_id('f_date_p1')
    datefield2=driver.find_element_by_id('f_date_p2')
    ActionChains(driver).move_to_element(datefield1).click().send_keys('15-05-2009').perform()
    ActionChains(driver).move_to_element(datefield2).click().send_keys(date.today().strftime("%d-%m-%y")).perform()
    search_btn = driver.find_element_by_name('mysubmit')
    ActionChains(driver).move_to_element(search_btn).click().click().perform()


    filename='test.csv'
    csv_writer=csv.writer(open(filename,'w'))


    soup = BeautifulSoup(driver.page_source,'html.parser')


    for tr in soup.find_all('tr')[1:]:
        data=[]

        for td in tr.find_all('td'):
            data.append(td.text.rstrip())
        if(data):
            print("Inserting Table data: {}".format(','.join(data)))
            csv_writer.writerow(data)
    driver.quit
Scrapper()