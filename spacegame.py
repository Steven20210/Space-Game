# This is Steven's Space Game

# Import all of the libraries that are necessary
import pygame as pg
import time
import random
from pygame import mixer
from settings import *
from os import path

# Loading all of the folders that are needed
img_dir = path.join(path.dirname(__file__), 'images')
snd_dir = path.join(path.dirname(__file__), 'sound')

# This is to initialize some of the libraries that are needed and also initalizes the screen and import time.
pg.init()
mixer.init()
pg.mixer.init() # This initializes the sound within the game
screen = pg.display.set_mode((WIDTH, HEIGHT)) # this initalizes the display of the window
pg.display.set_caption("Steven's Space Game") # this sets the name of the window
clock = pg.time.Clock # This help to import time into the game

font_name = pg.font.match_font('arial')


def draw_text(surf, text, size, x, y): # This allows me to draw my text onto the screen
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_shield_bar(surf, x, y, pct): # This function allows me to draw the shield bar onto the screen
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct/100) * BAR_LENGTH
    outline_rect = pg.Rect(x,y, fill, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, GREEN, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


# The new mob function allows me to make a new mob so that when one dies then a new one can respawn
def newmob():
    m = Mob()
    all_sprites.add(m)
    mob.add(m)


# classes
class Player(pg.sprite.Sprite):
    def __init__(self): # This function allows me to initialize all of the attributes that are associated with player
        pg.sprite.Sprite.__init__(self)
        self.image = resource.player_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pg.time.get_ticks()
        self.power = 1
        self.power_time = pg.time.get_ticks()
        self.score = 0
        self.highscore = 0


    def update(self):
        if self.power >= 2 and pg.time.get_ticks() - self.power_time > POWERUP_TIME:
            # This 'if' statement allows to record the amount of time passed until the amount of bullets that the spaceship is shooting should go down
            self.power -= 1
            self.power_time = pg.time.get_ticks()
        self.speedy = 0
        self.speedx = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]: # These statements below allow for the movement of the spaceship
            self.speedx = -8
        if keystate[pg.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if keystate[pg.K_UP]: # Extension
            self.speedy = -8
        if keystate[pg.K_DOWN]: # Extension
            self.speedy = 8
        if keystate[pg.K_SPACE]:
            self.shoot()
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


    def powerup(self): # This function starts the timer and updates self.power
        self.power += 1
        self.power_time = pg.time.get_ticks()

    def shoot(self): # This allows for player to shoot the bullets
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
            if self.power == 3: #Extension
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                bullet3 = Bullet(self.rect.centerx, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
            if self.power > 3: # Extension
                self.power = 3


class Mob(pg.sprite.Sprite):
    def __init__(self): # initializes mob attributes
        pg.sprite.Sprite.__init__(self)
        self.image = resource.mob_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3,3)

    def update(self): # This method allows for the movement of the mob
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH +20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pg.sprite.Sprite): # The creation of a bullet
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.image = resource.laser_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -40
    def update(self):# Movement of the bullet
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Pow(pg.sprite.Sprite): # creation of a powerup
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(['star', 'gun'])
        if random.random() > 0.8: # Extension
            self.type = random.choice(['op', 'star', 'gun']) # Extension
        self.image = resource.powerup[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


class Screen: # The creation of the screen object

    def load_data(self): # Extension
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, "HS_FILE.txt"), 'r') as f:
            try:
                player.highscore = int(f.read())
            except:
                player.highscore = 0

    def show_go_screen(self):
        screen.blit(resource.background,resource.background_rect)
        draw_text(screen, "Space Game", 56, WIDTH/ 2, HEIGHT/4)
        draw_text(screen, "Arrow Keys move, Space to fire", 22, WIDTH/ 2, HEIGHT/2)
        draw_text(screen, "Press y(yes) or n(no) to play", 10, WIDTH/2, HEIGHT *3/4) # Extension
        self.load_data()
        if player.score > player.highscore: # Extension
            player.highscore = player.score
            draw_text(screen, "NEW HIGH SCORE!! = " + str(player.highscore), 22, WIDTH/2, 10 )
            with open(path.join(self.dir, "HS_FILE.txt"), 'w') as f:
                f.write(str(player.score))
        else:
                draw_text(screen, "High Score:" + str(player.highscore), 22, WIDTH / 2, 15)
                draw_text(screen, "Current Score: " + str(player.score), 15, WIDTH / 2, 45)

        keystate = pg.key.get_pressed()
        pg.display.flip()
        waiting = True
        while waiting:
            time.sleep(0.05)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    keystate = pg.key.get_pressed() # Extension
                if keystate[pg.K_y]:
                    waiting = False
                if keystate[pg.K_n]:
                    pg.quit()

