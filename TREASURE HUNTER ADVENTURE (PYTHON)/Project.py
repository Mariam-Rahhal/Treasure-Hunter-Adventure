import pandas as pd   
import pygame         
import random        
import csv           
from datetime import date  

from Player_Class import Player
from Trap_Class import Trap
from Treasure_Class import Treasure

MARGIN = 95 # set the bound of the flowers 
game_started = False
WINDOW_WIDTH  = 800   # how wide the game window is in pixels
WINDOW_HEIGHT = 600   # how tall the game window is in pixels
WINDOW_TITLE  = "Flower Girl Adventure"  # the text shown in the title bar
GAME_DURATION = 60                           
SCORES_FILE   = "scores.csv" # the file where all scores are saved


def main():
    player_name = input("Enter your name: ").strip()  # strip() removes the spaces at the beginning and at the end

    player_name = player_name.replace(",", "") # cuz we save data in scores.csv separated by comma , if the user enter a name with comma it will understand that the name separated by comma is 2 lines so will give an error
    if player_name == "":        
        player_name = "Player1"  

    pygame.init() 
    pygame.mixer.init() # it allows us to add sounds for the game
    pygame.mixer.music.load("rec/game.mp3")
    pygame.mixer.music.set_volume(0.5) #  set the level of the volume
    pygame.mixer.music.play(-1) # when the sound finishes repeat it
    
    clock  = pygame.time.Clock()  # clock controls how we go from one frame to another same as for object 
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # create the game window
    pygame.display.set_caption(WINDOW_TITLE) # set the text in the title bar
    
    background   = pygame.image.load("img/background.jpeg") # load the background image from disk
    background   = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT)) # resize it to fit the window
    
    game_over_bg = pygame.image.load("img/gameover.jpeg") # load the game over background image
    game_over_bg = pygame.transform.scale(game_over_bg, (WINDOW_WIDTH, WINDOW_HEIGHT)) # resize it to fit the window

    start_bg = pygame.image.load("img/start_page.jpg") # set the home screen
    start_bg = pygame.transform.scale(start_bg, (WINDOW_WIDTH, WINDOW_HEIGHT)) # resize the background

    coin_sound = pygame.mixer.Sound("rec/treasure.mpeg") # set the sound for the treasure

    hit_sound = pygame.mixer.Sound("rec/trap1.mpeg") # set the sound when we take the trap

    font = pygame.font.SysFont("monospace", 24, bold=True)  # small font used for score/health/timer text
    big_font = pygame.font.SysFont("monospace", 48, bold=True)  # large font used for "GAME OVER" text



    def start_screen():
        screen.blit(start_bg, (0, 0)) #(0,0) is the position of the image 

        title = big_font.render("Treasure Hunter Adventure", True, (255, 255, 255)) # True to show 
        hint  = font.render("Press ENTER to start", True, (255, 255, 255))

        screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 140)) # //2 to be at the center of the screen
        screen.blit(hint,  (WINDOW_WIDTH//2 - hint.get_width()//2, 320))

        pygame.display.flip() # push everything to the screen so the player can see it
        
    def check_collision(rect_a, rect_b):
        return rect_a.colliderect(rect_b)  # returns True if the two rectangles overlap, False otherwise


    def draw_timer_health_score(screen, player, time_left):
        
        score_text  = font.render(f"Score: {player.score}",   True, (255, 255, 255))  # white text
        health_text = font.render(f"Health: {player.health}", True, (50, 200, 80))    # green text
        timer_text  = font.render(f"Time: {time_left}s",      True, (255, 140, 0))    # orange text
        screen.blit(score_text,  (10, 10))  # draw score at top left
        screen.blit(health_text, (10, 40))  # draw health just below the score
        screen.blit(timer_text,  (10, 70))  # draw timer just below the health

    def save_score(player_name, score):
        try:
            file = open(SCORES_FILE, "a")
            file.write(f"{player_name},{score},{date.today()}\n")
            file.close()
        except IOError:
          print("Could not save score")
        
        
    def show_statistics():
 
     try:
        df = pd.read_csv(SCORES_FILE, header=None)

        # Give names to the 3 columns manually
        df.columns = ["name", "score", "date"]

        if df.empty:
            print("No scores yet.")
            return

        print("\nGAME STATISTICS ")
        print("Highest Score:", df["score"].max())
        print("Lowest Score:", df["score"].min())
        print("Average Score:", round(df["score"].mean(), 2))
        print("Number of Games:", len(df))

     except FileNotFoundError:
        print("No scores file found yet.")
        
        
    def game_over_screen(player):
        
        screen.blit(game_over_bg, (0, 0))  # draw the game over background image

        if player.health <= 0:  # player died
            reason = font.render("You ran out of health!", True, (220, 50, 50))  # red message
        else:  # timer ran out
            reason = font.render("Time is up!",True, (255, 140, 0))  # orange message

        title = big_font.render("GAME OVER", True, (255, 50,  50))   # big red title
        score = font.render(f"Final Score: {player.score}", True, (255, 255, 255))  # white final score
        hint  = font.render("Press ESC to quit", True, (150, 150, 150))  # grey hint text

        # center  each text piece horizontally by subtracting half its width from the middle of the screen
        screen.blit(title,  (WINDOW_WIDTH // 2 - title.get_width()  // 2, 150))  # 150 is the y position in pixels
        screen.blit(reason, (WINDOW_WIDTH // 2 - reason.get_width() // 2, 260))  # get_width() gives the width of the text
        screen.blit(score,  (WINDOW_WIDTH // 2 - score.get_width()  // 2, 310))
        screen.blit(hint,   (WINDOW_WIDTH // 2 - hint.get_width()   // 2, 400))
        
        pygame.display.flip()  # push everything to the screen so the player can see it


        waiting = True
        while waiting:  # keep showing the screen until the player quits
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # player clicked the X button
                    waiting = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # player pressed ESC
                        waiting = False
                        
            pygame.display.flip()  # keep refreshing so the screen stays visible
            clock.tick(30) # 30 fps is enough for a static screen


    player = Player()  # create the player object here

    treasures = []
    for _ in range(5): 
        treasures.append(Treasure())  # create a treasure and add it to the list

    traps = []
    for _ in range(3): 
        traps.append(Trap())  # create a trap and add it to the list

    start_ticks = pygame.time.get_ticks()  # record the time the game started (in milliseconds)
    
    
    #this loop is For start screen frame
    waiting = True
    running = True

    while waiting:
        start_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                waiting = False
  
    
            if event.type == pygame.KEYDOWN: # if we press keydown so i can press any key 
                if event.key == pygame.K_RETURN: #  if they key is ENTER
                    waiting = False # so i go to the game directly
    
    
                  
    if not running:
        pygame.quit()
        return 
    
    #This loop is mainplay game frame             
    running = True
    while running:  # this loop runs 60 times per second  one iteration = one frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # player clicked the X to close the window
                running = False

        # 2. time left
        elapsed   = (pygame.time.get_ticks() - start_ticks) // 1000  # seconds since game started
        time_left = GAME_DURATION - elapsed  # seconds remaining

        if time_left <= 0:
            time_left = 0
            running = False   # time ran out

        if player.health <= 0:
            player.health = 0  # clamp to 0 so it never shows a negative number
            running = False    # player died

        # 3. move player
        player.move()
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)  # player rectangle for collision detection

        # 4. treasures
        for i in range(len(treasures)):
            treasure = treasures[i]
            treasure_rect = pygame.Rect(treasure.x, treasure.y, treasure.size, treasure.size)  # treasure itself
            
            if check_collision(player_rect, treasure_rect): # check both if player and treasure is found so the player may touch the treasure
                player.score += treasure.value 
                coin_sound.play()
                treasures[i] = Treasure()    # treasure[i] should be empty and creates another flower randomly             

        # 5. traps
        for trap in traps:
            trap.update()  # move the trap if 2 seconds have passed
            trap_rect = pygame.Rect(trap.x, trap.y, trap.size, trap.size)
            
            if check_collision(player_rect, trap_rect):  # if player and trap are found so player  may touch trap
                
              if not trap.hit:
                player.health -= trap.damage
                hit_sound.play()
                trap.hit = True # dont damage again
            else:
                trap.hit = False  # player moved away

        screen.blit(background, (0, 0))  # draw the background image (removes the previous frame)

        for treasure in treasures:
            treasure.draw(screen)  # draw each treasure image

        for trap in traps:
            trap.draw(screen)  # draw each trap image

        player.draw(screen)   # draw the player image on top
        draw_timer_health_score(screen, player, time_left)  # draw the  (score, health, timer)
        pygame.display.flip()   # show the completed frame on screen
        clock.tick(60)   # wait so the loop runs at most 60 frames per second

    save_score(player_name, player.score)  # write this game's score to the CSV file
    show_statistics() # print all-time stats to the terminal
    game_over_screen(player)   # show the Game Over screen and wait for ESC
    pygame.quit()


if __name__ == "__main__":
    main()