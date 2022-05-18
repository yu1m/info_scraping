from cgitb import text
from re import T
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import chromedriver_binary
from time import sleep
import time
import requests
import sys
import pprint


def main(Filename):
    options=Options()
    options.add_experimental_option('excludeSwitches',['eneable-logging'])


    url_beauty='https://beauty.hotpepper.jp/'
    driver=webdriver.Chrome(options=options)
    driver.get(url_beauty)

    sleep(0.5)
    driver.implicitly_wait(20)#要素を取得するまで待機

    sln_list=[]
    prefs=[]

    while True:
        pref=input('地名を入力してください>')
        prefs.append(pref)
        while True:
            confirmer=input('別の地名を検索しますか？（検索するならy,したいならn)>')
            if (confirmer == 'y')or(confirmer=='n'):
                break
            else:
                print('yかnを入力してください')
        if confirmer=='y':
            pass
        else:
            break
            
            
        
    for x,pref_ in enumerate(prefs):
        start=time.perf_counter()
        #地域名を入力して検索
        search_box=driver.find_element(By.CLASS_NAME,'inputSalonName')
        search_box.clear()
        search_box.send_keys(pref_)
        driver.find_element(By.CLASS_NAME,'searchButton').click()

        sleep(0.5)

        #ページごとのurl取得
        url_main=driver.current_url

        max_number=(int(driver.find_element(By.CLASS_NAME,'numberOfResult').text))//20
        n=10
        if max_number<10:
            n=max_number

        for i in range(1,n+1):
            url=url_main+'&pn={}'.format(i)

            r_main=requests.get(url)
            sleep(0.5)
            soup_page=BeautifulSoup(r_main.text,'html.parser')
            #urlを集める
            shop_slninfos=soup_page.find_all('div',class_='slnInfo')
            #1ページ集める

            for shop_slninfo in shop_slninfos:
                shop_slninfo_url=shop_slninfo.find('a')['href']
                r=requests.get(shop_slninfo_url)

                sleep(0.5)

                #詳細な情報を取得
                soup_info=BeautifulSoup(r.text,'html.parser')
                infos_flame=soup_info.find('table',class_='slnDataTbl bdCell bgThNml fgThNml vaThT pCellV10H12 mT20')
                infos_detail=infos_flame.find_all('td')

                try:
                    shop_title=soup_info.find('p',class_='detailTitle').text
                    shop_adress=infos_detail[1].text
                    shop_access=infos_detail[2].text
                    shop_time=infos_detail[3].text
                    shop_nonrun=infos_detail[4].text
                    shop_homepage=infos_detail[6].find('a').text
                    shop_cost=infos_detail[7].text
                    
                    #電話番号取得
                    shop_tell_url=infos_detail[0].find('a')['href']
                    r_tell=requests.get(shop_tell_url)
                    sleep(0.3)
                    soup_tell=BeautifulSoup(r_tell.text,'html.parser')
                    shop_tell=soup_tell.find('table',class_='wFull bdCell pCell10 mT15').find('td').text
                    


                    d={'店名':shop_title.replace('\xa0','').replace('\u3000',''),
                    '住所':shop_adress.replace('\xa0','').replace('\u3000',''),
                    'アクセス':shop_access.replace('\xa0','').replace('\u3000',''),
                    '電話番号':shop_tell.replace('\xa0','').replace('\u3000',''),
                    '営業時間':shop_time.replace('\xa0','').replace('\u3000',''),
                    '定休日':shop_nonrun.replace('\xa0','').replace('\u3000',''),
                    'カット価格':shop_cost.replace('\xa0','').replace('\u3000',''),
                    'ホームページ':shop_homepage.replace('\xa0','').replace('\u3000','')}

                    sln_list.append(d)
                except:
                    pass
        
        print(time.perf_counter()-start)
        driver.get(url_beauty)
        


    df=pd.DataFrame(sln_list)
    df.to_csv(Filename,encoding='utf_8_sig',index=None)
    driver.quit()




if __name__=='__main__':
    Filename=input('csvファイル名を入力してください(.csvをつけ忘れないでください)>')
    main(Filename)


