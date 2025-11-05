
import pygame
import random
import math
from pygame import mixer

pygame.init()

background = pygame.image.load(r'resources\background.png')
scaled_background = pygame.transform.scale(background, (800, 600))

explosion_img = pygame.image.load(r'resources\explosion.png')
explosion_img = pygame.transform.scale(explosion_img, (64, 64))

mixer.music.load(r'resources\background.wav')
mixer.music.play(-1)

score_font = pygame.font.Font('freesansbold.ttf', 32)
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Spam Invaders")
pygame_icon = pygame.image.load(r'resources\alien.png')
pygame.display.set_icon(pygame_icon)

class Button:
    def __init__(self, x, y, img, scale):
        self.x = x
        self.y = y
        self.img = img
        self.rect = self.img.get_rect()
        self.scale = scale

    def draw(self):
        pos = pygame.mouse.get_pos()
        print(pos)
        if self.rect.collidepoint(pos):
            print("Hover")
        screen.blit(self.img, (self.x, self.y))

class Bullet:
    def __init__(self, x=0, y=0, change=-1):
        self.state = "ready"
        self.x = x
        self.y = y
        self.change = change
        img = pygame.image.load(r'resources\bullet.jpg')
        self.img = pygame.transform.scale(img, (32, 32))
    
    def shoot(self):
        self.change = -1
        screen.blit(self.img, (self.x,self.y))

    def move(self):
        self.y += self.change
        if self.y <= 0:
            self.state = "ready"

class Player:
    def __init__(self, x, change=0):
        img = pygame.image.load(r'resources\spaceship.webp')
        self.img = pygame.transform.scale(img, (64, 80))  # Scale the image to fit the screen 
        self.x = x
        self.y = 530
        self.change = change
        self.score = 0

    def player_set(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.x += self.change
        if self.x <= 0:
            self.x = 0
        if self.x >= 736:
            self.x = 736



class Enemy:
    def __init__(self, x, y):
        img = pygame.image.load(r'resources\alien.png')
        self.img = pygame.transform.scale(img, (64, 64))  # Scale the image to fit the screen 
        self.img = pygame.transform.flip(self.img, True, False)  # Scale the image to fit the screen 
        self.x = x
        self.y = y
        self.x_change = 0.2
        self.y_change = 20
        self.exploding = False
        self.explode_start = 0
        self.orig_img = self.img

    def enemy_set(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        # don't move while exploding (added)
        if self.exploding:
            return
        self.x += self.x_change
        if self.x <= 0:
            self.x_change = .2
            self.y += self.y_change
            self.img = pygame.transform.flip(self.img, True, False)  # Scale the image to fit the screen 
        if self.x >= 736:
            self.x_change = -.2
            self.y += self.y_change
            self.img = pygame.transform.flip(self.img, True, False)  # Scale the image to fit the screen 

    def is_hit(self, bullet):
        distance = math.sqrt((self.x - bullet.x)**2 + (self.y - bullet.y)**2)
        if distance < 48:
            return True
        return False
    
    def lose(self):
        if self.y >= 440:
            return True
        return False
    
    def start_explosion(self):
        self.exploding = True
        self.explode_start = pygame.time.get_ticks()
        self.img = explosion_img

    def explosion_done(self):
        return self.exploding and (pygame.time.get_ticks() - self.explode_start) >= 500


enemies = []
enemy_count = 6
player = Player(370)
bullet = Bullet()
for i in range(enemy_count):
    enemy = Enemy(random.randint(0, 800-64), random.randint(0, 300-64))
    enemies.append(enemy)

game_over_font = pygame.font.Font('freesansbold.ttf', 64)
game_over_text = game_over_font.render("GAME OVER", True, (0, 0, 0))
game_over = False
running = True
restart_img = pygame.image.load('resources\start.png')
restart_img = pygame.transform.scale(restart_img, (300, 100))
while running:
    screen.fill((0,0,0))
    screen.blit(scaled_background, (0, 0))
    score_display = score_font.render(f"Score: {player.score}", True, (255, 255, 255))
    screen.blit(score_display, (10, 10))
    #Loops
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_LEFT]:
                player.change = -0.3
            if keys[pygame.K_RIGHT]:
                player.change = 0.3
            if keys[pygame.K_z]:
                if bullet.state == "ready":
                    mixer.Sound(r'resources\laser.wav').play()
                    bullet.x = player.x + 16
                    bullet.y = player.y +10
                    bullet.state = "fire"
                    

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.change = 0

   
    #Changes
    player.move()
    for enemy in enemies:
        enemy.move()
        if enemy.lose():
            enemies = []
            game_over = True
    bullet.move()

    for i, enemy in enumerate(enemies):
        if enemy.is_hit(bullet):
            enemy = Enemy(random.randint(0, 800-64), random.randint(0, 300-64))
            #explode
            bullet.state = "ready"
            bullet.x = player.x
            bullet.y = player.y
            bullet.change = 0
            player.score  += 1
            mixer.Sound(r'resources\explosion.wav').play()
            enemies.pop(i)

            if enemies == []:
                for j in range(enemy_count + 1):
                    new_enemy = Enemy(random.randint(0, 800-64), random.randint(0, 300-64))
                    enemies.append(new_enemy)
            
            if enemy.is_hit(bullet) and not enemy.exploding:
             enemy.start_explosion()
             mixer.Sound(r'resources\explosion.wav').play()
             bullet.state = "ready"
             bullet.x = player.x
             bullet.y = player.y
             bullet.change = 0
             player.score  += 1

            for idx in range(len(enemies)-1, -1, -1):
             if enemies[idx].explosion_done():
                 enemies.pop(idx)
                 new_enemy = Enemy(random.randint(0, 800-64), random.randint(0, 300-64))
                 enemies.append(new_enemy)


     #Show Items
    player.player_set()
    for enemy in enemies:
        enemy.enemy_set()
    bullet.shoot()
    
    if game_over:
        screen.blit(game_over_text, (200, 250))

        button = Button(250, 370, restart_img, 0)
        button.draw()


    
    pygame.display.flip()