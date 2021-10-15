from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from selectorlib import Extractor
import requests
from datetime import datetime, date, timedelta
import pandas as pd
from math import floor
import concurrent.futures
import streamlit as st

def divide_dates(start, works):
    end = datetime.strptime(datetime.strftime(datetime.now(),"%d-%m-%Y"), "%d-%m-%Y")
    start = datetime.strptime(start, "%d-%m-%Y")
    delta = end-start
    day_diff = floor(int(delta.days/works))
    print(day_diff)
    all_ = []
    for i in range(0, works-1):
        a = start + timedelta(days=day_diff)
        t = (datetime.strftime(start, "%d-%m-%Y"), datetime.strftime(a, "%d-%m-%Y"))
        all_.append(t)
        start = a + timedelta(days=1)
    all_.append((datetime.strftime(start, "%d-%m-%Y"), datetime.strftime(end, "%d-%m-%Y")))
    return all_

def scrape(times, e):
    url = "https://www.sbipensionfunds.com/historical-nav/"
    op = webdriver.ChromeOptions()
    
    op.add_argument('--headless')
    op.add_argument('--log-level=3')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)
    driver.get(url)
    from_date = driver.find_element_by_name("fromdate")
    from_date.clear()
    from_date.send_keys(times[0])
    to_date = driver.find_element_by_name("todate")
    to_date.clear()
    to_date.send_keys(times[1])
    #time.sleep(1)
    
    button = driver.find_element_by_xpath("""//input[contains(concat(" ",normalize-space(@class)," ")," btn ")]""")
    driver.execute_script("arguments[0].click();", button)
    #sub = driver.find_element_by_name("mysubmit").click()
    r = driver.page_source
    data = e.extract(r)
    return data['table']

def main():
    works = 4
    e = Extractor.from_yaml_file('sbi.yml')
    count = 0
    all_times = divide_dates("15-05-2009", works)
    print(all_times)
    start = time.time()
    frames = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=works) as executor:
        results = {executor.submit(scrape, times, e): times for times in all_times}
        for result in concurrent.futures.as_completed(results):
            data = result.result()
            frames.append(pd.DataFrame(data))
    end=time.time()
    print(f"Runtime: {end-start}")
    thing = pd.concat(frames)      
    thing['Date'] =  pd.to_datetime(thing['Date'], format='%Y-%m-%d')
    thing.sort_values(by='Date', ascending=True, ignore_index=True, inplace=True)
    st.write(thing)
    thing.to_csv('data.csv', index=False)
    
main()


