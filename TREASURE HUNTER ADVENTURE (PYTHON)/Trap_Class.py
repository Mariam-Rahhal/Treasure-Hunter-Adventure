
import pygame
import random

MARGIN = 95  # set the bound of the flowers
WINDOW_WIDTH  = 800   # how wide the game window is in pixels
WINDOW_HEIGHT = 600   # how tall the game window is in pixels

class Trap:
    def __init__(self):
        self.size = 28   # trap square is 28x28 pixels
        self.damage = 20   # touching a trap removes 20 health
        self.x = random.randint(MARGIN, WINDOW_WIDTH - self.size - MARGIN)  # random starting X position
        self.y = random.randint(MARGIN, WINDOW_HEIGHT - self.size - MARGIN)  # random starting Y position
        
        self.hit = False                
        self.last_move = pygame.time.get_ticks() # records the time the trap last moved (in ms)
        self.image = pygame.image.load("img/f_no.jpeg")  # load the trap image from disk
        self.image = pygame.transform.scale(self.image, (self.size, self.size))  # resize it to 28x28

    def update(self):
        if pygame.time.get_ticks() - self.last_move > 2000:  # if 2 seconds passed
            self.x = random.randint(MARGIN, WINDOW_WIDTH - self.size - MARGIN)  # move to new random X
            self.y = random.randint(MARGIN, WINDOW_HEIGHT - self.size - MARGIN)  # move to new random Y
            self.hit = False                   # reset hit
            self.last_move = pygame.time.get_ticks() # save current time


    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))  # draw the trap image on the screen
        
        