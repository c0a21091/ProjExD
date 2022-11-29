import tkinter as tk
import tkinter.messagebox as tkm

#練習１
root =tk.Tk()
root.title("電卓")
root.geometry("300x500")

#練習２
def button_click(event):
    btn = event.widget
    txt = btn["text"]
    tkm.showwarning("警告", f"{txt}のボタンがクリックされました")

r, c = 0, 0
for num in range(9, -1, -1):
    button = tk.Button(root, text=f"{num}",width=4,height=2,font=("",30))
    button.bind("<1>",button_click)
    button.grid(row=r,column=c)
    c += 1
    if c%3 == 0:
        r+= 1
        c = 0
    
root.mainloop()