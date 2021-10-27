from selenium import webdriver
from datetime import date
from bs4 import BeautifulSoup
import pandas as pd
url='https://www.sbipensionfunds.com/historical-nav/'

driver=webdriver.Chrome("C:\\Users\\udaud\\Desktop\\PYHTON\\scraping\\chromedriver.exe")
driver.get(url)
driver.find_element_by_name("fromdate").send_keys("15-05-2009")
driver.find_element_by_name("todate").send_keys(date.today().strftime("%d-%m-%Y"))
driver.find_element_by_name("mysubmit").click()
html_code = driver.page_source
soup = BeautifulSoup(html_code, 'html.parser')
table = soup.find("table", class_="table table-hover table-condensed table-bordered")
table_rows = table.find_all("tr")
data_csv=[]
for i in table_rows:
    row =i.find_all("td")
    data_row=[data.text for data in row ]
    data_csv.append(data_row)
df=pd.DataFrame(data_csv) 
print(df)
df.to_csv('C:\\Users\\udaud\\Desktop\\PYHTON\\scraping\\data.csv',index=False)