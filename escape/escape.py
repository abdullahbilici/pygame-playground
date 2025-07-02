# İmportng necessary libraries
import pygame
import numpy as np
from time import sleep, time
import sys

# İnitialize the pygame
pygame.init()

# Sets the width and hight of screen
WIDTH, HEIGHT = 500,700

# Creates the screen
screen = pygame.display.set_mode((WIDTH,HEIGHT))

# Sets caption
pygame.display.set_caption("game")

# Game state will open diffrent screens in game

# Time
clock = pygame.time.Clock()
door_timer = pygame.USEREVENT + 1
pygame.time.set_timer(door_timer, 100)

# Colors
BLUE = "#3498db"
RED = "#c0392b"
PURPLE = "#9b59b6"
YELLOW = "#f1c40f"
GREEN = "#2ecc71"
GREY = "#7f8c8d"
BLACK = "#3d3d3d"
WHITE = "#efefef"

COLORS = {"blue": BLUE, "red": RED, "purple": PURPLE, "yellow": YELLOW, "green": GREEN, "grey": GREY, "black": BLACK, "white": WHITE}
"/black.png"
# Font
font100 = pygame.font.Font("./font/Pixeltype.ttf",100)
font70 = pygame.font.Font("./font/Pixeltype.ttf",70)
font40 = pygame.font.Font("./font/Pixeltype.ttf",40)


# Heart
red_heart = pygame.image.load("./pic/red_heart.png").convert_alpha()
grey_heart = pygame.image.load("./pic/grey_heart.png").convert_alpha()
red_heart = pygame.transform.rotate(red_heart, 45)
grey_heart = pygame.transform.rotate(grey_heart, 45)

# Player class
class Player():
    # Initialize
    def __init__(self):
        self.width = 40
        self.color = GREEN
        self.loc = np.array([WIDTH/2-self.width/2,640])
        self.rect = pygame.Rect(self.loc[0], self.loc[1], self.width, self.width)
        self.pace = np.array([0,0])
        self.heart = 3
        self.level = 0
        self.game_state = "start_game"

    # Draws player
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    # Changes location of player respect to player.pace
    def replace(self):

        # Replace player in x-axis  
        self.loc[0] += self.pace[0] * 5

        # If player goes out of screen puts it back to sccreen
        if self.loc[0] < 0:
            self.loc[0] = 0
        elif self.loc[0] > WIDTH - self.width:
            self.loc[0] = WIDTH - self.width

        self.rect = pygame.Rect(self.loc[0], self.loc[1], self.width, self.width)

        # Checks if player collideing with walls or doors
        for wall in levels[self.level][1]:
            if wall.rect.colliderect(self.rect):
                self.loc[0] -= self.pace[0]*5
                self.rect = pygame.Rect(self.loc[0], self.loc[1], self.width, self.width)

                # If the wall is red player lose heart.
                if isinstance(wall, RWall):
                    self.reset()
                    self.heart -= 1
                    if self.heart == 0: self.game_state = "game_over"
                    for door in levels[self.level][0]:
                        door.reset()

        for door in levels[self.level][0]:
            if not door.open:
                if self.rect.colliderect(door.door_rect):
                    self.loc[0] -= self.pace[0]*5
                    self.rect = pygame.Rect(self.loc[0], self.loc[1], self.width, self.width)

        # replace player in y-axis
        self.loc[1] += self.pace[1] * 5

        # If player goes out of screen puts it back to sccreen
        if self.loc[1] < 0:
            self.loc[1] = 0
        elif self.loc[1] > HEIGHT - self.width:
            self.loc[1] = HEIGHT - self.width

        self.rect = pygame.Rect(self.loc[0], self.loc[1], self.width, self.width)

        # Checks if player collideing with walls or doors
        for wall in levels[self.level][1]:
            if wall.rect.colliderect(self.rect):
                self.loc[1] -= self.pace[1]*5
                self.rect = pygame.Rect(self.loc[0], self.loc[1], self.width, self.width)

                # If the wall is red player lose heart.
                if isinstance(wall, RWall):
                    self.reset()
                    self.heart -= 1
                    if self.heart == 0: self.game_state = "game_over"
                    for door in levels[self.level][0]:
                        door.reset()

        for door in levels[self.level][0]:
            if not door.open:
                if self.rect.colliderect(door.door_rect):
                    self.loc[1] -= self.pace[1]*5
                    self.rect = pygame.Rect(self.loc[0], self.loc[1], self.width, self.width)

        # Check şf player passes the level
        if self.loc[1] < 50:
            self.reset()
            self.level += 1

    # Resets players location and pace
    def reset(self):
        self.loc = np.array([WIDTH/2-self.width/2,640])
        self.rect = pygame.Rect(self.loc[0], self.loc[1], self.width, self.width)
        self.pace = np.array([0,0])

    # Shows how many hearts player have
    def draw_heart(self):
        if self.heart == 3:
            screen.blit(red_heart,red_heart.get_rect( topleft = (WIDTH-50 , 6) ))
            screen.blit(red_heart,red_heart.get_rect( topleft = (WIDTH-90 , 6) ))
            screen.blit(red_heart,red_heart.get_rect( topleft = (WIDTH-130 , 6) ))

        elif self.heart == 2:
            screen.blit(grey_heart,red_heart.get_rect( topleft = (WIDTH-50 , 6) ))
            screen.blit(red_heart,red_heart.get_rect( topleft = (WIDTH-90 , 6) ))
            screen.blit(red_heart,red_heart.get_rect( topleft = (WIDTH-130 , 6) ))

        elif self.heart == 1:
            screen.blit(grey_heart,red_heart.get_rect( topleft = (WIDTH-50 , 6) ))
            screen.blit(grey_heart,red_heart.get_rect( topleft = (WIDTH-90 , 6) ))
            screen.blit(red_heart,red_heart.get_rect( topleft = (WIDTH-130 , 6) ))    

        else:
            screen.blit(grey_heart,red_heart.get_rect( topleft = (WIDTH-50 , 6) ))
            screen.blit(grey_heart,red_heart.get_rect( topleft = (WIDTH-90 , 6) ))
            screen.blit(grey_heart,red_heart.get_rect( topleft = (WIDTH-130 , 6) ))

