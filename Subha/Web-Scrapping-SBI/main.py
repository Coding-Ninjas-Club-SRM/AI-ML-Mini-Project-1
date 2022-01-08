# import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
# import time
from datetime import date
from bs4 import BeautifulSoup
# import bs4
import pandas as ps

ser = Service("C:/Users/mohit/OneDrive/Desktop/Github/CN-Projects/Web-Scrapping-SBI/msedgedriver.exe")
# driver_location = "C:/Users/mohit/OneDrive/Desktop/Github/CN-Projects/Web-Scrapping-SBI/msedgedriver.exe"
driver = webdriver.Edge(service=ser)
driver.minimize_window()
driver.get("https://www.sbipensionfunds.com/historical-nav/")
# driver.minimize_window()
# time.sleep(10)
a = date.today()
print(a)

driver.find_element(By.NAME, "fromdate").send_keys("15-05-2009")
driver.find_element(By.NAME, "todate").send_keys(a.day, "-", a.month, "-", a.year)
# time.sleep(10)

driver.find_element(By.NAME, "mysubmit").click()

html_content = driver.page_source
# print(t)

soup = BeautifulSoup(html_content, 'html5lib')
# print(beauty.prettify)

tbody = soup.find("table", class_="table table-hover table-condensed table-bordered")

# inside = table.find_all('tr')

rows = tbody.find_all('tr')
# td = tbody.find("td")
# print(type(table))
# print(rows)
# print(td)
data_list = []

for values in rows:
    value = values.find_all('td')
    list = []
    for key in value:
        text = key.get_text()
        list.append(text)
        # print(text, end='')
        # print(list)
        # print(type(key))
    # print(list)
    data_list.append(list)
    # print(value)
    # print(type(value))

# for values in table:
#     tr = values.find_all('tr')
#     for value in tr:
#         td = values.find_all('td')
#         print(td)
print(data_list)

pd = ps.DataFrame(data_list)

pd.to_csv('scraped_data.csv', index=False, header=False)

driver.quit()