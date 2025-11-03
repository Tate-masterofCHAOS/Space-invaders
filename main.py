
import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Invaders")
pygame_icon = pygame.image.load(r'resources\alien.png')
pygame.display.set_icon(pygame_icon)

class Bullet:
    def __init__(self, x=0, y=0):
        self.state = "ready"
        self.x = x
        self.y = y
        self.change = -1
        img = pygame.image.load(r'resources\bullet.jpg')
        self.img = pygame.transform.scale(img, (32, 32))
    
    def shoot(self):
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

    def enemy_set(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.x += self.x_change
        if self.x <= 0:
            self.x_change = 0.2
            self.y += self.y_change
            self.img = pygame.transform.flip(self.img, True, False)  # Scale the image to fit the screen 
        if self.x >= 736:
            self.x_change = -0.2
            self.y += self.y_change
            self.img = pygame.transform.flip(self.img, True, False)  # Scale the image to fit the screen 

    def is_hit(self, bullet):
        distance = math.sqrt((self.x - bullet.x)**2 + (self.y - bullet.y)**2)
        if distance < 27:
            pass


player = Player(370)
enemy = Enemy(random.randint(0, 800-64), random.randint(0, 300-64))
bullet = Bullet()


running = True
while running:
    screen.fill((0,0,0))
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
                    bullet.x = player.x + 16
                    bullet.y = player.y +10
                    bullet.state = "fire"
                    

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.change == 0

   
    #Changes
    player.move()
    enemy.move()
    bullet.move()
     #Show Items
    player.player_set()
    enemy.enemy_set()
    bullet.shoot()
    

    
    pygame.display.flip()