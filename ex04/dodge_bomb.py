import pygame as pg
import random
import sys
import tkinter as tk
import tkinter.messagebox as tkm
from datetime import datetime

def check_bound(obj_rct, scr_rct):
    # 第1引数：こうかとんrectまたは爆弾rect
    # 第2引数：スクリーンrect
    # 範囲内：+1／範囲外：-1
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko, tate


def main():
    global obj_rct, scr_rct, start
    start = datetime.today()  # 開始時刻を取得
    clock =pg.time.Clock()
    pg.display.set_caption("逃げろ！こうかとん")
    scrn_sfc = pg.display.set_mode((1500, 800))
    scrn_rct = scrn_sfc.get_rect()
    pgbg_sfc = pg.image.load("fig/pg_bg.jpg")
    pgbg_rct = pgbg_sfc.get_rect()

    # 練習３
    tori_sfc = pg.image.load("fig/6.png")
    tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = 900, 400
    # scrn_sfcにtori_rctに従って，tori_sfcを貼り付ける
    scrn_sfc.blit(tori_sfc, tori_rct) 

    # 練習５
    bomb_sfc = pg.image.load(("fig/bomb.png"))
    bomb_rct = bomb_sfc.get_rect()
    bomb_rct.centerx = random.randint(10, scrn_rct.width-10)
    bomb_rct.centery = random.randint(10, scrn_rct.height-10)
    scrn_sfc.blit(bomb_sfc, bomb_rct)

    bomb_sfc2 = pg.image.load(("fig/bomb2.png"))
    bomb_rct2 = bomb_sfc2.get_rect()
    bomb_rct2.centerx = random.randint(10, scrn_rct.width-10)
    bomb_rct2.centery = random.randint(10, scrn_rct.height-10)
    scrn_sfc.blit(bomb_sfc2, bomb_rct2)

    vx, vy = +1, +1
    vx2, vy2 = +2, +2

    # 練習２
    while True:
        scrn_sfc.blit(pgbg_sfc, pgbg_rct) 

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        # 練習4
        key_dct = pg.key.get_pressed() # 辞書型
        if key_dct[pg.K_UP]:
            tori_rct.centery -= 1
        if key_dct[pg.K_DOWN]:
            tori_rct.centery += 1
        if key_dct[pg.K_LEFT]:
            tori_rct.centerx -= 1
        if key_dct[pg.K_RIGHT]:
            tori_rct.centerx += 1
        if check_bound(tori_rct, scrn_rct) != (+1, +1):
            # どこかしらはみ出ていたら
            if key_dct[pg.K_UP]:
                tori_rct.centery += 1
            if key_dct[pg.K_DOWN]:
                tori_rct.centery -= 1
            if key_dct[pg.K_LEFT]:
                tori_rct.centerx += 1
            if key_dct[pg.K_RIGHT]:
                tori_rct.centerx -= 1            
        scrn_sfc.blit(tori_sfc, tori_rct) 

        # 練習６
        bomb_rct.move_ip(vx, vy)
        scrn_sfc.blit(bomb_sfc, bomb_rct) 
        yoko, tate = check_bound(bomb_rct, scrn_rct)
        vx *= yoko
        vy *= tate
        bomb_rct2.move_ip(vx2, vy2)
        scrn_sfc.blit(bomb_sfc2, bomb_rct2) 
        yoko, tate = check_bound(bomb_rct2, scrn_rct)
        vx2 *= yoko
        vy2 *= tate

        # 練習８
        if tori_rct.colliderect(bomb_rct) or tori_rct.colliderect(bomb_rct2):
            tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
            tori_rct = tori_sfc.get_rect()
            tori_rct.center = 900, 400
            scrn_sfc.blit(tori_sfc, tori_rct)
            end = datetime.today()  # 終了時刻を取得
            dif = end - start  # 差分を計算 
            root = tk.Tk()
            root.withdraw()
            ret = tkm.showinfo("result", f"耐久時間：{dif.seconds}秒\nゲームオーバーです。")
            if ret == True:
                return
            else:
                return
        pg.display.update()
        clock.tick(1000)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()