# https://tkdocs.com/shipman/
# https://cosmosproject.tistory.com/m/610
# https://pythonguides.com/python-tkinter-treeview/

# https://github.com/multizone-quant/system-trading/blob/master/tkinter_sample.py

# 색상 선택
# color https://www.google.com/search?si=AC1wQDAoyjQYg3jwXlqSN_ppczo9u1jtdbgfRuCrHQSJJwEt2W4iv0bsHN1F5PH1083ADz-LNQYSCuyghCVkrzYn6ywkaIBPSg%3D%3D&hl=ko-KR&kgs=c09b70874624f115&shndl=21&source=sh/x/fbx/1&entrypoint=sh/x/fbx&fbxst=CgkKByMzMmE4NTI
# gray https://www.schemecolor.com/shiny-gray-color-palette.php 


# tksheet
#https://github.com/ragardner/tksheet/wiki

# pip install tk
# pip install tksheet

# https://github.com/multizone-quant/system-trading/blob/master/tk_sheet_ex/tkinter_sample-github.py

import tkinter as tk
import tkinter.ttk as ttk
import tksheet
import threading
import time

# colors
#f7e4e4 연빨강
#eef5ed 연녹색
#a1b4f7 연파랑

#------------------------------------------
#  sheet related

# sheet 생성 후 property 변경시 사용할 함수들
def refresh(sheet) :
    sheet.refresh( redraw_header = False, redraw_row_index = False)

def sheet_column_width(sheet, col, width) :
    sheet.column_width(col, width)

# align : left = 'w', right = 'e', center = 'center'
def sheet_column_align(sheet, cols, align) :
    sheet.align_columns(columns = cols, align = align)


def sheet_row_column_color(sheet, row, col, foreground='black', background='') :
    if background == '' :
        sheet.highlight_cells(row = row, column = col, fg = foreground)
    else :
        sheet.highlight_cells(row = row, column = col, fg = foreground, bg=background)

def sheet_column_color(sheet, col, max_row, foreground='black', background='') :
    for i in range(max_row) :
        if background == '' :
            sheet.highlight_cells(row = i, column = col, fg = foreground)
        else :
            sheet.highlight_cells(row = i, column = col, fg = foreground, bg=background)
    
# sheet 생성 
def create_sheet(window, x, y, heads, row, col, col_width, width, height) :
    frame = tk.Frame(relief='solid')
    frame.grid_columnconfigure(0, weight = 1)
    frame.grid_rowconfigure(0, weight = 1)

    sheet = tksheet.Sheet(frame, headers=heads, 
        row_index = None,
        show_row_index = False,
        show_top_left = False,
        column_width = col_width,
        data = [["" for c in range(col)] for r in range(row)],
        align = "e",
        header_align = "c",
        show_x_scrollbar = False,
        show_y_scrollbar = False,
        width = width, height = height
    )
    frame.place(x=x, y=y)
    if 0:
        # change width of specific col
        sheet.config(background='#EBECF0')
        
        # change align of specific col
        sheet.align_columns(columns = [1,3], align = "w")
        # change foreground color of specific col
        for i in range(col) :
            sheet.highlight_cells(row = i, column = 3, fg = 'red', bg='blue')

    sheet.grid()
    
    return sheet

# sheet 값 update
def update_sheet(sheet, row, val, sign=[]) :
    sheet.set_row_data(row, val)
    if len(sign) > 0 :    
        for i in range(len(sign)) :
            # sign에 따라 fg색 바끔
            profit_col = 'red'
            if val[sign[i]] < 0 :
                profit_col = 'blue'

            sheet_row_column_color(sheet, row, sign[i], foreground=profit_col)

#  end of sheet
#------------------------------------------


#------------------------------------------
#  label related

# label 생성
# relief : flat, groove, raised, ridge, solid, sunken
def create_label(window, x, y, text='', width = 200, foreground='black', background='#EBECF0') :
    label = tk.Label(window, text=text, relief='solid', borderwidth=1, width=width, foreground=foreground, background=background)
    label.place(x=x, y=y)
    return label

# label update
def update_label(window, label, data, foreground='black', background='') :
    if background == '' :
        label.config(text=data, foreground=foreground)
    else :
        label.config(text=data, foreground=foreground, background=background)
#  end of label
#------------------------------------------

#----------------------------------------------------------------------------------------------
# for sample
# 옵션 전광판
def create_option_monitor(window, x, y, title_label, title_x, title_width, table_head, num_options) :
    create_label(window, title_x, y, title_label, title_width) #window, x, y, text='', width = 200,

    row = num_options
    col = len(title_label)

    y = y + 33 # table의 y 위치
    col_width = 50
    width = 301
    height = 435  # 458  1줄은? 22
    sheet = create_sheet(window, x, y, table_head, row, col, col_width, width, height)
    # 수익 컬럼은 넓힌다.
    #sheet_column_width(sheet, 8, 60)
    return sheet