# Door-Key class
class DoorKey():
    # Initialize
    def __init__(self, color, keyloc, doorloc, doorwidth, doorheight,time):
        self.color = COLORS[color]
        self.surface = pygame.image.load(f"./pic/{color}.png")
        self.surface = pygame.transform.scale(self.surface, (30, 12))
        self.surface = pygame.transform.rotate(self.surface, 40)
        self.key_rect = self.surface.get_rect(topleft= keyloc)
        self.doorloc = doorloc
        self.doorwidth = doorwidth
        self.doorheight = doorheight
        self.door_rect = pygame.Rect(self.doorloc[0], self.doorloc[1], self.doorwidth, self.doorheight)
        # How much seconds/10 after door opens it will close
        self.time_limit = time
        # How much  seconds/10 passed after door opened
        self.timer = 0
        self.open = False

    # Draws key and door
    def draw(self):
        if not self.open:
            screen.blit(self.surface, self.key_rect)
            pygame.draw.rect(screen, self.color, self.door_rect)

    # Reset key and door
    def reset(self):
        self.open = False
        self.timer = 0

# Wall class
class Wall():
    # Initialize
    def __init__(self, loc, width, height):
        self.color = WHITE
        self.loc = loc
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.loc[0], self.loc[1], self.width, self.height)

    # Draws wall
    def draw(self):
        # If wall is red wall it will draw it red
        if isinstance(self, RWall):
            pygame.draw.rect(screen, "#FF0000", self.rect)

        # If wall is normal wall it will draw it normally
        else:
            pygame.draw.rect(screen, self.color, self.rect)

class RWall(Wall):
    pass

# Prints level and return text in screen in game
def game_text(level):
    resart_surface = font40.render("Resart: R", True, WHITE)
    resart_rect = resart_surface.get_rect(midleft = (15,25))
    screen.blit(resart_surface,resart_rect)

    level_surface = font40.render(f"Level: {level + 1}",True,WHITE)
    level_rect = level_surface.get_rect(center = (WIDTH/2,25))
    screen.blit(level_surface,level_rect)

# Prints game over screen
def game_over(level):
    game_over_surface = font70.render("Game Over", True, WHITE)
    game_over_rect = game_over_surface.get_rect(midtop = (WIDTH/2,200))
    screen.blit(game_over_surface, game_over_rect)

    score_surface = font40.render(f"Your Score: {level}", True, GREEN)
    score_rect = score_surface.get_rect(topleft = (100,280))
    screen.blit(score_surface, score_rect)

    play_again_surface = font40.render("Press space to play again", True, GREEN)
    play_again_rect = play_again_surface.get_rect(topleft = (100,330))
    screen.blit(play_again_surface, play_again_rect)

