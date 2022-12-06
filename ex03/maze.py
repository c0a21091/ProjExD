import tkinter as tk
import tkinter.messagebox as tkm
import maze_maker as mm

def key_down(event):
    global key
    key = event.keysym


def key_up(event):
    global key
    key = ""

def main_proc():
    global cx, cy 
    global mx, my
    global tmr, jid
    tmr = tmr+1
    if key == "Up": my -= 1
    if key == "Down": my += 1
    if key == "Left": mx -= 1
    if key == "Right": mx += 1
    if maze_lst[mx][my] == 1: # 移動先が壁だったら
        if key == "Up": my += 1
        if key == "Down": my -= 1
        if key == "Left": mx += 1
        if key == "Right": mx -= 1
    if mx == 13 and my == 7:                      #ゴールしたら
        tkm.showinfo("goal", f"所要時間：{tmr/10}秒\nゴールしました。")
        root.mainloop()        
    cx, cy = mx*100+50, my*100+50
    canvas.coords("kokaton", cx, cy)
    root.after(100, main_proc)
    

if __name__ == "__main__":
    tmr = 0
    root = tk.Tk()
    root.title("迷えるこうかとん")
    canvas = tk.Canvas(root, width=1500, height=900, bg="black")
    canvas.pack()
    maze_lst = mm.make_maze(15, 9)
    # print(maze_lst)
    mm.show_maze(canvas, maze_lst)

    #スタート
    start1 = tk.PhotoImage(file="fig/start.png")
    #ゴール
    goal = tk.PhotoImage(file="fig/goal.png")
    sx, sy = 1, 1
    ssx, ssy = sx*100+50, sy*100+50
    canvas.create_image(ssx, ssy, image=start1, tag = "start")
    canvas.create_image(1350, 750, image=goal, tag = "goal")
    

    mx, my = 1, 1
    cx, cy = mx*100+50, my*100+50
    tori = tk.PhotoImage(file="fig/8.png")
    canvas.create_image(cx, cy, image=tori, tag="kokaton")
    key = ""
    root.bind("<KeyPress>", key_down)
    root.bind("<KeyRelease>", key_up)
    main_proc()

    root.mainloop()

    