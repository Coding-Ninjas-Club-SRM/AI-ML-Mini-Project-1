import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

PATH = "C:\Program Files\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://www.sbipensionfunds.com/historical-nav/")

data_from = driver.find_element_by_name('fromdate')
data_from.send_keys("15-05-2009")
sleep(2)

data_to = driver.find_element_by_name('todate')
data_to.send_keys("20-09-2021")
driver.find_element_by_xpath("//table/tbody/tr/td/a[text()='17']")
sleep(2)

search = driver.find_element_by_name("mysubmit")
search.send_keys(Keys.RETURN)
sleep(2)

page_source = driver.page_source
soup = BeautifulSoup(page_source,'html.parser')

table = soup.find('table',class_="table table-hover table-condensed table-bordered")

final_data = []

for tr in table.find_all('tr'):
    data = []
    for td in tr.find_all('td'):
        data.append(td.get_text())
    final_data.append(data)

df = pd.DataFrame(final_data)
df.to_csv('data.csv', index= False)
sleep(5)
driver.quit()