# Prints starting screen
def start_game():
    escape_surface = font100.render("ESCAPE!", True, RED)
    escape_rect = escape_surface.get_rect(midtop = (WIDTH/2,100))
    screen.blit(escape_surface, escape_rect)

    welcome_surface = font70.render("Welcome to Escape!", True, WHITE)
    welcome_rect = welcome_surface.get_rect(midtop = (WIDTH/2,220))
    screen.blit(welcome_surface, welcome_rect)

    start_game_surface = font40.render("Press space to start", True, GREEN)
    start_game_rect = start_game_surface.get_rect(topleft = (120,330))
    screen.blit(start_game_surface, start_game_rect)

# Prints win game screen
def win_game(time_played):
    congratulations_surface = font70.render("Congratulations!!", True, WHITE)
    congratulations_rect = congratulations_surface.get_rect(midtop = (WIDTH/2,200))
    screen.blit(congratulations_surface, congratulations_rect)

    win_game_surface = font40.render("You Finished the game!!", True, WHITE)
    win_game_rect = win_game_surface.get_rect(midtop = (WIDTH/2,265))
    screen.blit(win_game_surface, win_game_rect)

    score_surface = font40.render(f"You Finished the game in {format(time_played,'.2f')} seconds.", True, WHITE)
    score_rect = score_surface.get_rect(midtop = (WIDTH/2,310))
    screen.blit(score_surface, score_rect)

    play_again_surface = font40.render("Press space to play again", True, GREEN)
    play_again_rect = play_again_surface.get_rect(midtop = (WIDTH/2,400))
    screen.blit(play_again_surface, play_again_rect)

# Levels
level1_keys = [DoorKey("yellow", (460,410), (175,100), 150, 25, 20)]
level1_walls = [Wall((0,100), 175, 50), Wall((325,100), 175, 50), Wall((WIDTH - 50, 450), 50, 50)]
level1 = [level1_keys, level1_walls]

level2_keys = [DoorKey("yellow", (135,365), (175,430), 25, 75, 33), DoorKey("blue", (15,290), (175,100), 150, 25, 30)]
level2_walls = [Wall((0,100), 175, 50), Wall((325,100), 175, 50), RWall((0,230), 75, 25), Wall((75,230), 25, 175), Wall((75,405), 125, 25), Wall((0,505), 200, 25)]
level2 = [level2_keys, level2_walls]

level3_keys = [DoorKey("yellow", (460,560), (50,475), 150, 25, 20), DoorKey("purple", (10,437), (300, 350), 150, 25, 20), DoorKey("red", (460,313), (50,225), 150, 25, 20), DoorKey("blue", (10,187), (300,100), 150, 25, 20)]
level3_walls = [Wall((0,100), 300, 50), Wall((450,100), 50, 50), Wall((0,225), 50, 50), Wall((200,225), 300, 50), Wall((0,350), 300, 50), Wall((450,350), 50, 50), Wall((0,475), 50, 50), Wall((200,475), 300, 50), Wall((WIDTH-50,600), 50, 50) ] 
level3 = [level3_keys, level3_walls]

level4_keys = [DoorKey("yellow", (460,310), (0,300), 274, 25, 27), DoorKey("purple", (7,460), (1000,3000), 1, 1, 1), DoorKey("grey", (82,460), (175,100), 150, 25, 22), DoorKey("red", (157,460), (1000,3000), 1, 1, 1), DoorKey("blue", (232,460), (3000,1000), 1, 1, 1)]
level4_walls = [Wall((0,100), 175, 50), Wall((325,100), 175, 50), Wall((450,350), 50, 50), RWall((0,500), 275, 50), Wall((275,300), 50, 250), Wall((50,375), 25, 125), Wall((125,375), 25, 125), Wall((200,375), 25, 125)]
level4 = [level4_keys, level4_walls]

level5_keys = [DoorKey("grey",(20,645),(300,575), 150, 25, 17),DoorKey("yellow", (0,645), (50,455), 150, 25, 30), DoorKey("purple", (460,540), (300, 335), 150, 25, 30), DoorKey("red", (10,420), (50,215), 150, 25, 30), DoorKey("blue", (460,300), (300,95), 150, 25, 30)]
level5_walls = [Wall((0,95), 300, 50), Wall((450,95), 50, 50), Wall((0,215), 50, 50), Wall((200,215), 300, 50), Wall((0,335), 300, 50), Wall((450,335), 50, 50), Wall((0,455), 50, 50), Wall((200,455), 300, 50), Wall((WIDTH-50,575), 50, 50), Wall((0,575), 300, 50), Wall((0,680), 50, 50)] 
level5 = [level5_keys, level5_walls]

