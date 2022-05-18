from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import chromedriver_binary
from time import sleep
import time
import pandas as pd
import sys

def main(Filename):
    options=Options()
    options.add_argument('--incognito')#Chromeをシークレットモードで開く
    options.add_experimental_option('excludeSwitches',['enable-logging'])

    #Chromeでクックドアを開く
    url_main='https://www.cookdoor.jp/'
    driver=webdriver.Chrome(options=options)
    driver.get(url_main)

    #要素が見つかるまでの待機時間
    driver.implicitly_wait(10)

    sleep(1)


    html_main=driver.page_source
    soup_main=BeautifulSoup(html_main,'html.parser')

    soup_japan=soup_main.find('div',class_='search_area_change_box')
    prefs=soup_japan.find_all('a')

    sleep(1)

    food_list=[]
    Flag_main=True
    given_prefs=[]
    page_numbers=[]



    #都道府県の入力
    Flag_sub=True
    while Flag_sub==True:
        Flag=True
        while Flag==True:
            given_pref=input('都道府県を入力してください。(例:兵庫)>')
            confirm_number=1#北海道が選ばれた時のために値を代入しておく
            for i,pref in enumerate(prefs):
                if pref.text == given_pref:
                    break
                else:
                    confirm_number=i
            if confirm_number==46:
                print('都道府県名を正しく入力してください')
            else:
                Flag=False
        
                
        #取得したいページ数を入力
        while True:
            try:
                page_number=int(input('取得したいページ数を入力してください(30店舗/1ページ)>'))
                break
            except ValueError as e:
                print(e)
                print('数字を正しく入力してください')
        
        given_prefs.append(given_pref)
        page_numbers.append(page_number)
        
        while True:
            while True:
                confirm=input('別の都道府県を検索しますか？(検索するならy,しないならnを入力してください)>')
                if (confirm=='y')or(confirm=='n'):
                    break
                else:
                    print('yかnを入力してください')
            if confirm=='y':
                break
            else:
                Flag_sub=False
                break
    

    for t,given_pref_ in enumerate(given_prefs):
        #都道府県のページに移動
        element_japan=driver.find_element(By.XPATH,'//*[@id="search_area_japan"]')
        element_button=element_japan.find_element(By.PARTIAL_LINK_TEXT,given_pref_)
        element_button.click()

        sleep(1)



        #県全体の検索結果が出てくるページに移動
        element_pref=driver.find_element(By.CLASS_NAME,'area_list01_head')
        element_button2=element_pref.find_element(By.TAG_NAME,'a')
        element_button2.click()

        sleep(1)

        #取得したいページ数がサイトのページ数を超えている場合の処理
        page_site_=driver.find_element(By.CLASS_NAME,'pager01_area').find_elements(By.CLASS_NAME,'pager_num')
        page_site_number=int(page_site_[-1].text)
        page_number_=page_numbers[t]
        if page_number_>page_site_number:
            page_number_=page_site_number
            
        #取得したいページ分ループ
        for x in range(page_number_):
            ranking_frame=driver.find_element(By.CLASS_NAME,'ranking_frame')
            restaurant_names=ranking_frame.find_elements(By.CLASS_NAME,'restaurant_name')
            shop_number=len(restaurant_names)
            #各店舗の情報を取得
            for i in range(shop_number):
                    
                ranking_frame=driver.find_element(By.CLASS_NAME,'ranking_frame')
                restaurant_names=ranking_frame.find_elements(By.CLASS_NAME,'restaurant_name')
                restaurant_name=restaurant_names[i].find_element(By.TAG_NAME,'a')
                
                try:
                    restaurant_name.click()
                
                    sleep(0.5)
                    html_detail_shop=driver.page_source
                    soup_detail=BeautifulSoup(html_detail_shop,'html.parser')
                    detail_infos_1=soup_detail.find('table',class_='table01 mb15').find_all('td')
                    detail_infos_2=soup_detail.find('table',class_='table01 mb10').find_all('td')
                    
                    shop_name=detail_infos_1[0].text.replace('\n','').replace('\u3000','')
                    detail_infos_1[2].find('span').decompose()
                    shop_adress=detail_infos_1[2].get_text(strip=True).replace('\n','').replace('\u3000','')
                    shop_access=detail_infos_1[3].find('p',class_='basic_info_traffic').text.replace('\n','').replace('\u3000','')
                    shop_tell=detail_infos_1[4].text.replace('\n','').replace('\u3000','')
                    shop_time=detail_infos_2[0].text.replace('\n','').replace('\u3000','')
                    shop_nonrun=detail_infos_2[1].text.replace('\n','').replace('\u3000','')
                    shop_cost=detail_infos_2[7].text.replace('\n','').replace('\u3000','')
                    
                    d={'店名':shop_name,
                    '住所':shop_adress,
                    'アクセス':shop_access,
                    '電話番号':shop_tell,
                    '営業時間':shop_time,
                    '定休日':shop_nonrun,
                    '平均予算':shop_cost}
                    
                    food_list.append(d)
                except:
                    pass
                finally:
                    driver.back()
                    sleep(0.7)
            
            #次のページに移動
            next_page=driver.find_element(By.CLASS_NAME,'pager01_area').find_element(By.CLASS_NAME,'pager_next')
            next_page.click()

       
        home_back=driver.find_element(By.ID,'siteroute').find_element(By.TAG_NAME,'a')
        home_back.click()          
                
    df=pd.DataFrame(food_list)
    df.to_csv(Filename,encoding='utf_8_sig',index=None)
    driver.quit()

if __name__=='__main__':
    Filename=input('csvファイル名を入力してください(.csvを付け忘れないでください)>')
    main(Filename)
    
            




        
        






















