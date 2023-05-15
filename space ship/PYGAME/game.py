#sprite
from math import ceil
import pygame
import random
import os

from pygame.constants import HIDDEN

FPS = 60
WIDTH = 350
HEIGHT = 700

#顏色
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
ROCKCOLOR =(255, 50, 0)
BULLETCOLOR =(255, 178, 25)
BLACK = (0 , 0, 0)

#初始化 pygame 原始參數
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("射擊小遊戲")
clock = pygame.time.Clock()

#載入圖片
background_img = pygame.image.load(os.path.join("PYGAME\\IMG", "back.png")).convert() #轉成pygame好處理
ship_img = pygame.image.load(os.path.join("PYGAME\\IMG", "dickship1.png")).convert()
ship_img_lives = pygame.transform.scale(ship_img, (20,20))
ship_img_lives.set_colorkey(BLACK)
pygame.display.set_icon(ship_img_lives)#改變視窗icon
#rock_img = pygame.image.load(os.path.join("PYGAME\\IMG", "rock.png")).convert()
shoot_img = pygame.image.load(os.path.join("PYGAME\\IMG", "shoot.png")).convert()
background_img = pygame.transform.scale(background_img,(700  ,350 ))
background_img = pygame.transform.rotate(background_img,270 )
rock_imgs = []
for i in range(4):
    rock_imgs.append(pygame.image.load(os.path.join("PYGAME\\IMG", f"rock{i}.png")).convert())
expl_anim = {}
expl_anim['large']=[]
expl_anim['ship']=[]
expl_anim['ship_die']=[]
for i in range(9):
    expl_imgs = pygame.image.load(os.path.join("PYGAME\\IMG", f"expl{i}.png")).convert()
    expl_imgs.set_colorkey(WHITE)
    expl_die_imgs = pygame.image.load(os.path.join("PYGAME\\IMG", f"dieexpl{i}.png")).convert()
    expl_die_imgs.set_colorkey(WHITE)
    expl_anim['large'].append(pygame.transform.scale(expl_imgs, (100, 100)))
    expl_anim['ship'].append(pygame.transform.scale(expl_imgs, (150, 150)))
    expl_anim['ship_die'].append(pygame.transform.scale(expl_die_imgs, (150, 150)))
font_name = os.path.join("PYGAME", "font.ttf")

power_imgs = {}
power_imgs['shield'] = pygame.image.load(os.path.join("PYGAME\\IMG", "shield.png")).convert()
power_imgs['gun'] = pygame.image.load(os.path.join("PYGAME\\IMG", "gun.png")).convert()

#載入音樂
shoot_sound = pygame.mixer.Sound(os.path.join("PYGAME\\sound", "shoot.wav"))
power_sounds = []
for i in range(2): 
    power_sounds.append(pygame.mixer.Sound(os.path.join("PYGAME\\sound", f"pow{i}.wav")))
expl_sounds = []
for i in range(2): 
    expl_sounds.append(pygame.mixer.Sound(os.path.join("PYGAME\\sound", f"expl{i}.wav")))
pygame.mixer.music.load(os.path.join("PYGAME\\sound", "background.wav "))
pygame.mixer.music.set_volume(0.4) #調整back聲音

#class
def draw_init():
    screen.blit(background_img, (0, 0))
    draw_text(screen, '射擊小遊戲', 64, WHITE, WIDTH/2,HEIGHT/10)
    draw_text(screen, '方向鍵移動 空白建射擊', 25, WHITE, WIDTH/2,HEIGHT/4)
    draw_text(screen, 'PUSH ANY KEY', 20, WHITE, WIDTH/2,HEIGHT-100)
    pygame.display.update()
    waiting = True
    while waiting:        
        clock.tick(FPS)
            #pygame.event.get() 記錄所有事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP: #按下鍵盤鬆開
                waiting = False
                return False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(ship_img,(70 ,70 ))
        #self.image = ship_img
        self.image.set_colorkey(BLACK) #顏色透明化
        self.rect = self.image.get_rect() #定位圖片 框起來
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 20
        self.speedx = 5
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.gun_level = 1
        self.hide_time = 0
        self.gun_power_time = 0
    def update(self):
        now = pygame.time.get_ticks()
        if self.hidden and now-self.hide_time > 10000:
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT - 20
        key_pressed = pygame.key.get_pressed() #回傳一整串布林值判斷按鍵有沒有被按
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if self.rect.right > WIDTH :
            self.rect.right = WIDTH
        if self.rect.left < 0 :
            self.rect.left = 0
        if self.gun_level > 1 and now-self.gun_power_time > 5000:
            self.gun_level -=1
            self.gun_power_time = now
    def shoot(self):
        if not(self.hidden):
            gun_parameter = 0
            for bullet in range(self.gun_level):
                if (bullet%2-0.5) > 0 and bullet != 0:
                    gun_parameter += 4
                bullet = BULLET(gun_parameter*((bullet%2)-0.5), self.rect.centerx,self.rect.top+10)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+1000)