# Puts levels together
levels = [level1, level2, level3, level4, level5]

# Main function
def main():

    # Creates player
    player = Player()
    # Game loop
    while True:
        
        # What will happen in game
        if player.game_state == "game":
            for event in pygame.event.get():
                # If event is quit closes the game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Checks if any key pressed
                if event.type == pygame.KEYDOWN:
                    # Checks for directions
                    if event.key == pygame.K_UP:
                        player.pace[1] = -1

                    if event.key == pygame.K_DOWN:
                        player.pace[1] = 1

                    if event.key == pygame.K_LEFT:
                        player.pace[0] = -1

                    if event.key == pygame.K_RIGHT:
                        player.pace[0] = 1

                    # If r is pressed it will reset player position and doors and player will start level from beggining
                    if event.key == pygame.K_r:
                        player.reset()
                        player.heart -= 1
                        for door in levels[player.level][0]:
                            door.reset()
                        if player.heart == 0:
                            player.game_state = "game_over"
                            starting_time = time()

                    # This keys are for devoloping process
                    if event.key == pygame.K_s:
                        player.reset()
                        for door in levels[player.level][0]:
                            door.reset()
                        if player.level != len(levels) - 1:
                            player.level += 1

                    if event.key == pygame.K_a:
                        player.reset()
                        for door in levels[player.level][0]:
                            door.reset()
                        if player.level != 0:
                            player.level -= 1
                        else:
                            player.level = len(levels) - 1
                        

                    if event.key == pygame.K_k: 
                        if player.heart != 3: player.heart += 1

                # If player is going to the direction of released key it will make pace of that direction 0
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        
                        if player.pace[1] == -1: player.pace[1] = 0

                    if event.key == pygame.K_DOWN:
                        if player.pace[1] == 1: player.pace[1] = 0

                    if event.key == pygame.K_LEFT:
                        if player.pace[0] == -1: player.pace[0] = 0

                    if event.key == pygame.K_RIGHT:
                        if player.pace[0] == 1: player.pace[0] = 0

                # Checks if door has to be close after it opened.
                if event.type == door_timer:
                    for door in levels[player.level][0]:
                        if door.open:
                            if door.timer != door.time_limit:
                                door.timer += 1 
                            elif door.timer == door.time_limit:
                                door.timer = 0
                                door.open = False
                                # If door close on the player.
                                if door.door_rect.colliderect(player.rect):
                                    player.heart -= 1
                                    player.reset()
                                    if player.heart == 0:
                                        player.game_state = "game_over" 
                                        starting_time = time()
                                    for d in levels[player.level][0]:
                                        d.reset()

            # fills screen with black
            screen.fill(BLACK)
            game_text(player.level)
            player.draw_heart()
            # Green line on top of the screen
            pygame.draw.line(screen, GREEN, (0,50), (WIDTH,50))

            # Draws the doors and keys on screen
            # Check if player collide with any key. if it is door will open
            for key in levels[player.level][0]:
                key.draw()
                if key.key_rect.colliderect(player.rect):
                    key.open = True

            # Draws the walls in screen
            for wall in levels[player.level][1]:
                wall.draw()

            # Replaces the player
            player.replace()

            # Check if player wins the game.
            if player.level >= len(levels):
                player.game_state = "win_game"
                finishing_time = time()
                time_played = finishing_time - starting_time
                player.reset()

            # Draws player
            player.draw()

        # prints game over screen
        elif player.game_state == "game_over":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    # Starts the game if space pressed
                    if event.key == pygame.K_SPACE:
                        for lvl in levels:
                            for door in lvl[0]:
                                door.reset()
                        player.reset()
                        player.heart = 3
                        player.level = 0
                        player.game_state = "game"
            
            # Fills the screen with black
            screen.fill(BLACK)
            game_over(player.level)

        # Prints win game screen
        elif player.game_state == "win_game":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    # Starts game if space pressed
                    if event.key == pygame.K_SPACE:
                        for lvl in levels:
                            for door in lvl[0]:
                                door.reset()
                        player.reset()
                        player.heart = 3
                        player.level = 0
                        player.game_state = "game"
                        starting_time = time()

            # Fills the screen with black
            screen.fill(BLACK)
            win_game(time_played)

        # Prints starting screen
        elif player.game_state == "start_game":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    # Starts game if space pressed
                    if event.key == pygame.K_SPACE:
                        player.game_state = "game"
                        starting_time = time()

            # Fills screen with black
            screen.fill(BLACK)
            start_game()
            player.draw()

        pygame.display.update()
        clock.tick(60)
main()