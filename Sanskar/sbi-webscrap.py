from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import date
from time import sleep
import pandas as pd
from bs4 import BeautifulSoup


def get_date():
    today = date.today()
    date_today = today.strftime("%d")
    month = today.strftime("%m")
    year = today.strftime("%Y")
    return date_today, month, year


driver = webdriver.Chrome(ChromeDriverManager().install())
wt = driver.implicitly_wait

columns_defined = [["Date"], ["CG Scheme"], ["SG Scheme"], ["E Tier I"], ["C Tier I"], ["G Tier I"], ["E Tier II"], [
    "C Tier II"], ["G Tier II"], ["NPS Lite"], ["Corporate CG"], ["APY"], ["A Tier I"], ["A Tier II"], ["NPS TTS-II"]]


def get_data():
    driver.get('https://www.sbipensionfunds.com/historical-nav/')
    wt(5)
    driver.find_element(
        By.XPATH, '//*[@id="f_date_p1"]').send_keys("15-05-2009")
    sleep(1)
    date_today, month, year = get_date()
    driver.find_element(
        By.XPATH, '//*[@id="f_date_p2"]').send_keys(f"{date_today}-{month}-{year}")
    sleep(1)
    driver.find_element(
        By.XPATH, '/html/body/section/div/div/div/div/div/div/div/table/tbody/tr/td[5]/input').click()
    wt(3)
    sleep(5)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    data = []
    table = soup.find(
        'table', attrs={'class': 'table table-hover table-condensed table-bordered'})
    tbody = table.find('tbody')

    rows = tbody.find_all('tr')
    for r in rows:
        cols = r.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    data_frame = pd.DataFrame(data)
    data_frame.to_csv(r'./data.csv', index=False)
    print(pd.read_csv('data.csv'))


get_data()


driver.quit()
