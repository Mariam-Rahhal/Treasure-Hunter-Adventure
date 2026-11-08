import pygame
import random

MARGIN = 95
WINDOW_WIDTH  = 800
WINDOW_HEIGHT = 600


class Treasure:
    
    def __init__(self):
        self.size  = 24  # treasure square is 24x24 pixels
        self.value = 10  # collecting one treasure adds 10 points
        self.x = random.randint(MARGIN, WINDOW_WIDTH - self.size - MARGIN)  # random X position inside the window
        self.y = random.randint(MARGIN, WINDOW_HEIGHT - self.size - MARGIN)  # random Y position inside the window
        flowers = ["img/f1.jpeg","img/f2.jpeg","img/f3.jpeg",] # the list of flowers
        
        
        self.image = pygame.image.load(random.choice(flowers)) # load a random flower image
        self.image = pygame.transform.scale(self.image, (self.size, self.size)) # resize it to 24x24

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))  # draw the treasure image on the screen