# 양매수/양매도
def create_both_table(window, x, y, label_title, label_width, table_head):
    # 양매도
    create_label(window, x, y, label_title, label_width) #window, x, y, text='', width = 200,
    
    y = y + 20 # table의 y 위치
    row = 2  # head를 포함한 row
    col = 9
    col_width = 50

    width = 461  # table 전체 넓이  돌려보면서 숫자를 맞추어야 함
    height = 44  # table 전체 높이
    sheet = create_sheet(window, x, y, table_head, row, col, col_width, width, height)

    # 수익 컬럼은 넓힌다.
    sheet_column_width(sheet, 8, 60)

    # 구분의 용이를 위하여 두 번째 option의 배경색을 다르게 표출
    dif_col = '#ecf7eb' 
    sheet_column_color(sheet, 3, row, background=dif_col)
    sheet_column_color(sheet, 4, row, background=dif_col)
    sheet_column_color(sheet, 5, row, background=dif_col)
    
    return sheet


if __name__ == "__main__":
    window = tk.Tk()
    f_label = None              # for 선물표시
    both_sell_sheet = None      # for 양매도 표시
    both_buy_sheet  = None      # for 양매수 표시
    g_sheet = None              # 정규 옵션 전광판
    w_sheet = None              # 위클리 옵션 전광판    
    num_option_to_display = 18  # 화면에 동시에 보여줄 옵션 수

    def create_gui():
        global f_label              # for 선물표시
        global both_sell_sheet      # for 양매도 표시
        global both_buy_sheet       # for 양매수 표시
        global g_sheet              # 정규 옵션 전광판
        global w_sheet              # 위클리 옵션 전광판    

        window.geometry('700x750')
        window.configure(bg="#EBECF0")
        # for 선물
        create_label(window, 10, 10, '선물', width=10) # 선물 title
        f_label = create_label(window, 80, 10, '', width=10) # 현재 선물 가격 출력할 label

        # for 양매도
        x = 10
        y = 550
        label_title = "양매도"
        label_width = 10
        table_head = ['행사가', '매도가', '현재가', '행사가', '매도가', '현재가', '양합', '양합차', '수익']  
        both_sell_sheet = create_both_table(window, x, y, label_title, label_width, table_head)

        # for 양매수
        x = 10
        y = y + 90
        label_title = "양매수"
        label_width = 10
        table_head = ['행사가', '매수가', '현재가', '행사가', '매수가', '현재가', '양합', '양합차', '수익']  
        both_buy_sheet = create_both_table(window, x, y, label_title, label_width, table_head)

        # for 옵션전광판
        x = 10
        y = 50
        title_label = "정규옵션"
        title_width = 20
        title_x = 90
        
        table_head = ['대비', '콜', '행사가', '풋', '대비', '양합']
        
        g_sheet = create_option_monitor(window, x, y, title_label, title_x, title_width, table_head, num_option_to_display)
        sheet_column_color(g_sheet, 2, num_option_to_display, background='lightgray')
        sheet_column_color(g_sheet, 5, num_option_to_display, background='yellow')

        # for 주간전광판
        x = 350
        title_x = 440
        title_label = "주간옵션"
        w_sheet = create_option_monitor(window, x, y, title_label, title_x, title_width, table_head, num_option_to_display)
        sheet_column_color(w_sheet, 2, num_option_to_display, background='lightgray')
        sheet_column_color(w_sheet, 5, num_option_to_display, background='yellow')

    def update_gui(cnt) :
        # ebest api를 이용하여 필요한 값을 받아온다.

        # 선물 현재가  표시
        f_val = 312.44
        update_label(window, f_label, f_val, foreground='red') # 현재 선물가격 출력

        # 양매도 상태 표시
        val = [312, 2.0, 1.2, 312, 1.0, 1.5, 1.0, 0.1, 10000]
        row = 0
        update_sheet(both_sell_sheet, row, val, sign=[8]) # sign표시할 col
        refresh(both_sell_sheet)  # update한 것을 화면에 보여줌

        # for 양매수 표시
        val = [312, 2.0, 1.2, 312, 1.0, 1.5, 1.0, -0.1, -10000]
        row = 0
        update_sheet(both_buy_sheet, row, val, sign=[8]) # sign표시할 col
        refresh(both_buy_sheet) # update한 것을 화면에 보여줌

        # for 정규전광판 표시
        val = [-1.0, 0.2, 312.0, 1.0, 1.5, 12+cnt]
        row = 0
        for i in range(num_option_to_display) :
            update_sheet(g_sheet, i, val, sign=[0,4]) # sign표시할 col
            val[2] -= 0.5
        refresh(g_sheet) # update한 것을 화면에 보여줌

        # for 주간전광판 test
        val = [-1.0, 0.2, 312.0, 1.0, 1.5, 120-cnt]
        row = 0
        for i in range(num_option_to_display) :
            update_sheet(w_sheet, i, val, sign=[0,4]) # sign표시할 col
            val[2] -= 0.5
        refresh(w_sheet) # update한 것을 화면에 보여줌


    def main_thread() :
        # ebest api 로그인
        create_gui()
        i = 1
        while(1) :
            update_gui(i)
            i += 1
            time.sleep(1)



    my_thread = threading.Thread(target=main_thread)
    my_thread.daemon = True
    print('starting main_thread')
    my_thread.start()

    window.mainloop()
