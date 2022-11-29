import tkinter as tk
import tkinter.messagebox as tkm


def click_number(event):         #数字をクリックした場合
    btn = event.widget
    num = btn["text"]
    entry.insert(tk.END,num)

def click_equal(event):          #＝をクリックした場合
    eqn = entry.get()
    res = eval(eqn)
    entry.delete(0,tk.END)
    entry.insert(tk.END, res)

def click_AC(event):          #ACをクリックした場合
    entry.delete(0,tk.END)

def click_hanten(event):          #+/-をクリックした場合
    eqn = entry.get()
    res = str(eval(eqn))
    entry.delete(0,tk.END)
    res_hanten = list(res)
    if res_hanten[0] == "-":
        res_hanten.pop(0)
    else:
        res_hanten.insert(0,"-")
    hanten = "".join(res_hanten)
    entry.insert(tk.END, hanten)

def click_percent(event):          #%をクリックした場合
    eqn = entry.get()
    res = str(eval(eqn))
    entry.delete(0,tk.END)
    res_percent = list(res)
    c = res_percent.count(".")
    if c == 1:
        res_percent.remove(".")
    res_percent.insert(2,".")
    if res_percent[-1] == "0":
        del res_percent[-1]
    strres = "".join(res_percent)
    entry.insert(tk.END, f"{strres}0%")

root = tk.Tk()                   #画面の設定
root.title("電卓")              #名前付け
root.geometry("600x560")         #画面サイズ


entry = tk.Entry(root, width=10, font=(", 40"),justify="right")
entry.grid(row=0, column=0, columnspan=3)                       #位置設定

c_list = ["#FA8072", "#CD5C5C", "#A260BF"] #色のリスト
r, c = 4, 0
numbers = list(range(0,10,+1))
numbers.insert(1, ".")
numbers.insert(2,"")
for i, num in enumerate(numbers, 1):
    btn = tk.Button(root, text = f"{num}",font=("Times New Roman", 30), width=4, height=2, bg=c_list[0])
    btn.bind("<1>",click_number)
    btn.grid(row = r, column = c)
    c += 1
    if i%3 == 0:
        r -= 1
        c = 0

btn = tk.Button(root,text = "=",font = ("Times", 30), width=4, height=2, bg=c_list[1])
btn.bind("<1>",click_equal)
btn.grid(row = 4, column = 4)

btn = tk.Button(root,text="AC",font=("Times", 30), width=4, height=2, bg=c_list[2])
btn.bind("<1>",click_AC)
btn.grid(row = 1, column = 4)



btn = tk.Button(root,text="%",font=("Times", 30), width=4, height=2, bg=c_list[1])
btn.bind("<1>",click_percent)
btn.grid(row = 1, column = 5)

btn = tk.Button(root,text = "+/-",font=("Times", 30), width=4, height=2, bg=c_list[1])
btn.bind("<1>",click_hanten)
btn.grid(row = 2, column = 6)

btn = tk.Button(root,text = "+",font=("Times", 30), width=4, height=2, bg=c_list[1])
btn.bind("<1>",click_number)
btn.grid(row = 2, column = 4)
btn = tk.Button(root,text = "-",font=("Times", 30), width=4, height=2, bg=c_list[1])
btn.bind("<1>",click_number)
btn.grid(row = 3, column = 4)
btn = tk.Button(root,text = "*",font=("Times", 30), width=4, height=2, bg=c_list[1])
btn.bind("<1>",click_number)
btn.grid(row = 2, column = 5)
btn = tk.Button(root,text = "/",font=("Times", 30), width=4, height=2, bg=c_list[1])
btn.bind("<1>",click_number)
btn.grid(row = 3, column = 5)
btn = tk.Button(root,text = "**",font=("Times", 30), width=4, height=2, bg=c_list[1])
btn.bind("<1>",click_number)
btn.grid(row = 1, column = 6)


root.mainloop()