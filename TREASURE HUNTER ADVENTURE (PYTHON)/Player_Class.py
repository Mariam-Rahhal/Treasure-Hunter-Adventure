import pygame
WINDOW_WIDTH  = 800   #how wide the game window is in pixels
WINDOW_HEIGHT = 600   # how tall the game window is in pixels
class Player:
    def __init__(self):                                     
        self.x = WINDOW_WIDTH  // 2  # starting X position: centre of the window
        self.y = WINDOW_HEIGHT // 2  # starting Y position: centre of the window
        self.width  = 40 # player image width in pixels
        self.height = 40 # player image height in pixels
        self.speed  = 3  # how many pixels the player moves per frame
        self.score  = 0   
        self.health = 100 
        self.image  = pygame.image.load("img/character.jpeg") # load the player image from disk
        self.image  = pygame.transform.scale(self.image, (self.width, self.height))  # resize it to 40x40

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))  # draw the image at specific position on the screen

    def move(self):
        keys = pygame.key.get_pressed()       
        if keys[pygame.K_UP]:
            self.y -= self.speed  
        if keys[pygame.K_DOWN]:
            self.y += self.speed              
        if keys[pygame.K_LEFT]:
            self.x -= self.speed              
        if keys[pygame.K_RIGHT]:
            self.x += self.speed          
            
               
        if self.x < 0:                             # went off the left edge
            self.x = 0                            
        if self.x > WINDOW_WIDTH - self.width:     # went off the right edge
            self.x = WINDOW_WIDTH - self.width     
        if self.y < 0:                             # went off the top edge
            self.y = 0                             
        if self.y > WINDOW_HEIGHT - self.height:   # went off the bottom edge
            self.y = WINDOW_HEIGHT - self.height  

