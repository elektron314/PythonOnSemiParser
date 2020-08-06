from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

driver = webdriver.Chrome()
products = []
prices = []
descriptions = []
output_file = '3-gate.csv'
filter_word = 'Buffer'


def parse():
    for a in soup.findAll(class_='px-row', id=re.compile('r_'), attrs={"data-description-search": re.compile(filter_word)}):
        priceTag = a.find(class_="px-cell", string=re.compile("$"))
        price = (re.findall(r'\$[\d.]*', priceTag.get_text()))
        if not price:
            price = ['0']
        prices.append(price[0])
        for d in a.findAll("div", class_="px-cell px-description-cell"):
            description = d.find("a").string.strip()
            descriptions.append(description)
        i = 0
        for b in a.findAll("div", class_="px-cell"):
            for c in b.findAll("a", class_="productInfo"):
                product = c['data-id']
                products.append(product)


# driver.get("https://www.onsemi.com/products/standard-logic/metal-gate")
# driver.get("https://www.onsemi.com/products/standard-logic/buffers")
driver.get("https://www.onsemi.com/products/standard-logic/3-gate")
# driver.get("https://www.onsemi.com/products/standard-logic/buffers?_ga=2.202468626.2085979349.1593163729-135515443.1593163729")

content = driver.page_source
soup = BeautifulSoup(content, "html.parser")

parse()

time.sleep(1)
while soup.find(class_="pageSelector").find("a", string=re.compile("next")):
    driver.execute_script("processTable('nextPage','');")
    time.sleep(3)
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    parse()

df = pd.DataFrame({'Product Name': products, 'Prices': prices, 'Description': descriptions})
df.to_csv(output_file, index=False, encoding='utf-8')

driver.quit()