class ROCK(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rockwidth = random.randrange(20, 70)
        self.rockhight = random.randrange(30, 60 )
        self.rockangle = 0
        self.image_ori = pygame.transform.scale(random.choice(rock_imgs),(self.rockwidth  ,self.rockhight  ))
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() #定位圖片 框起來
        self.rect.centerx = random.randrange(0, WIDTH)
        self.rect.bottom = 0
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(2, 10)
        self.rotatespeed = random.randrange(-5, 5 ) 

    def rotate(self):
        self.rockangle += self.rotatespeed +0.5
        self.rockangle = self.rockangle % 360
        self.image = pygame.transform.rotate(self.image_ori, self.rockangle)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        
    def update(self):
        self.rect.centerx += self.speedx
        self.rect.bottom += self.speedy
        self.rotate()
        if  self.rect.top > HEIGHT+self.rockhight or self.rect.right > WIDTH+self.rockwidth or self.rect.left < -self.rockwidth :
            self.rockwidth = random.randrange(20,50)
            self.rockhight = random.randrange(30, 45)
            self.image = pygame.transform.scale(random.choice(rock_imgs) ,(self.rockwidth  ,self.rockhight  ))
            self.image.set_colorkey(BLACK)
            self.rect.centerx = random.randrange(0, WIDTH)
            self.rect.bottom = 0
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(2, 10)

class BULLET(pygame.sprite.Sprite):
    def __init__(self, speedx, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(shoot_img,(30  ,60 ))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect() #定位圖片 框起來
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        self.speedx = speedx
    def update(self): 
        self.rect.bottom += self.speedy
        self.rect.centerx += self.speedx
        if self.rect.bottom < 0 :
            self.kill()

class EXPLOSIOM(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect() #定位圖片 框起來
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 60

    def update(self): 
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class POWER(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['gun', 'shield'])
        self.image = power_imgs[self.type]
        self.image = pygame.transform.scale(self.image,(30  ,30 ))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() #定位圖片 框起來
        self.rect.center = center
        self.speedy = 3
    def update(self): 
        self.rect.bottom += self.speedy
        if self.rect.top > HEIGHT :
            self.kill()


def small_pics(img, scale_x, scale_y):
    smallpics = img.set_colorkey(BLACK)
    smallpics = pygame.transform.scale(smallpics,(scale_x,scale_y))
    return smallpics

def new_rock():
    rock = ROCK()
    all_sprites.add(rock)
    rocks.add(rock)

def draw_text(surf, text, size, color, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def draw_health(surf, hp, x, y):
    if hp  < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2) #第四參數等於 外框的像素

def draw_live(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img.set_colorkey(BLACK)
        img_rect.center = (x+30*i, y)
        surf.blit(img, img_rect)


#創造物件
all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powers = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
rocknumber = 10
for rocknum in range(rocknumber) :
    new_rock()
score = 0
pygame.mixer.music.play(-1) #參數是播放次數 -1等於無限

#遊戲迴圈
init_screen = True
running = True
while running:
    if init_screen:
        close = draw_init()
        if close:
            break
        init_screen = False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        rocknumber = 10
        for rocknum in range(rocknumber) :
            new_rock()
        score = 0
    clock.tick(FPS)
    #pygame.event.get() 記錄所有事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN: #按下鍵盤
            if event.key == pygame.K_SPACE:
                player.shoot()
    #遊戲刷新 執行每個物件的update函式
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True) #回傳值為字典碰撞到的石頭 boolen true消失
    for hit in hits:
        score += hit.rockwidth #hit 等於碰撞石頭
        score += hit.rockhight 
        score = int(score)
        expl = EXPLOSIOM(hit.rect.center, 'large')
        all_sprites.add(expl)
        random.choice(expl_sounds).play()
        new_rock()
        if random.random() > 0.99 :
            power = POWER(hit.rect.center)
            all_sprites.add(power)
            powers.add(power)
    hit_play_rock = pygame.sprite.spritecollide(player, rocks, True) #回傳值為list 所有碰撞到player的rock true消失
    for hit in hit_play_rock:
        player.health -= 10
        expl = EXPLOSIOM(hit.rect.center, 'ship')
        all_sprites.add(expl)
        random.choice(expl_sounds).play()
        new_rock()
        if player.health < 0:
            expl_deathath = EXPLOSIOM(player.rect.center, 'ship_die')
            all_sprites.add(expl_deathath)
            random.choice(expl_sounds).play()
            player.lives -= 1
            player.health = 100
            player.gun_level = 1
            player.hide()
            #running =  False
    hit_play_power = pygame.sprite.spritecollide(player, powers, True)
    for hit in hit_play_power:
        if hit.type == 'shield':
            power_sounds[0].play()
            player.health += 30
            if player.health > 100 :
                player.health = 100
        elif hit.type == 'gun' and player.gun_level < 6:
            power_sounds[1].play()
            player.gun_level +=1
            player.gun_power_time = pygame.time.get_ticks()
    if player.lives == 0 and not(expl_deathath.alive()):
        init_screen = True

    #畫面顯示
    screen.fill((WHITE))
    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    draw_text(screen, str(score) , 18, WHITE, WIDTH/2, 10)
    draw_health(screen, player.health, 5, 10,)
    draw_live(screen, player.lives, ship_img_lives, WIDTH-100, 10)
    pygame.display.update()
    

pygame.quit()