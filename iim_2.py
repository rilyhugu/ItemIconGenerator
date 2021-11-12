import tkinter as tk
import tkinter.ttk as ttk
import os
import glob

from tkinter.constants import ACTIVE, END
from typing import Collection
import random
from PIL import Image, ImageTk
from tkinter import filedialog

#作業ディレクトリの変更
os.chdir(os.path.dirname(__file__))

#アプリの作成
root = tk.Tk()
root.title("Item Icon Maker")
root.geometry("448x364")

#画像リストの取得
def load_resource(path):
    resources = glob.glob(path)
    list = []
    for i in resources:
        list.append(os.path.basename(i))
    list.sort(key=len)
    return list

blade = load_resource("./resources/weapon/sword/blade/*.png")
grip = load_resource("./resources/weapon/sword/grip/*.png")
hilt = load_resource("./resources/weapon/sword/hilt/*.png")

#画像の表示サイズ変更
def resize_image(path):
    image = Image.open(path)
    image = image.resize((128, 128), resample=0)
    return image

#画像のランダム選択
def select_random():
    lb_blade.select_clear(0, END)
    lb_grip.select_clear(0, END)
    lb_hilt.select_clear(0, END)
    lb_blade.select_set(random.choice(range(0, lb_blade.size() - 1)))
    lb_grip.select_set(random.choice(range(0, lb_grip.size() - 1)))
    lb_hilt.select_set(random.choice(range(0, lb_hilt.size() - 1)))
    select_listbox("<<ListboxSelect>>")

#画像の選択
def select_listbox(event):
    global image_preview
    global image_result
    blade = Image.open("./resources/weapon/sword/blade/" + str(lb_blade.get(lb_blade.curselection())))
    grip = Image.open("./resources/weapon/sword/grip/" + str(lb_grip.get(lb_grip.curselection())))
    hilt = Image.open("./resources/weapon/sword/hilt/" + str(lb_hilt.get(lb_hilt.curselection())))

    image_result = Image.alpha_composite(grip, hilt)
    image_result = Image.alpha_composite(blade, image_result)

    image_preview = ImageTk.PhotoImage(image_result.resize((128, 128), resample=0))
    cv_preview.itemconfig(draw_preview, image=image_preview)

#名前を付けて保存
def named_save():
    global image_result
    file = filedialog.asksaveasfilename(
        title = "名前を付けて保存",
        filetypes = [("PNG", ".png")],
        initialdir = "./saves",
        defaultextension = "png"
    )
    if len(file) != 0:
        image_result.save(file)


#ノートブックの作成
notebook = ttk.Notebook(root)

#タブの作成
tab_sword = tk.Frame(notebook)
tab_stuff = tk.Frame(notebook)

notebook.add(tab_sword, text="Sword")
notebook.add(tab_stuff, text="Stuff")



#フレームの作成
#コンポーネント用フレーム
fr_component = tk.Frame(tab_sword, relief="ridge", bd=1)

#キャンバス用フレーム
fr_canvas = tk.Frame(tab_sword)#, relief="groove", bd=1)

#ボタン用フレーム
fr_button = tk.Frame(fr_canvas)#, relief="groove", bd=1)


#コンポーネント配置
#===========================================
la_blade = tk.Label(fr_component, text="Blade",font=("Helvetica",10))
la_blade.grid(row=0,column=0, sticky="W"+"E")

sc_blade = tk.Scrollbar(fr_component, orient="vertical")

lb_blade = tk.Listbox(fr_component, listvariable=tk.StringVar(value=blade), width=20, height=10, yscrollcommand=sc_blade.set, selectmode="single", activestyle="none", exportselection=False)
lb_blade.grid(row=1, column=0)
lb_blade.bind("<<ListboxSelect>>", select_listbox)

sc_blade.config(command=lb_blade.yview)
sc_blade.grid(row=1, column=1, sticky="N"+"S")
#-------------------------------------------
la_grip = tk.Label(fr_component, text="Grip",font=("Helvetica",10))
la_grip.grid(row=0,column=2, sticky="W"+"E")

sc_grip = tk.Scrollbar(fr_component, orient="vertical")

lb_grip = tk.Listbox(fr_component, listvariable=tk.StringVar(value=grip), width=20, height=10, yscrollcommand=sc_grip.set, selectmode="single", activestyle="none", exportselection=False)
lb_grip.grid(row=1, column=2)
lb_grip.bind("<<ListboxSelect>>", select_listbox)

sc_grip.config(command=lb_grip.yview)
sc_grip.grid(row=1, column=3, sticky="N"+"S")
#-------------------------------------------
la_hilt = tk.Label(fr_component, text="Hilt",font=("Helvetica",10))
la_hilt.grid(row=0,column=4, sticky="W"+"E")

sc_hilt = tk.Scrollbar(fr_component, orient="vertical")

lb_hilt = tk.Listbox(fr_component, listvariable=tk.StringVar(value=hilt), width=20, height=10, yscrollcommand=sc_hilt.set, selectmode="single", activestyle="none", exportselection=False)
lb_hilt.grid(row=1, column=4)
lb_hilt.bind("<<ListboxSelect>>", select_listbox)

sc_hilt.config(command=lb_hilt.yview)
sc_hilt.grid(row=1, column=5, sticky="N"+"S")
#====================================================================================

#キャンバス配置
cv_preview = tk.Canvas(fr_canvas, bg="white", width=128, height=128)
cv_preview.grid(row=0, column=0)

#ボタン配置
style = ttk.Style()



bt_random = ttk.Button(fr_button, text="ランダム", command=select_random)
bt_random.grid(row=0, column=0, sticky="W"+"E")
bt_save = ttk.Button(fr_button, text="保存", command=named_save)
bt_save.grid(row=1, column=0, sticky="W"+"E")


#初期値設定
lb_blade.select_set(0)
lb_grip.select_set(0)
lb_hilt.select_set(0)

draw_preview = cv_preview.create_image(64, 64)


fr_component.grid(row=0, column=0)
fr_canvas.grid(row=1, column=0, sticky="w")
fr_button.grid(row=0, column=1)

select_listbox("<<ListboxSelect>>")


notebook.pack(expand=True, fill='both', padx=10, pady=10)

root.resizable(width=False,height=False)
root.mainloop()
