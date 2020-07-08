# -*- coding: utf-8 -*-
# date : 2020/07/08
# 현재 상장된 모든 종목의 일봉 정보를 json 파일로 저장
# naver 아래 사이트의 정보를 크롤링하여 저장
# https://finance.naver.com/sise/sise_market_sum.nhn
#
# 항목변경 기능 추가함 거래량,시가,고가,저가,시가총액으로 설정함
# 
# 종목이 많아서 page로 구성되어 있음. 마지막에 page 번호를 증가시키면서 계속 검색함
# https://finance.naver.com/sise/sise_market_sum.nhn?&page=1
# https://finance.naver.com/sise/sise_market_sum.nhn?&page=2
#
# 실행결과
# 코스닥 상승 종목 : 날짜_kosdaq_day_bong_list.txt
# 코스피 상승 종목 : 날짜_kospi_day_bong_list.txt
#
# 관련 설명 : https://money-expert.tistory.com/16

import time
import urllib.request
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import time


def load_json_from_file(file_name) :
    try :
        with open(file_name,'r',encoding="cp949") as make_file: 
           data=json.load(make_file) 
        make_file.close()
    except  Exception as e : # 또는 except : 
        data = {}
        print(e, file_name)
    return data

def save_to_file_json(file_name, data) :
    with open(file_name,'w',encoding="cp949") as make_file: 
       json.dump(data, make_file, ensure_ascii=False, indent="\t") 
    make_file.close()

TODAY = time.strftime("%Y%m%d")

SETUP_CHANGED = 0
# 네이버 상승종목 페이지 중 시가/고가/저가 값을 가지고 올 수 있도록 설정
# 최대 6항목 설정 가능.
def open_naver_stock_page(driver, url) :
    global SETUP_CHANGED
    if SETUP_CHANGED :
        return
    SETUP_CHANGED = 1
    driver.get(url)

    driver.find_element_by_xpath(".//*[contains(text(), '고가')]").click()
    driver.find_element_by_id("option7").click()  # 시가
    driver.find_element_by_xpath(".//*[contains(text(), '저가')]").click()
    driver.find_element_by_xpath(".//*[contains(text(), '외국인비율')]").click()  # 삭제
    driver.find_element_by_xpath(".//*[contains(text(), '상장주식수')]").click()  # 삭제
    driver.find_element_by_xpath(".//*[contains(text(), 'ROE')]").click()  # 삭제

    driver.find_element_by_css_selector('[alt="적용하기"]').click()

    time.sleep(3)

# 특정 url에 있는 정보를 뽑아냄 
def get_stock_list(url, cnt) :
    with urllib.request.urlopen(url) as fs :
        soup = BeautifulSoup(fs.read().decode(fs.headers.get_content_charset()), 'html.parser')
    get_stock_list_soup(soup, cnt)

# 특정 url에 있는 정보를 뽑아냄 (soup을 입력으로)
def get_stock_list_soup(soup, cnt) :
    title_list = []

    prices =[]
    got_title = 0

    # 각 데이터는 tr로 시작
    for tr in soup.find_all('tr') :
        # title은 th로 시작
        if got_title == 0 :
            th_list = tr.find_all('th')
            if th_list != [] :
                if th_list[0].text.strip() == 'N' :
                    info = {}
                    for i in range(0,len(th_list)) :
                        data = th_list[i].text.strip()
                        title_list.append(data)
                        print(i, data )
                    print('')
                got_title = 1
        # 각 항목은 td로 시작
        td_list = tr.find_all('td')
        try : 
            no = td_list[0].text.strip()
            print(no)
            if no[0] == '\n' :
                no = no.replace('\n','')
            # 빈줄, 라인 등 데이터가 아닌 경우도 있다.
            # 다행히 n 값에 1부터 증가하는 값이 기록되어 있으므로, 이 값이 맞으면 정상적인 데이터로 판단
            if int(no) == cnt :
                info = {}
                for i in range(0,len(td_list)) :
                    data = td_list[i].text.strip()
                    info[title_list[i]] = data
                prices.append(info)
                cnt+=1
        except :
            continue
    return prices, cnt

def day_bong_list(name) :
    # 코스피
    url1 = 'https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0'
    # 코스닥
    url2 = 'https://finance.naver.com/sise/sise_market_sum.nhn?sosok=1'
    
    sise_list = {'kospi':url1, 'kosdaq':url2}

    # 총 페이지수, 상장 종목이 늘어나면 증가할 수 있음
    sise_page_list = {'kospi':32, 'kosdaq':29}

    # 네이버 시총 페이지 설정 변경
    print('open naver ', sise_list[name])
    open_naver_stock_page(driver, sise_list[name])

    cnt = 1
    prices = []
    for i in range(1, sise_page_list[name]+1) :
        print('page ', i)
        # 해당 페이지 클릭
        driver.find_element_by_link_text(str(i)).click()
        time.sleep(3)
        
        # 특정 page를 클릭한 후 로딩될 동안 잠시 기다린다.
        soup = BeautifulSoup(driver.page_source, 'html.parser', from_encoding='utf-8')
        ret, cnt = get_stock_list_soup(soup, cnt) 
        prices += ret

        # 10 page 단위로 보임, 11, 21, 31페이지를 위해서는 '다음' 버튼 클릭
        if (i % 10) == 0 : # 다음 page 클릭
            print('click next')
            driver.find_element_by_link_text('다음').click()
            time.sleep(3)
        input()
    # 저장
    fname = TODAY+'_'+name+'_day_bong_list.txt'
    save_to_file_json(fname, prices)
    print('done ', name)


driver = webdriver.Chrome("C:\\my\\chromedriver.exe")

print('kosdaq 전 종목 오늘 봉 저장 시작')
day_bong_list('kosdaq')

print('kospi 전 종목 오늘 봉 저장 시작')
day_bong_list('kospi')



# 잘 저장되어 있는지 test
if 0 :
    fname = TODAY+'_kosdaq'+'_day_bong_list.txt'
    prices = load_json_from_file(fname)
    for p in prices :
        print(p)
