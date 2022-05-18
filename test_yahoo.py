import requests
from bs4 import BeautifulSoup
from time import sleep

url='https://store.shopping.yahoo.co.jp/popai-y/'

r=requests.get(url)
sleep(1)

soup=BeautifulSoup(r.text,'html.parser')

s=soup.find('p',class_='elMainItem isName')

shop_name=s.text
shop_url=s.find('a')['href']

print(shop_name)
print(shop_url)



    
