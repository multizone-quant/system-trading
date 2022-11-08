# https://cosmosproject.tistory.com/m/610
# https://pythonguides.com/python-tkinter-treeview/

# https://github.com/multizone-quant/system-trading/blob/master/tkinter_sample.py

# requirements
# pip install pkinter

import tkinter as tk
import tkinter.ttk as ttk

def create_table(window, x, y, row, col, heads, widths, width=0) :
    treeview=ttk.Treeview(window, columns=heads, height=row)
    if width == 0 : 
        treeview.place(x=x, y=y)
    else : 
        treeview.place(x=x, y=y, width=width)

    treeview.column('#0', width=1)
    for i in range(0, len(heads)) :
        treeview.heading('#'+str(i+1), text=heads[i])
        treeview.column('#'+str(i+1), width=widths[i], anchor='center')

    vals = [''] * len(heads)
    for i in range(row) :
        id = treeview.insert("", "end", values=vals, iid=str(i))  #insert(상위 항목, 삽입 위치, option)  "end" 뒤에 붙임
    
    return treeview

# items : 출력할 table의 (i,j) label
def update_tree_view(t_view, row, val) :
    for i in range(len(val)) :
        t_view.set(str(row), column=i, value=val[i])  # iid번째에서 col 번째 val[i]로 변환

def create_label(window, x, y, text='', width = 200, background='#EBECF0') :
    label = tk.Label(window, text=text, relief='solid', width=width, background=background)
    label.place(x=x, y=y)
    return label

def update_label(window, label, data, background='') :
    if background == '' :
        label.config(text=data)
    else :
        label.config(text=data, background=background)

if __name__ == "__main__":
    window = tk.Tk()
    window.geometry('620x680')

    # for 선물
    create_label(window, 10, 10, '선물', width=10) # 선물 title
    f_label = create_label(window, 80, 10, '', width=10) # 현재 선물 가격 출력할 label
    f_val = 312.44
    update_label(window, f_label, f_val, background='red') # 현재 선물가격 출력

    # for 양매수
    width = 50
    heads = ['행사가', '매도가', '현재가', '행사가', '매도가', '현재가', '양합', '양합차', '수익']
    widths = [width] * len(heads) 
    widths[8] = 80 # 수익
            
    row = 1
    col = 9

    create_label(window, 10, 50, '양매도', width=10) #window, x, y, text='', width = 200,
    tr_view = create_table(window, 10, 70, row, col, heads, widths)

    # 출력하고자 하는 값    
    val = [312, 2.0, 1.2, 312, 1.0, 1.5, 1.0, 0.1, 10000]
    
    update_tree_view(tr_view, 0, val) # 1번째 row에 추가
    window.mainloop()
