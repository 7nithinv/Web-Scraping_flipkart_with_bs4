import requests
from bs4 import BeautifulSoup
import pandas as pd
from dateutil import parser
import re


baseurl = "https://www.flipkart.com"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}

productlinks = []

for x in range(1,7):
    r = requests.get(f"https://www.flipkart.com/bags-wallets-belts/luggage-travel/suitcases/it-luggage~brand/pr?sid=reh%2Cplk%2Ctvv&marketplace=FLIPKART&otracker=product_breadCrumbs_It+Luggage+Suitcases&page={x}")
    soup = BeautifulSoup(r.content, 'html.parser')
    productlist = soup.find_all('div', class_='_1xHGtK _373qXS')

    for item in productlist:
        for link in item.find_all('a', href=True, limit = 1):
            productlinks.append(baseurl + link['href'])
        
names = []
sps =  []
mrps = []
sellers = []

for link in productlinks:
    r = requests.get(link, headers = headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    
    name = soup.find('span', class_ = 'B_NuCI')
    sp = soup.find('div', class_ = '_30jeq3 _16Jk6d')
    mrp = soup.find('div', class_='_3I9_wc _2p6lqe')
    seller = soup.find('div', class_='_1RLviY')
    
    names.append(name)
    sps.append(sp)
    mrps.append(mrp)
    sellers.append(seller)

    fsn = []
    for l in productlinks:
        li = re.search("pid=\w+", l)
        fsn.append(li)


    info = {
        'name': names,
        'sp': sps,
        'mrp': mrps,
        'seller': sellers,
        'fsn' : fsn,
    }

df = pd.DataFrame(info)
df.to_csv("output2.csv")
