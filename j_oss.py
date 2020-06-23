# -*- coding: utf-8 -*-
import time
import datetime
import json
import csv
import glob

TODAY = time.strftime("%Y%m%d")
TODAY_TIME = time.strftime("%H%M%S")
TODAY_S = time.strftime("%Y-%m-%d")

import sys, time, msvcrt
#
# 일정 시간이 지나면 자동으로 default 값이 입력으로 들어온 것으로 간주하고 return됨
# get default input after limited secs.
#
def readInput(caption, default, timeout = 5):
    if caption != '' :
        print (caption)
    start_time = time.time()
    input = ''
    while True:
        if msvcrt.kbhit():
            byte_arr = msvcrt.getche()
            if ord(byte_arr) == 13: # enter_key
                break
            elif ord(byte_arr) >= 32: #space_char
                input += "".join(map(chr,byte_arr))
        if len(input) == 0 or (time.time() - start_time) > timeout:
#           print("timing out, using default value.")
            break

#    print('')  # needed to move to next line
    if len(input) > 0:
        return input
    else:
        return default

def get_time_str(cont='T') :
    date=datetime.datetime.now()
    form = '%Y/%m/%d'+cont+'%H:%M:%S'
    return date.strftime(form)


# 거래일 기준 어제 일자를 알려준다. 월요일에 이 함수를 부르면 금요일 일자가 돌아온다.
# todo : 증권시장이 닫는 날은 그 전날.
def get_yesterday() :
    t = time.time()

    lt = time.localtime(t)
    diff = 60*60*24 # 하루 전
    if lt.tm_wday == 0 : # 월요일
        diff *= 3
    elif lt.tm_wday == 6 : # 일요일
        diff *= 2
    yst = time.localtime(t-diff)

    return str(yst.tm_year)+str('%02d'%yst.tm_mon)+str('%02d'%yst.tm_mday)

def read_csv(fname) :
    data = []
    with open(fname, 'r', encoding='UTF8') as FILE :
        csv_reader = csv.reader(FILE, delimiter=',', quotechar='"')
        for row in csv_reader :
            data.append(row)
    return data

#    with open(fname, 'r', encoding='cp949') as FILE :
def read_data_from_file(fname) :
    data = []
    try : 
        with open(fname, 'r', encoding='cp949') as FILE :
            while True :
                line = FILE.readline()
                if not line :
                    break
                data.append(line.replace('\n',''))
        FILE.close()
    except  Exception as e : # 또는 except : 
        pass
    return data

#def read_data_from_file(fname) :
def save_to_file_csv(file_name, data) :
    with open(file_name,'w',encoding="cp949") as make_file: 
        # title 저장
        vals = data[0].keys()
        ss = ''
        for val in vals:
            val = val.replace(',','')
            ss += (val + ',')
        ss += '\n'
        make_file.write(ss)

        for dt in data:
            vals = dt.values()
            ss = ''
            for val in vals:
                sval = str(val) 
                sval = sval.replace(',','')
                ss += (sval + ',')
            ss += '\n'
            make_file.write(ss)
    make_file.close()

def save_to_file_json(file_name, data) :
    with open(file_name,'w',encoding="cp949") as make_file: 
       json.dump(data, make_file, ensure_ascii=False, indent="\t") 
    make_file.close()

def load_json_from_file(file_name, err_msg=1) :
    try :
        with open(file_name,'r',encoding="cp949") as make_file: 
           data=json.load(make_file) 
        make_file.close()
    except  Exception as e : # 또는 except : 
        data = {}
        if err_msg :
            print(e, file_name)
    return data
def get_info_with_code(each, code) :
    sv = each
    sv['code'] = code
    return sv

def merge_single_day_bong_file(ddir) :
    # 대상 stock 정보
    tdate = '20200623'
    fname = '..\\data\\'+tdate+'_KOSPI_day_bong_list.txt'    

    targets = load_json_from_file(fname) 
    if targets == {} :
        return
    
    # read day price
    info = {}
    cnt2 = 0
    for t in targets :
        if t['code'] == '' : # code가 blank임  오류
            continue
        fname = ddir + t['code']  + '_20200619_day_bong.txt' 
        history = load_json_from_file(fname) 
        if history == {} :
            continue

        if cnt2 % 100 == 0 :
            print('processing ', cnt2, ' / ', len(targets))
        cnt2 += 1
        cnt = 0
        info[t['code']] = {}
        for each in history :
            # 입력 데이터에 code가 없으므로, code를 추가함
            sv = get_info_with_code(each, t['code'])
            info[t['code']][each['date']] = sv
            cnt += 1

    # write whole date for each day
    for i in range(20200619, 20200620) :
        day_hist = []
        for t in targets :
            if t['code'] == '' : # code가 blank임  오류
                continue
            if str(i) in info[t['code']] :
                day_hist.append(info[t['code']][str(i)])
        if len(day_hist) > 0 :
            fname = '..\\db1\\'+str(i)+'_KOSPI_day_history_list.txt'
            save_to_file_json(fname, day_hist)
#            fname = '..\\db1\\'+str(i)+'_KOSPI_day_history_list.csv'
#            save_to_file_csv(fname, day_hist)


# path 밑에 있는 모든 파일 목록
def get_file_list_in_dir(path):
    files = glob.glob(path+"*")
    return files
 
if __name__ == "__main__":
    print("my_utils.oss")
    if 1: # code별 day 봉 데이터를 일별로 모으기
        merge_single_day_bong_file('..\\db\\')
    
    ret = get_yesterday()
    print (ret)
    
    print('')
