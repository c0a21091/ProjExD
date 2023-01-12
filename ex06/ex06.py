import copy
import os
import pygame as pg
import random
import sys
import time
from datetime import datetime
import tkinter as tk
import tkinter.messagebox as tkm


WINDOW_SIZE = (1400, 900) #ウインドウサイズ
LIFE_POINT = 3 #ライフ
INVINCIBLE_TIME = 1 #無敵時間(sec)
BOMB_NUM = 3 #爆弾の初期の数
HIT_STOP = 0.2 #ヒットストップの設定
F_P_SIZE   = 60     # 得点用フォントサイズ
SCROLL_SPEED = 0.5 #スクロールのスピード
ENEMY_SPAWNING_TIME = 2000 #敵のスポーン時間
KOUKATON_SPEED = 3

class Screen(pg.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.screen = pg.display.set_mode(WINDOW_SIZE)


#スコア計算について加筆:佐野
class ScoreBoard(Screen):
    #スコア画面についてのクラス
    def __init__(self) -> None:
        super().__init__()
        self.font  = pg.font.SysFont("hgep006", F_P_SIZE)
        self.point = 0

    def cal_score(self, point):
        self.point += point

    def blit(self):
        self.scoreboard = pg.draw.rect(self.screen, (100, 100, 100), (1000, 0, WINDOW_SIZE[0], WINDOW_SIZE[1]))

    def draw(self):
        text = self.font.render("SCORE : " + "{:04d}".format(self.point), True, (63,255,63))
        self.screen.blit(text, [1010, 10])
        text = self.font.render("TIME : " + str((datetime.now()-st).seconds), True, (63,255,63))
        self.screen.blit(text, [1010, 100])
#担当 佐野 ここまで

class Image(Screen):
    def __init__(self, im_pass) -> None:
        """画像を扱うクラス
        Args:
            im_pass (string): 読み込む画像のパス
        """
        super().__init__()
        self.im_pass = im_pass
        self.image = pg.image.load(im_pass)
        self.rect = self.image.get_rect()
        
            
class Koukaton(Image):   
    key_dic = {
        "left":pg.K_LEFT, "right":pg.K_RIGHT, "up":pg.K_UP, 
        "down":pg.K_DOWN, "slow":pg.K_LSHIFT, "attack":pg.K_LCTRL,
        "exit":pg.K_ESCAPE, "reset":pg.K_F1
        } #キー の設定
    
    def __init__(self, im_pass, pos, speed) -> None:
        """こんかとんのクラス
        Args:
            pos (list): 初期座標
            speed (int, optional): こうかとんの移動速度. Defaults to 1.
        """
        super().__init__(im_pass)
        self.pos = pos
        self.speed = speed
        self.image = pg.transform.rotozoom(self.image, 0, 2.0)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.effct_image = pg.image.load("nc289332.png")
        self.effect_image = pg.transform.rotozoom(self.effct_image, 0, 0.6)
        self.effect_rect = self.effect_image.get_rect()
        self.attack_mode = False
        
    def blit(self):
        self.screen.blit(self.image, self.rect)
        
    def update(self):
        #こうかとん の移動の処理
        before_koukaton_rect = copy.deepcopy(self.rect) #こうかとん の移動前の座標
        pressed = pg.key.get_pressed()
        if pressed[Koukaton.key_dic["left"]]:
            self.rect.move_ip(-1 * self.speed, 0)
        if pressed[Koukaton.key_dic["right"]]:
            self.rect.move_ip(self.speed, 0)
        if pressed[Koukaton.key_dic["up"]]:
            self.rect.move_ip(0, -1 * self.speed)
        if pressed[Koukaton.key_dic["down"]]:
            self.rect.move_ip(0, self.speed)
            
        if pressed[Koukaton.key_dic["slow"]]:
            self.speed = 2
        elif pressed[Koukaton.key_dic["slow"]] == False:
            self.speed = KOUKATON_SPEED
        
        if pressed[Koukaton.key_dic["attack"]]:
            self.attack_mode = True     
            self.effect_rect.center = self.rect.center
            self.screen.blit(self.effect_image, self.effect_rect)
        elif pressed[Koukaton.key_dic["attack"]] == False:
            self.attack_mode = False
        
        #こうかとん が画面外に出たとき、元の位置に戻す、
        for i in range(2):
            # i == 0 のとき x座標が範囲外
            # i == 1 のとき y座標が範囲外
            if i == 0:
                tmp = 400
            else:
                tmp = 0
            if 0 >= self.rect[i] or self.rect[i] + self.rect[i+2]>= WINDOW_SIZE[i] - tmp:
                print(before_koukaton_rect)
                self.rect = before_koukaton_rect
        
    def change_image(self, ip):
        """画像を変更する
        Args:
            ip (string): 画像のパス
        """
        self.image = pg.image.load(ip)
        self.image = pg.transform.rotozoom(self.image, 0, 2.0)
            
#担当 山下
class Bullet(Image):
    def __init__(self, im_pass, pos, speed) -> None:
        super().__init__(im_pass)
        self.pos = pos
        self.speed = speed
        self.image = pg.transform.rotozoom(self.image, 0, 0.1)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        
    def update(self):
        self.rect.move_ip(0, -1)   
        if self.rect.y > 1000:
            self.kill()

# 担当 原田慶虎  
class Enemy(Image):
    def __init__(self, im_pass, speed=[0, 1]) -> None:
        """敵のクラス
        Args:
            im_pass (string): 読み込む画像のパス
            speed (list, optional): [x方向の速度, y方向の速度]. Defaults to [1, 1].
        """
        n = random.randint(0,2)
        super().__init__(im_pass[n])
        x = random.randint(0, WINDOW_SIZE[0]-400)
        y = 100
        self.pos = [x, y]
        self.speed = speed
        self.image = pg.transform.rotozoom(self.image, 0, 0.3)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        
    def blit(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.rect.move_ip(self.speed)
        if self.rect.y > 1000:
            self.kill()
#担当 原田慶虎 ここまで


class BackGroundImage(Image):
    BGI_Y = 0
    def __init__(self, im_pass,  title) -> None:
        """背景画像のクラス
        Args:
            im_pass (string): 読み込む画像のパス
            title (string): タイトル名
        """
        super().__init__(im_pass)    
        self.title = title
        pg.display.set_caption(self.title)
        
    def blit(self):
        self.BGI_Y = (self.BGI_Y + SCROLL_SPEED)%WINDOW_SIZE[1]
        self.screen.blit(self.image, [0, self.BGI_Y -WINDOW_SIZE[1]])
        self.screen.blit(self.image, [0, self.BGI_Y])
    
class Life(Image):
    def __init__(self, im_pass, pos, life=LIFE_POINT):
        """こうかとんのライフのクラス
        Args:
            im_pass (string): 読み込む画像のパス
            pos (tuple): 一つ目のライフの位置
            life (int, optional): 初期ライフの数. Defaults to LIFE_POINT.
        """
        super().__init__(im_pass)
        self.life = life
        self.pos = pos
        self.life_image = []
        self.life_rect = []
        for i in range(self.life):
            self.life_image.append(self.image)
            self.life_image[i] = pg.transform.rotozoom(self.life_image[i], 0, 0.3)
            self.life_rect.append(self.life_image[i].get_rect())
            self.life_rect[i].center = (self.pos[0] + i * 100, self.pos[1])
        
    def blit(self):
        for i in range(self.life):
            self.screen.blit(self.life_image[i], self.life_rect[i])


class Bomb(Image):
    def __init__(self, im_pass, speed=[0, 2]) -> None:
        """爆弾のクラス
        Args:
            im_pass (string): 読み込む画像のパス
            speed (list, optional): [x方向の速度, y方向の速度]
        """
        super().__init__(im_pass)
        x = random.randint(0, WINDOW_SIZE[0]-400)
        y = 100
        self.pos = [x, y]
        self.speed = speed
        self.image = pg.transform.rotozoom(self.image, 0, 0.3)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        
    def blit(self):
        self.screen.blit(self.image, self.rect)
        
    def update(self):
        self.rect.move_ip(self.speed)
        if self.rect.y > 1000:
            self.kill()
            
class Sound:
    def __init__(self, sd_name) -> None:
        """音のクラス
        Args:
            sd_name (string): 読み込むサウンドのファイル名
        """
        self.sd_name = sd_name
        pg.mixer.init(frequency = 44100)    # 初期設定
        self.music = pg.mixer.Sound(self.sd_name)     # 音楽ファイルの読み込み
        
        
class BGM(Sound):
    def __init__(self, sd_name) -> None:
        """BGMのクラス
        """
        super().__init__(sd_name)
        self.music.set_volume(0.1)
        self.music.play(-1)  # 音楽の再生回数(ループ再生)
        
    def stop_sound(self):
        self.music.stop()
        
class SoundEffect(Sound):
    def __init__(self, sd_name) -> None:
        """効果音のクラス
        """
        super().__init__(sd_name)
        self.music.set_volume(0.3)
        
    def start_sound(self):
        self.music.play(0)
          
#ゲームオーバー時の処理　轟
def gameover():
    root = tk.Tk()
    root.withdraw()
    ret = tkm.showinfo("result", f"耐久時間：{int(pg.time.get_ticks()/1000)}秒\nゲームオーバーです。")
    pg.quit()
    sys.exit()

#衝突時の処理
def collision_object(ko, lf, se, obj=None):
    """
    爆弾とこうかとんの衝突時の処理
    Args:
        ko (Koukaton): こうかとん
        lf (Life): ライフ
        se (SoundEffect): 効果音
    """
    global crash_time
    time_end = time.time()
    #前回衝突時から今回衝突時の時間の差が無敵時間より大きいなら、ライフを減らす
    if time_end - crash_time < INVINCIBLE_TIME:
        return
    se.start_sound()
    #アタックモードで衝突したのが敵ならその後の処理はしない
    if ko.attack_mode and obj == "enemy":
        return

    if lf.life != 0:    
        time.sleep(HIT_STOP)
        crash_time = time.time()#衝突時の時間を保存する
        lf.life -= 1
        num = random.randint(0, 9)
        ko.change_image(f"../fig/{num}.png")

    #ライフが0 なら gameover()を実行
    if lf.life == 0:
        gameover()
            

def main():
    global crash_time, st
    os.chdir(os.path.dirname(__file__))
    print("pass:"+os.getcwd())
    pg.init()
    scr = Screen()
    clock = pg.time.Clock()   

    #BGMの設定
    bgm = BGM("こんとどぅふぇ素材No.0129-Last-Horizon.wav")
    
    #効果音の設定
    hit_enemy = SoundEffect(sd_name="nc172283.wav")
    hit_bomb = SoundEffect(sd_name="nc84862.wav")
    burn_sound = SoundEffect(sd_name="nc224596.wav")
    
    #背景の設定
    scr = BackGroundImage(im_pass="space.jpg" ,title="飛べ、こうかとん")
    
    #スコアボードの設定
    sb = ScoreBoard()
    
    #こうかとん の設定
    koukaton = Koukaton(im_pass="../fig/0.png", pos=(500, 800), speed=KOUKATON_SPEED)
    
    #こうかとん のライフ
    life = Life(im_pass="nc237709.png", pos=(200 ,100))
    
    
    #爆弾の設定
    bomb = [Bomb(im_pass="bakudan.png", speed=[0, 2]) for i in range(BOMB_NUM)]
    
    all_sprites = pg.sprite.Group() #画像の処理用
    bomb_sprites = pg.sprite.Group() #爆弾衝突判定用
    enemy_sprites = pg.sprite.Group() #敵キャラ衝突判定用
    bullet_sprites = pg.sprite.Group() #弾丸 衝突判定用 担当 山下
    
    all_sprites.add(koukaton)
    for i in range(BOMB_NUM):
        all_sprites.add(bomb[i])
        bomb_sprites.add(bomb[i])
    
    crash_time = time.time()

    #担当 山下
    #弾の設定
    shot_event = pg.USEREVENT + 2
    pg.time.set_timer(shot_event, 300)

    #スコアについて加筆:佐野
    score = ScoreBoard()
    sb = ScoreBoard() 
    st = datetime.now()
    
    #担当 原田
    #敵を追加するイベントを作成:
    EnemyEvent = pg.USEREVENT + 1
    #ENEMY_SPAWNING_TIMEごとに行うようにタイマーをセット
    pg.time.set_timer(EnemyEvent, ENEMY_SPAWNING_TIME)
    
    
    
    while True:
        #画像の表示と更新
        scr.blit()
        all_sprites.draw(scr.screen)
        life.blit()
        sb.blit()

        #スコアについて加筆:佐野
        score.cal_score(1)
        score.draw()
        
        #イベント発生時の処理
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                
            if event.type == pg.KEYDOWN:
                if event.key == Koukaton.key_dic["exit"]:
                    pg.quit()
                    sys.exit()
                if event.key == Koukaton.key_dic["reset"]:
                    crash_time = time.time()
                    bgm.stop_sound()
                    main()
                print(f"push:{pg.key.name(event.key)}")  

            #担当 山下
            if event.type  ==shot_event:
                tmp = Bullet(im_pass="nc138278.png", pos=koukaton.rect.center, speed = 2)
                all_sprites.add(tmp)
                bullet_sprites.add(tmp)

            #担当 原田
            if event.type == EnemyEvent:
                #敵の追加 
                tmp = Enemy(im_pass=["Green.png", "Pink.png", "Purple.png"], speed=[0, 1])
                all_sprites.add(tmp)
                enemy_sprites.add(tmp)
        
        #爆弾の衝突
        bomb_collided = pg.sprite.spritecollide(koukaton, bomb_sprites, True)
        if bomb_collided:
            collision_object(ko=koukaton, lf=life, se=hit_bomb)
        #敵キャラとの衝突
        enemy_collided = pg.sprite.spritecollide(koukaton, enemy_sprites, koukaton.attack_mode)
        if koukaton.attack_mode:
            se = burn_sound
        else:
            se = hit_enemy
        if enemy_collided:
            collision_object(ko=koukaton, lf=life, se=se, obj="enemy")
        
        #弾丸が敵キャラと衝突 担当 山下
        bullet_collided = pg.sprite.groupcollide(bullet_sprites, enemy_sprites, True, True)
        if bullet_collided:
            #スコア計算の処理を追加 担当 佐野
            score.cal_score(10000)
                
        all_sprites.update()
        pg.display.update()
        clock.tick(1000)

if __name__ == "__main__":
    main()