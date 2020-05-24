# date : 2020/05/24
# Dart Open API를 이용하여 대주주 지분 변경 실시간으로 검색하기
#
# pip install requests
#
# 보다 자세한 내용을 아래 tstory 참고
# https://money-expert.tistory.com/6
#

import requests
import json


crtfc_key = '본인의 API key'

def request_get(url) :
    response = ""
    cnt2 = 0
    while str(response) != '<Response [200]>' and cnt2 < 10:
#            print("requests request_get", url)
        cnt2 += 1
        try :
            response = requests.get(url)
            if str(response) != '<Response [200]>':
                print('sleep ', url)
                sleep(15)
        except Exception as e:
            print(e)
            time.sleep(20)
            continue
    return response.json()


# 특정 기업 지분 공시 내역 검색 (공시정보)
# https://opendart.fss.or.kr/api/list.json
# corp_cls : 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) 없으면 전체조회
# pblntf_ty : A : 정기공시 B : 주요사항보고 C : 발행공시 D : 지분공시 E : 기타공시
#             F : 외부감사관련 G : 펀드공시 H : 자산유동화 I : 거래소공시 j : 공정위공시
# https://opendart.fss.or.kr/api/list.json?crtfc_key=xxx&pblntf_ty=D&&bgn_de=20200518&end_de=20200522&corp_cls=Y&page_no=1&page_count=10
def find_major_holder_change_all(pblntf_ty, begin ,end) :
    home = 'https://opendart.fss.or.kr/api/list.json'
    url = home + '?crtfc_key=' + crtfc_key + '&pblntf_ty=D' + '&bgn_de=' + \
          begin+ '&end_de=' + end + '&corp_cls=Y&page_no=1&page_count=10'
    print(url)
    res = request_get(url)

    for info in res['list'] :
        print(info)
    print('')



# corp_cls : 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) 없으면 전체조회
# pblntf_ty : A : 정기공시 B : 주요사항보고 C : 발행공시 D : 지분공시 E : 기타공시
#             F : 외부감사관련 G : 펀드공시 H : 자산유동화 I : 거래소공시 j : 공정위공시
res = find_major_holder_change_all('D', '20200518', '20200522')  # type, begin, end
print('')
