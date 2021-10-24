
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


url= 'https://www.sbipensionfunds.com/historical-nav/'

driver = webdriver.Chrome()
driver.get(url)

text_input1 = driver.find_element_by_id("f_date_p1")
text_input1.send_keys("15-05-2009")
text_input2 = driver.find_element_by_id("f_date_p2")
text_input2.send_keys("20-10-2021")
search_button = driver.find_element_by_name("mysubmit")
search_button.click()
driver.page_source

doc = BeautifulSoup(driver.page_source, "html.parser")

table = doc.find_all('table')
data = pd.read_html(str(table))[1]

df = data
print(df)

df.to_csv('sbi.csv', encoding='utf-8', index=False)

driver.close()
