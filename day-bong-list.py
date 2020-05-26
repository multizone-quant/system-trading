# -*- coding: utf-8 -*-
# date : 2020/05/23
# 현재 상장된 모든 종목의 일봉 정보를 json 파일로 저장
# naver 아래 사이트의 정보를 크롤링하여 저장
# https://finance.naver.com/sise/sise_market_sum.nhn
#
# 항목변경이 안됨 초기 상태 그래도 저장
# 
# 종목이 많아서 page로 구성되어 있음. 마지막에 page 번호를 증가시키면서 계속 검색함
# https://finance.naver.com/sise/sise_market_sum.nhn?&page=1
# https://finance.naver.com/sise/sise_market_sum.nhn?&page=2
#
# 실행결과
# 코스닥 상승 종목 : 날짜_kosdaq_day_bong_list.txt
# 코스피 상승 종목 : 날짜_kospi_day_bong_list.txt
#

import time
import urllib.request
import json
from bs4 import BeautifulSoup


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

# 특정 url에 있는 정보를 뽑아냄 
def get_stock_list(url, cnt) :
    title_list = []
    with urllib.request.urlopen(url) as fs :
        soup = BeautifulSoup(fs.read().decode(fs.headers.get_content_charset()), 'html.parser')

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
            if no[0] == '\n' :
                no = no.replace('\n','')
            # 빈줄, 라인 등 데이터가 아닌 경우도 있다.
            # 다행히 n 값에 1부터 증가하는 값이 기록되어 있으므로, 이 값이 맞으면 정상적인 데이터로 판단
            if int(no) == cnt :
                info = {}
                for i in range(0,len(td_list)) :
                    data = td_list[i].text.strip()
                    info[title_list[i]] = data
                if info['name'] == '2' : # 아래에 있는 페이지 정보이므로 무시
                    continue
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
    close_price_list = {'kospi':url1, 'kosdaq':url2}

    # 총 페이지수, 상장 종목이 늘어나면 증가할 수 있음
    close_page_list = {'kospi':32, 'kosdaq':29}

    cnt = 1
    prices = []
    for i in range(0, close_page_list[name]) :
        print('page ', i+1)
        url = close_price_list[name] + '&page='+str(i+1)
        ret, cnt = get_stock_list(url, cnt) 
        prices += ret

    # 저장
    fname = TODAY+'_'+name+'_day_bong_list.txt'
    save_to_file_json(fname, prices)
    print('done ', name)

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
