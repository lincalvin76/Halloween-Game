from typing import Any
import pygame
pygame.init()

import random

from pygame.locals import(
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

height = 800
width = 800

font = pygame.font.Font('freesansbold.ttf', 32)
score_val = 0

def addScore():
    global score_val
    score_val += 1

def showScore():
        score = font.render("Score: "+ str(score_val),True, (255,255,255))
        screen.blit(score, (0,0))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.surf = pygame.image.load("bucket.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -6)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 6)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-6, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(6, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.top <= 550:
            self.rect.top = 550
        if self.rect.bottom >= height:
            self.rect.bottom = height

class Candy(pygame.sprite.Sprite):
    def __init__(self):
        super(Candy, self).__init__()
        self.surf = pygame.image.load("candy.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, width),
                random.randint(0, height - 700),
            )
        )
        self.speed = random.randint(3,5)

    def update(self):
        self.rect.move_ip(0, + self.speed)
        if self.rect.colliderect(player):
            addScore()
            self.kill()
        elif self.rect.top < 0:
            self.kill()
 

class Ghost(pygame.sprite.Sprite):
    def __init__(self):
        super(Ghost, self).__init__()
        self.surf = pygame.image.load("ghost.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(width + 20, width + 100),
                random.randint(height - 250, height),
            )
        )
        self.speed = random.randint(1,1)


    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

screen = pygame.display.set_mode([height,width])

ADDCANDY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDCANDY, 700)
ADDGHOST = pygame.USEREVENT + 2
pygame.time.set_timer(ADDGHOST, 1000)

player = Player()

candy = pygame.sprite.Group()
ghost = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN: 
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

        elif event.type == ADDCANDY:
            new_candy = Candy()
            candy.add(new_candy)
            all_sprites.add(new_candy)

        elif event.type == ADDGHOST:
            new_ghost = Ghost()
            ghost.add(new_ghost)
            all_sprites.add(new_ghost)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    candy.update()
    ghost.update()
    

    screen.fill((0,0,0))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)


    if pygame.sprite.spritecollideany(player,ghost):
        player.kill()
        running = False
    
    showScore()
    pygame.display.flip()

    clock.tick(60)

pygame.quit()