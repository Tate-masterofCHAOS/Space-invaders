
import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Invades")
pygame_icon = pygame.image.load(r'resources\alien.png')
pygame.display.set_icon(pygame_icon)


class Player:
    def __init__(self, x, change=0):
        img = pygame.image.load('resources\spaceship.jpg')
        self.img = pygame.transform.scale(img, (64, 64))  # Scale the image to fit the screen 
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
    def __init__(self, x, change=0):
        img = pygame.image.load(r'resources\alien.png')
        self.img = pygame.transform.scale(img, (64, 64))  # Scale the image to fit the screen 


player = Player(370)

running = True
while running:

    #Loops
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_LEFT]:
                player.change = -0.2
            if keys[pygame.K_RIGHT]:
                player.change = 0.2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.change == 0

    #Show Items
    screen.fill((0,0,0))
    player.move()
    player.player_set()
    
    

    
    pygame.display.flip()