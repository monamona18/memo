import os,sys
import tkinter as tk
import tkinter.font as font
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import tkinter.simpledialog as simpledialog
import pyperclip

# ファイルを開く関数
def open_file():
    global file
    fTyp = [("","*.txt")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    file = tk.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
    root.title(file.split("/")[-1])

    # 処理ファイルの出力
    memo.delete('1.0', 'end')
    with open(file, encoding="utf-8") as f:
        content = f.read()
        memo.insert(0.1, content)

# 新規ファイル
def new_file():
    global file
    file = ""
    memo.delete('1.0', 'end')
    root.title("新規メモ")

# 上書き保存の関数
def save_file():
    save = memo.get('1.0', 'end -1c')
    if os.path.isfile(file):
        with open(file, mode="w", encoding="utf-8") as f:
            f.write(save)
    else:
        filename =  filedialog.asksaveasfilename(initialdir = "/",title = "名前を付けて保存",filetypes =  [("text file","*.txt")])
        with open(filename + ".txt", mode='w', encoding="utf-8") as f:
            f.write(save)
        
# 名前を付けて保存
def save_new_file():
    save = memo.get('1.0', 'end -1c')
    filename =  filedialog.asksaveasfilename(initialdir = "/",title = "名前を付けて保存",filetypes =  [("text file","*.txt")])
    with open(filename + ".txt", mode='w', encoding="utf-8") as f:
        f.write(save)
    root.title(filename.split("/")[-1] + ".txt")

# フォントサイズの変更（手動）
def fontsize_change():
    font_data=simpledialog.askstring("フォントサイズの変更", "フォントサイズ：")
    try:
        if font_data == None:
            return
        else:
            font_data = int(font_data)
    except:
        tk.messagebox.showinfo("エラー", "整数を入力してください")
        return
    
    myfont.configure(size=font_data)

# フォントサイズの変更（選択）
def fontsize_change_select(choice):
    myfont.configure(size=choice)

def change_wrap():
    memo.configure(wrap=tk.CHAR)

def change_nowrap():
    memo.configure(wrap=tk.NONE)

# ダブルクリックでコピー
def copy_line(event):
    clip = memo.get('insert linestart', 'insert lineend')
    pyperclip.copy(clip)

# --------------------------------------------------------------------------------------------------------------------

file = "オリジナルメモ帳"

root = Tk()
root.title('オリジナルメモ帳')
root.geometry("650x650")
root.resizable(False, False)

# フォントサイズの設定
myfont = font.Font(root, family="MS Gothic", size=20)

# フレーム
frame1 = ttk.Frame(root, width=650, height=650)
frame1.grid(row=0, column=0)
frame1.grid_propagate(False)


# 画面をテキストボックス化
memo = tk.Text(frame1, wrap = tk.NONE, font = myfont, bd=0)
memo.grid(row=0, column=0, sticky = "nsew")
frame1.grid_columnconfigure(0, weight=1)
frame1.grid_rowconfigure(0, weight=1)

# メニューバーの作成
men = tk.Menu(root) 

#メニューバーを画面にセット 
root.config(menu=men) 

#メニューに親メニュー（ファイル）を作成する 
menu_file = tk.Menu(root, tearoff=False) 
men.add_cascade(label='ファイル', menu=menu_file) 

#親メニューに子メニューを追加する 
menu_file.add_command(label='新規', command=new_file)
menu_file.add_command(label='ファイルを開く', command=open_file) 
menu_file.add_separator() 
menu_file.add_command(label='上書き保存', command=save_file)
menu_file.add_command(label='名前をつけて保存', command=save_new_file)


menu_font = tk.Menu(root, tearoff=False)
men.add_cascade(label='フォント', menu=menu_font) 
menu_font_child = tk.Menu(root, tearoff=False)
menu_font_select = tk.Menu(root, tearoff=False)

menu_font.add_cascade(label='フォントサイズの変更', menu=menu_font_child) 
menu_font_child.add_command(label="フォントサイズの入力", command=fontsize_change)

menu_font_child.add_cascade(label='フォントサイズの変更', menu=menu_font_select)
menu_font_select.add_command(label="12", command=lambda: fontsize_change_select(12))
menu_font_select.add_command(label="18", command=lambda: fontsize_change_select(18))
menu_font_select.add_command(label="20", command=lambda: fontsize_change_select(20))
menu_font_select.add_command(label="24", command=lambda: fontsize_change_select(24))
menu_font_select.add_command(label="36", command=lambda: fontsize_change_select(36)) 
menu_font_select.add_command(label="48", command=lambda: fontsize_change_select(48))
menu_font_select.add_command(label="72", command=lambda: fontsize_change_select(72)) 

menu_setting = tk.Menu(root, tearoff=False)
menu_wrap = tk.Menu(root, tearoff=False)
men.add_cascade(label='設定', menu=menu_setting)
menu_setting.add_cascade(label="折り返し", menu=menu_wrap)
menu_wrap.add_command(label="あり", command=change_wrap)
menu_wrap.add_command(label="なし", command=change_nowrap)


# スクロールバー
xscroll = ttk.Scrollbar(frame1, orient=HORIZONTAL, command=memo.xview)
memo.configure(xscrollcommand = xscroll.set)
xscroll.grid(row = 1, column = 0, sticky='ew')

yscroll = ttk.Scrollbar(frame1, orient=VERTICAL, command=memo.yview)
memo.configure(yscrollcommand = yscroll.set)
yscroll.grid(row = 0, column = 1, sticky='ns')




# ダブルクリックした行をコピーする
memo.bind("<Double-1>", copy_line)

# メインループ
root.mainloop()
