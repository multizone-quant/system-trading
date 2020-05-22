# date : 2020/05/23
# 일 기준 오른 종목을 json 파일로 저장
# naver 아래 사이트의 정보를 크롤링하여 저장
# https://finance.naver.com/sise/sise_rise.nhn
# 단 아래 항목을 선택하여야 정상 동작함
#   거래량, 시가, 고가, 저가, 시가총액, per, poe
# 필요한 경우에 위 항목을 변경할 수 있음. 코드 상에서 title에서 변경한 항목 반영 필요함
#
# 실행결과
# 코스닥 상승 종목 : 날짜_kosdaq_up_list.txt
# 코스피 상승 종목 : 날짜_kospi_up_list.txt
#
# pip install urllib.request
# pip install BeautifulSoup
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


def uplist() :
    # 코스피
    url1 = 'https://finance.naver.com/sise/sise_rise.nhn'
    # 코스닥
    url2 = 'https://finance.naver.com/sise/sise_rise.nhn?sosok=1'

    up_list = {'kospi':url1, 'kosdaq':url2}

    title_list = ['no', 'name', 'close', 'diff', 'per', 'qty', 'open', 'high', 'low', 'sichong', 'per', 'pbr']
    for name, url in up_list.items() :
        with urllib.request.urlopen(url) as fs :
            soup = BeautifulSoup(fs.read().decode(fs.headers.get_content_charset()), 'html.parser')

        cnt = 1
        prices =[]
        # 각 데이터는 tr로 시작
        for tr in soup.find_all('tr') :
            # 각 항목은 td로 시작
            td_list = tr.find_all('td')
            try : 
                # 빈줄, 라인 등 데이터가 아닌 경우도 있다.
                # 다행히 n 값에 1부터 증가하는 값이 기록되어 있으므로, 이 값이 맞으면 정상적인 데이터로 판단
                if int(td_list[0].text.strip()) == cnt :
                    info = {}
                    # 총 12 항목에 대하여 set 구조체(info)에 옮긴다.
                    for i in range(0,len(td_list)) :
                        data = td_list[i].text.strip()
                        info[title_list[i]] = data
                    # 종목 하나 정보 완성 list에 추가
                    prices.append(info)
                    cnt+=1
            except :
                continue
        # 저장
        fname = TODAY+'_'+name+'_up_list.txt'
        save_to_file_json(fname, prices)
        print('done ', name)

# 상승종목 저장 
print('상승종목 저장 시작')
uplist()
print('상승종목 저장 끝')


# 잘 저장되어 있는지 test
if 0 :
    fname = TODAY+'_kosdaq'+'_up_list.txt'
    prices = load_json_from_file(fname)
    for p in prices :
        print(p)