class Resource: # Extension
    def __init__(self):
        self.background = pg.image.load(path.join(img_dir, "black.png")).convert()
        self.background_rect = self.background.get_rect()

        self.player_img1 = pg.image.load(path.join(img_dir,"smiling-emoji.png")).convert()
        self.player_img = pg.image.load(path.join(img_dir,"eating-emoji.png")).convert()

        self.mob_img = pg.image.load(path.join(img_dir, "report_card.jpg")).convert()

        self.laser_img = pg.image.load(path.join(img_dir, "sprite_0.png")).convert()

        self.rip_sound = pg.mixer.Sound(path.join(snd_dir, 'rip.wav'))
        pg.mixer.music.load(path.join(snd_dir, 'game.ogg'))
        pg.mixer.music.set_volume(0.4)

        self.powerup = {}
        self.powerup['gun'] = pg.image.load(path.join(img_dir, 'bolt_gold.png'))
        self.powerup['star'] = pg.image.load(path.join(img_dir, "star.png")).convert()
        self.powerup['op'] = pg.image.load(path.join(img_dir, "op.png"))

resource = Resource()


all_sprites = pg.sprite.Group() # This variable helps to define all of the functions within the sprite group aka the tab that has the title Sprites
player = Player() #This helps to initalize a reference to the class
mob = pg.sprite.Group()
powerups = pg.sprite.Group()
bullets = pg.sprite.Group()
all_sprites.add(player)# This is used to add the player class to the sprites group

n = 8
for i in range(n):
    newmob()

player.score = 0

# Game loop
game_over = True
running = True
while running:
    if game_over:
        my_screen = Screen()
        my_screen.show_go_screen()
        game_over = False
        all_sprites = pg.sprite.Group()  # This variable helps to define all of the functions within the sprite group aka the tab that has the title Sprites
        player = Player()  # This helps to initalize a reference to the class
        mob = pg.sprite.Group()
        powerups = pg.sprite.Group()
        bullets = pg.sprite.Group()
        all_sprites.add(player)  # This is used to add the player class to the sprites group

        n = 8
        for i in range(n):
            newmob()

        player.score = 0
        pg.mixer.music.play(loops=-1) # Extension

    # keep loop running at the right speed
    time.sleep(0.05) # this is a delay function within python
    # Process input (events)
    for event in pg.event.get():
        # check for closing window
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.image = resource.player_img # Extension
                player.shoot()
        elif event.type == pg.KEYUP:
            player.image = resource.player_img1 # Extension
    # Update
    all_sprites.update()
    hits = pg.sprite.groupcollide(mob, bullets, True, True)

    for hit in hits:
        resource.rip_sound.play()
        player.score += 50
        if player.score > 500 and player.score < 650: # Extension
            for i in range(20):
                newmob()
        if player.score > 10000 and player.score < 10150: # Extension
            for i in range(30):
                newmob()
        if random.random() >0.9:
            p = Pow(hit.rect.center)
            all_sprites.add(p)
            powerups.add(p)
        newmob()


    # Check to see if a mob hit the player
    hits = pg.sprite.spritecollide(player, mob, True)
    for hit in hits:
        player.shield -= 20
        newmob()
        if player.shield <= 0:
            game_over = True

    # Check if the player hit a powerup
    hits = pg.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'star':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()
        if hit.type == 'op': # Extension
            for i in mob:
                i.kill()
                newmob()



    # Draw / render
    screen.fill(BLACK)
    screen.blit(resource.background, resource.background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(player.score), 18,WIDTH/2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    # *after* drawing everything, flip the display
    pg.display.flip()

pg.quit()