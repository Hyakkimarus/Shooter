#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as timer

font.init()
font1 = font.SysFont('Arial', 80)
font2 = font.SysFont('Arial', 36)
win = font1.render('YOU WIN!', 1, (255, 255, 255))
lose = font1.render("YOU LOSE!", 1, (180, 0, 0))

img_back = "galaxy.jpg" # фон игры
img_hero = "rocket.png" # герой
img_enemy = "ufo.png" # враг
img_bullet ="bullet.png"
score = 0 #сбито кораблей
lost = 0 #пропущено кораблей
max_lost = 3
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, height, widht, koord_x, koord_y, speed):
        super().__init__()
        self.widht = height
        self.height = widht
        self.image = transform.scale(image.load(player_image), (50,50))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = koord_x
        self.rect.y = koord_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def collidepoint(self):
        return self.rect.collidepoint(x,y)

    def colliderect(self):
        return self.rect.colliderect(rect)

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet,15 ,20 , self.rect.x, self.rect.top, -15)
        bullets.add(bullet)
        
class Enemy(GameSprite):
   def update(self):
       self.rect.y += self.speed
       global lost
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
#class Label():
#    def __init__(self, x=0, y=0, width=10, height=10):
#        self.rect = pygame.Rect(x, y, width, height)
#    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
#        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)
#
#    def draw(self, shift_x=0, shift_y=0):
#        self.fill()
#        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

rocket = Player(img_hero, 350, 100,5 ,win_height -  100, 10)

monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, 80, 50,randint(80, win_width - 80) , -40, randint(1, 5))
   monsters.add(monster)

bullets = sprite.Group()

game = True

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

#time_text = Label(50, 150, 10, 10 )
#time_text.set_text('ВЫ ПРОИГРАЛИ!!', 60, (255,0,0))
#time_text.draw(10,10)

finish = False
run = True 
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                rocket.fire()
    if not finish:
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, 80,50,randint(80, win_width - 80), -40,   randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(rocket, monsters, False) or lost >= max_lost:
            window.blit(lose,(200, 200))
            finish = True 
            




        window.blit(background,(0,0))
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        rocket.update()
        monsters.update()
        rocket.reset()
        monsters.draw(window)
        bullets.draw(window)
        bullets.update()
        display.update()
       
    time.delay(50)
