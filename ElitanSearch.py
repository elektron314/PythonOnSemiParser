import selenium.webdriver as webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import random

my_email_login = "the.only@mail.ru"
my_login_pas = "14252154iI"
price = ''
prices = []
input_file = '3-gate.csv'
output_file = '3-gate-rus.csv'
url = "https://elitan.ru/"


def read_csv(filename):
    df = pd.read_csv(filename)
    return df


def get_prices(df):
    total_rows = len(df['Product Name'])
    for i in range(total_rows):
        search_item = df['Product Name'][i]
        price = get_results(search_item)
        prices.append(price)
    return prices

def wait_for_appear(atr1, atr2):
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((atr1, atr2)))

def wait_for_clickable(atr1, atr2):
    wait2 = WebDriverWait(browser, 10)
    wait2.until(EC.element_to_be_clickable((atr1, atr2)))

def get_results(search_term):
    search_box = browser.find_element_by_id("find")
    search_box.clear()
    search_box.send_keys(search_term)
    search_box.submit()
    wait_for_appear(By.CLASS_NAME, 'link_block_grad')
    browser.find_element_by_xpath("//div[@style='display: table-cell; text-align: right;']/a").click()
    try:
        browser.find_element_by_xpath("//a[@class='personal_aut']").click()
        emailbox = browser.find_element_by_xpath("//input[@id='email']")
        emailbox.send_keys(my_email_login)
        passbox = browser.find_element_by_xpath("//input[@id='password']")
        passbox.send_keys(my_login_pas)
        time.sleep(4)
        browser.find_element_by_xpath("//input[@id='btn2']").click()
    except:
        # print('already logged in')
        pass
    # wait_for_appear(By.ID, 'sortprice')
    # wait_for_clickable(By.ID, 'sortprice')
    # why should i wait? what is wrong with functions upper?
    time.sleep(1)
    browser.find_element_by_xpath("//input[@id='sortprice']").click()
    my_target = browser.find_element_by_xpath("//div[@style='display: table-cell; text-align: right;']/a")
    try:
        my_target.click()
    except:
        pass

    try:
        price = my_target.find_element_by_xpath("//tr[starts-with(@class, 'good_price')]").text
        if price == '':
            price = my_target.find_element_by_xpath("//span[@class='pricetd_span']").text
    except:
        price = my_target.find_element_by_xpath("//span[@class='pricetd_span']").text
        print('no good price')
    print(price[0:2])
    # time.sleep(2)
    return price[0:2]


# data = read_csv('buffers.csv')
browser = webdriver.Chrome()
browser.get(url)
# browser.implicitly_wait(10)

read_data = pd.read_csv('3-gate.csv')
# get_prices(read_data)
read_data['Elitan Prices'] = get_prices(read_data)
read_data.to_csv('3-gate-rus.csv', index=False)

# data["Elitan_price"] = ""
# data.to_csv("buffers.csv", index=False)
browser.quit()