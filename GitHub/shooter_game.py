#Создаю собственный Шутер!

from pygame import *
from random import randint
from time import time as timer


font.init()
font2 = font.SysFont('Arial', 36)

back = 'galaxy.jpg'
plr = 'rocket.png'
enm = 'ufo.png'
enm2 = 'monster.png'
pyl = 'bullet.png'
boss1 = 'BOSS.png'
j = 'jizn.png'

score = 0
lost = 0
bosss = 0
bosssj = 10
score2 = 0


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed,x_size,y_size):
        super().__init__()

        self.image = transform.scale(image.load(player_image),(x_size,y_size))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):
        win.blit(self.image, (self.rect.x,self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        pyla = pyla_strelya(pyl,self.rect.centerx, self.rect.top,15,20,25)
        pylii.add(pyla)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_width:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

    




class pyla_strelya(GameSprite):
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y > win_width:
            self.rect.x = randint(80, win_width - 80)
            self.kill()

class boss(GameSprite):
    direct = "right"
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_width:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

font = font.SysFont('Times New Roman', 70)
lose = font.render('YOU LOSE!!!!',True,(200, 58, 0))


win_width = 700
win_height = 500

clock = time.Clock() 
FPS = 60

win = display.set_mode((win_width,win_height))
display.set_caption('GALAXY')
background = transform.scale(image.load(back),(win_width, win_height))



player = Player(plr, 5, win_height - 90 , 10,65,85)



jizn2 = GameSprite(j,570, win_height-500,60,65,65)
bossgroup = sprite.Group()
monsters1 = sprite.Group()
for i in range(1,5):
    monster1 = Enemy(enm,randint(80,win_width-80), - 40,randint(1,5),80,50)
    monsters1.add(monster1)


monsters2 = sprite.Group()
for i in range(1,3):
    monster2 = Enemy(enm2,randint(80,win_width-80), - 40,randint(1,5),50,50)
    monsters2.add(monster2)

for i in range(1,2):
    boss = boss(boss1,randint(130,win_width-80), - 40,1,200,200)
    bossgroup.add(boss)

pylii = sprite.Group()
pylii2 = sprite.Group()

finish = False
game = True

rel_time = False
num_fire = 0
gg = 5

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 31 and rel_time == False:
                    num_fire += 1
                    player.fire()
                
                if num_fire >= 31 and rel_time == False:
                    last_time = timer()
                    rel_time = True


    if not finish:
        win.blit(background,(0,0))

        player.update()
        player.reset()

        text = font2.render('СЧЁТ: ' + str(score),1,(255,255,255))
        win.blit(text,(10,20))

        text_lose = font2.render('ПРОПУЩЕНО: ' + str(lost),1,(255,255,255))
        win.blit(text_lose,(10,50))


        
        gj = font2.render(str(gg),1,(255,255,255))
        win.blit(gj,(650,20))



        
        monsters2.update()
        monsters2.draw(win)


        

        monsters1.update()
        monsters1.draw(win)
        pylii.update()
        pylii.draw(win) 
        jizn2.reset()

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 2:
                op_p = font2.render('ПЕРЕЗАРЯДКА...',1,(255,0,0))
                win.blit(op_p,(260,460))
            else:
                num_fire = 0
                rel_time = False








        s_l = sprite.groupcollide(monsters1,pylii,True,True)
        for c in s_l:
            score += 1
            score2 += 1

            monster1 = Enemy(enm,randint(80,win_width-80), - 40,randint(1,5),80,50)
            monsters1.add(monster1)


        s_l = sprite.groupcollide(bossgroup,pylii,False,True)
        for c in s_l:
            bosssj -= 1

        if bosssj == 0:
            bosssj = 10
            bosss = 0
            boss.kill()





        s_l2 = sprite.groupcollide(monsters2,pylii,True,True)
        for c1 in s_l2:
            score += 1
            score2 += 1

            monster2 = Enemy(enm2,randint(80,win_width-80), - 40,randint(1,5),50,50)
            monsters2.add(monster2)

        if sprite.spritecollide(player, monsters1, False) or sprite.spritecollide(player, monsters2, False):
            sprite.spritecollide(player, monsters1, True)
            sprite.spritecollide(player, monsters2, True)
            gg -= 1
            monster1 = Enemy(enm,randint(80,win_width-80), - 40,randint(1,5),80,50)
            monsters1.add(monster1)
            monster2 = Enemy(enm2,randint(80,win_width-80), - 40,randint(1,5),50,50)
            monsters2.add(monster2)





        if lost >= 5 or gg == 0:
            finish = True
            win.blit(lose,(200,200))

        

        if score2 == 10:
            bosss = 1
            score2 = 0

        if bosss == 1:
            bossgroup.draw(win)
            bossgroup.update()
        display.update()

        

    time.delay(30)
                        
                        
