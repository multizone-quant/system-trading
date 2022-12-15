from pykrx import stock
import pandas as pd
import glob
import os
import time

def is_exist(fname) :
    ret = glob.glob(fname)
    if len(ret) > 0 :
        return 1
    return 0


# kospi200 업종 028
def get_kospi200_data(start, end, kospi200_folder) :

    # kospi200 받기
    data = stock.get_index_ohlcv_by_date(start, end, "1028") # kospi200 028

    # 최초 저장이면 저장 후 return
    fname = kospi200_folder + '\\kospi200_'+start[:4]+'.csv'   # start[:4] : 연도만 뽑음 2022
    if is_exist(fname)  == 0:
        data.to_csv(fname, header=True, index=True, encoding='euc-kr') 
        print(data)
        return

    # 기존 데이터가 있으면 새로 검색한 데이터는 temp에 저장
    temp = kospi200_folder + '\\temp.csv'
    data.to_csv(temp, header=True, index=True, encoding='euc-kr') 

    # 기존 파일과 temp merge 후 기존 파일에 저장
    pre_data = pd.read_csv(fname, encoding='euc-kr')
    new_data = pd.read_csv(temp, encoding='euc-kr')    

    merged_data = pd.concat([pre_data,new_data], ignore_index=True)
    merged_data.to_csv(fname, header=True, index=False, encoding='euc-kr')

    print(merged_data)


# KRDRVFUK2I : 정규 선물
# KRDRVFUMKI : 미니 선물
# KRDRVOPK2I : 정규 option
# KRDRVOPWKI : weekly option
# KRDRVOPMKI : mini option

# 정규옵션과 weekly 옵션을 동시에 받는다.
def get_op_data(yyyy, mm, start, end, op_folder, wop_folder) :
    tp1    = 'KRDRVOPK2I' # 옵션
    tp2    = 'KRDRVOPWKI' # : weekly option

    for each in range(start, end+1) :
    #    if each in skips :
    #        continue
        dt = yyyy + mm + '%02d'%each
        data = stock.get_future_ohlcv(dt, tp1) # option
        if data.empty == False :
            fname = op_folder + '\\op_' + dt + '.csv'
            data.to_csv(fname, header=True, index=True, encoding='euc-kr')
            print(fname)

        data = stock.get_future_ohlcv(dt, tp2) # option
        if data.empty == False :
            fname = wop_folder + '\\wop_' + dt + '.csv'
            data.to_csv(fname, header=True, index=True, encoding='euc-kr')
            print(fname)

# 
folder = '.\\data'
if is_exist(folder)  == 0:
    os.mkdir(folder)

if 1: # for kospi200
    st_yyyymmdd  = '20221201'  # 시작 년월일
    end_yyyymmdd = '20221202'  # 끝 년월일
    get_kospi200_data(st_yyyymmdd, end_yyyymmdd, folder)

# for option
if 1:
    yyyy  = '2022'  # year
    start = 5       # start day
    end   = 9     # end day

    for mm in range(12, 13) :  # 원하는 달 12, 13은 12월만 저장한다는 의미. 최대 3개월이 넘으면 krx에서 오류 뜨기도 함
        s_mm    = '%02d'%mm  # 1-9월 -> '01' - '09'
        get_op_data(yyyy, s_mm, start, end, folder, folder)
        time.sleep(10)
