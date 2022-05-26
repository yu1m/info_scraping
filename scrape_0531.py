from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
from time import sleep
import urllib.parse
import chromedriver_binary
import pandas as pd

def chrome_setting():
    url_main='https://www.jab.or.jp/system/iso/search/'
    driver=webdriver.Chrome()
    driver.get(url_main)
    driver.implicitly_wait(10)
    sleep(1)
    driver.find_element(By.ID,'standard_1').click()
    sleep(5)
    return driver

def getting_url(driver):
    html=driver.page_source
    soup=BeautifulSoup(html,'html.parser')
    urls=soup.find('table',id='selectResultDisplay').find_all('tr')[1:]
    sleep(0.3)
    return urls

def getting_infos(url,url_main):
    url_d=urllib.parse.urljoin(url_main,url.find('a').get('href'))
    r=requests.get(url_d)
    sleep(0.4)
    soup_d=BeautifulSoup(r.text,'html.parser')
    infos=soup_d.find('div',class_='contentInner').find_all('td')
    return infos,url_d

def input_d(url_d,infos,dic):
    d={'取得元URL':url_d,
    '組織名':infos[0].text,
    '事業所名':infos[1].text,
    '認証機関名':infos[2].text.replace('\n',' ').replace('\r',' '),
    '認証機関登録番号':infos[3].text,
    '初回登録日':infos[4].text,
    '有効期限':infos[5].text,
    '認証規格':infos[6].text,
    '産業分類':infos[7].text,
    '所在地':infos[8].text,
    '登録範囲':infos[9].text.replace('\n',' ').replace('\r',' '),
        }
    dic.append(d)



def main(Filename):
    #Chromeを開きISO 9001をクリック
    driver=chrome_setting()
    
    dic=[]

    while True:
        print('-----------開始-------------')
        #閲覧しているページにある各詳細ページへの相対URLを取得
        urls=getting_url(driver)
        for url in urls:
            #取得する情報をリストに格納
            infos=getting_infos(url,'https://www.jab.or.jp/system/iso/search/')[0]
            #詳細ページの絶対urlを取得
            url_d=getting_infos(url,'https://www.jab.or.jp/system/iso/search/')[1]
            input_d(url_d,infos,dic)
        try:
            driver.find_element(By.CLASS_NAME,'next').click()
            print('----次ページに移動----')
            sleep(1)
        except:
            ('-----終了------')
            break
    driver.quit
    
    #Excelファイルへ出力
    df=pd.DataFrame(dic)
    df.to_excel(Filename,index=None,encoding='utf_8_sig')
        

if __name__=='__main__':
    filename=input('ファイル名を入力>')
    main(filename)
    


