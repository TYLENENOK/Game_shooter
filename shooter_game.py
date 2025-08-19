#Хороший шутер

from pygame import *
from random import randint
font.init()
mixer.init()

win = display.set_mode((700,500))
display.set_caption('Шутер')

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_speed,width,height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width,height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        win.blit(self.image, (self.rect.x,self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 695:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -10, 10,10)
        bullets.add(bullet)

lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 495:
            self.rect.y = 0
            self.rect.x = randint(65,645)
            lost += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
    
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 495:
            self.rect.y = 0
            self.rect.x = randint(65,645)


background = transform.scale(image.load('galaxy.jpg'), (700,500))

score = 0
hp = 3

font1 = font.SysFont('Arial', 32)
lose_text = font1.render('Пропущено: ' + str(lost), 1, (255,255,255))
score_text = font1.render('Счет: ' + str(score), 1, (255,255,255))
font2 = font.SysFont('Arial', 64)
win_text = font2.render('YOU WIN', 1, (0,255,0))
lose = font2.render('YOU LOSE', 1, (255,0,0))
hp_text = font2.render('Жизни: ' + str(hp), 1, (255,255,255))

asteroids = sprite.Group()
for i in range(3):
    asteroid_1 = Asteroid('asteroid.png',randint(65,645), 0, randint(2,4), 80,50)
    asteroids.add(asteroid_1)
ship = Player('rocket.png', 320, 400, 12, 65,65)
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(65, 645), 0, randint(2,6), 80,50)
    monsters.add(monster)

#mixer.music.load('space.ogg')
#mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


FPS = 60
finish = False
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
                fire_sound.play()
    if not finish:
        win.blit(background, (0,0))
        ship.reset()
        ship.update()
        monsters.draw(win)
        monsters.update()
        bullets.update()
        bullets.draw(win)
        asteroids.update()
        asteroids.draw(win)
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        if sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, asteroids, True)
            hp -= 1
        for s in sprites_list:
            score += 1
            monster = Enemy('ufo.png', randint(65, 645), 0, randint(2,6), 80,50)
            monsters.add(monster)
        if score >= 30:
            finish = True
            win.blit(win_text, (250,220))
        if lost >= 3 or hp <= 0 or sprite.spritecollide(ship, monsters, False):
            finish = True
            win.blit(lose ,(250, 220))
        lose_text = font1.render('Пропущено: ' + str(lost), 1, (255,255,255))
        score_text = font1.render('Счет: ' + str(score), 1, (255,255,255))
        hp_text = font2.render('Жизни: ' + str(hp), 1, (255,255,255))
        win.blit(hp_text, (470,10))
        win.blit(lose_text, (30,30))
        win.blit(score_text, (30,60))
        display.update()
    time.delay(FPS)
