import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

PATH = "/Users/gauravganju/Developer/WebDrivers/chromedriver"
driver = webdriver.Chrome(PATH)
driver.get("https://www.sbipensionfunds.com/historical-nav/")

DateFrom = driver.find_element_by_id("f_date_p1")
DateFrom.send_keys("25-05-2009")
DateTo = driver.find_element_by_id("f_date_p2")
DateTo.send_keys("15-10-2021")

sbttn = driver.find_element_by_name("mysubmit")
sbttn.click()

time.sleep(2)

webpage = driver.page_source
soup = BeautifulSoup(webpage, features="lxml")

table = soup.find("table", class_="table table-hover table-condensed table-bordered")
trows = table.findAll("tr")

res = []
for tr in trows:
    td = tr.findAll("td")
    row = [tr.text.strip() for tr in td if tr.text.strip()]
    if row:
        res.append(row)

dataf = pd.DataFrame(res)
print(dataf)
dataf.to_csv('hackerman.csv', index=False)
time.sleep(10)
driver.quit()
