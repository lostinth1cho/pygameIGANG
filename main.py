'''
https://github.com/lostinth1cho/pygameIGANG
todo-list:
顯示版本代號
調整開始畫面
計時器會在畫面最上方移動
'''
import pygame
import random
import os
import time

patch = "patch:230513"
FPS = 50
WIDTH = 800
HEIGHT = 600
timer_height = 10
timer_width = 10
SPEED_Y = 5
debug = True
gravity = 0.98
XspeedL_low = 4
XspeedL_high = 6
speed_of_timer = WIDTH / (FPS*10)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (160, 32, 240)
BLUE = (0, 0, 255)
color_list = [BLACK, GREEN, RED, PURPLE, BLUE]

pygame.init()   
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("igang igang dog dou bu dang")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')
font = pygame.font.Font(font_name, 25)

#載入圖片
BackGround_img = pygame.image.load(os.path.join("img", "BackGround.png")).convert()
player_img = pygame.image.load(os.path.join("img", "igang.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
pygame.display.set_icon(player_mini_img)
# ball_img = pygame.image.load(os.path.join("img", "ball.png")).convert()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 48))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 25
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT -10
        self.speedx = 10

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

class Rock(pygame.sprite.Sprite):
    def __init__(self, direction):
        pygame.sprite.Sprite.__init__(self)
        ball_size = random.randint(50, 100)
        self.image = pygame.Surface((ball_size, ball_size))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 1.0 / 2
        color = random.choice(color_list)
        pygame.draw.circle(self.image, color, self.rect.center, self.radius)
        self.rect.x = random.randrange(-100, 0) if direction == "left" else random.randrange(WIDTH, WIDTH+100)
        self.rect.y = random.randrange(HEIGHT-400, HEIGHT-200)
        self.maxHigh = self.rect.top
        #self.speedy = random.randint(5, 6)
        self.speedy = SPEED_Y
        self.speedx = random.randint(XspeedL_low, XspeedL_high) if direction == 'left' else random.randint(-1*XspeedL_high, -1*XspeedL_low)
        self.reset(direction)

    def reset(self, direction):
        ball_size = random.randint(40, 100)
        self.image = pygame.Surface((ball_size, ball_size))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 1.0 / 2
        color = random.choice(color_list)
        pygame.draw.circle(self.image, color, self.rect.center, self.radius)
        if direction == 'left':
            self.rect.x = random.randint(-100, 0)
            self.speedx = random.randint(XspeedL_low, XspeedL_high)
        else:
            self.rect.x = random.randint(WIDTH, WIDTH + 100)
            random.randint(-1*XspeedL_high, -1*XspeedL_low)
        self.rect.y = random.randint(HEIGHT - 400, HEIGHT - 200)
        self.speedy = random.randrange(5, 10)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        self.speedy += gravity
        if self.rect.bottom >= HEIGHT :
            self.speedy *= -0.98
        if self.rect.left > WIDTH+100 or self.rect.right < -100:
            self.reset('left' if self.speedx > 0 else 'right')
'''
class clock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((timer_height, timer_width))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x = (self.rect.x + speed_of_timer) % WIDTH'''

def generate_ball(n):
    klr = random.randint(1, n)
    krl = random.randint(1, n)
    for i in range(klr):
        lr = Rock("left")
    all_sprites.add(lr)
    for i in range(krl):
        rl = Rock("Right")
    all_sprites.add(rl)
    rocks.add(lr)
    rocks.add(rl)

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def draw_init(out):
    screen.blit(BackGround_img, (0, 0))
    draw_text(screen, 'igang igang dog dou bu dang', 64, WIDTH/2, HEIGHT/4-60)
    draw_text(screen, 'your : '+out, 40, WIDTH/2, 350)
    draw_text(screen, 'press ← → to move Kryst4l', 18, WIDTH/2, 545)
    draw_text(screen, 'press ↑ to start', 18, WIDTH/2, 565)
    draw_text(screen, patch, 15, 45, 575)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            else :
                key_pressed = pygame.key.get_pressed()
                if key_pressed[pygame.K_UP]:
                    waiting = False
                    return pygame.time.get_ticks()

all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
generate_ball(1)

show_init = True
start_ticks = pygame.time.get_ticks()
timer_x = 0
running = True
result = ""
out = "0.0"
while running:
    BackGround_img = pygame.transform.scale(BackGround_img, (WIDTH, HEIGHT))
    if show_init:
        start_ticks = draw_init(out)
        if start_ticks == False:
            break
        show_init = False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        timer_x = 0
        generate_ball(1)
    now_ticks=pygame.time.get_ticks()
    
    ticks = now_ticks - start_ticks
    #ticks=pygame.time.get_ticks()
    
    millis=ticks%1000
    seconds=int(ticks/1000 )
    minutes=int(ticks/60000 % 24)
    if ticks % 250 == 0:
        generate_ball(1)
    out='{seconds}.{millis}'.format( millis=millis//10, seconds=seconds)
    result = out
    timer_x = (timer_x + speed_of_timer) % WIDTH
    draw_text(screen, out, 25, timer_x, 60)
    pygame.display.flip()
    clock.tick(FPS)

    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #更新遊戲
    all_sprites.update()

    hits = pygame.sprite.spritecollide(player, rocks, False, pygame.sprite.collide_circle)
    if (hits and debug):
        show_init = True

    #畫面顯示
    screen.fill(BLACK)
    screen.blit(BackGround_img, (0, 0))
    all_sprites.draw(screen)
    pygame.display.update()

'''running = True
out = "Score:" + out
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False
    if not running :
        break
    font.render_to(screen, (100, 100), out, pygame.Color('black'))
    pygame.display.flip()
    pygame.display.update()'''


pygame.quit()