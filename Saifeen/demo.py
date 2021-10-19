import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.maximize_window()
driver.get("https://www.sbipensionfunds.com/historical-nav/")

data_from = driver.find_element(By.ID,"f_date_p1")
data_from.send_keys("25-05-2009")

driver.find_element(By.ID,"f_date_p2").click()
driver.find_element(By.XPATH,"//table/tbody/tr/td/a[text()='17']").click()

search = driver.find_element(By.NAME,"mysubmit")
search.send_keys(Keys.RETURN)

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
df.to_csv('test.csv', index= False, header=False)
driver.quit()

