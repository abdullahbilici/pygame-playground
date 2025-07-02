from random import randint
import time
import pygame

pygame.init()

# Colors
BLUE = "#3498db"
RED = "#c0392b"
PURPLE = "#9b59b6"
YELLOW = "#f1c40f"
GREEN = "#2ecc71"
GREY = "#3d3d3d"
BLACK = "#000000"
HEAD_BLACK = "#1d1d1d"

file_path = "./highscore.txt"

class Board():
    def __init__(self, width, height, size, space):
        # Number of squares
        self.width = width
        self.height = height
        self.lenght = 0

        # size of the squares
        self.size = size

        self.space = space
        self.score = 0
        self.state = 2

        # pixel size of the screen
        self.WIDTH = self.size * self.width + self.space * (self.width + 1)
        self.HEIGHT = self.size * self.height + self.space * (self.height + 1)

        #  Creates snake
        self.snake = [[randint(0,self.width-1),randint(0,self.height-1)]]
        self.snake_dir = [1,0]
        self.last_move = self.snake_dir

        # Creates apple
        self.apple = self.snake[0]
        while self.apple in self.snake:
            self.apple = [randint(0,self.width-1), randint(0,self.height-1)]

        # Creates matrix
        self.matrix = [[0 for i in range(self.height)] for i in range(self.width)]
        for p in self.snake:
            self.matrix[p[0]][p[1]] = 1
        self.matrix[self.apple[0]][self.apple[1]] = 2
        with open(file_path) as file:
            a = file.readline()
            self.highscore = int(a)

    def draw(self):
        self.matrix = [[0 for i in range(self.height)] for i in range(self.width)]
        for p in self.snake:
            self.matrix[p[0]][p[1]] = 1
        self.matrix[self.apple[0]][self.apple[1]] = 2
        
        for i in range(self.width):
            for j in range(self.height):
                # Calculates the coordinates of pieces
                x = (self.size+self.space) * i + self.space
                y = (self.size+self.space) * j + self.space + 40

                # Draws the ground
                pygame.draw.rect(screen, GREY,pygame.Rect(x,y,self.size,self.size))

                # Draws the snake
                if self.matrix[i][j] == 1:
                    pygame.draw.rect(screen, RED,pygame.Rect(x,y,self.size,self.size))

                # Draws the apple
                elif self.matrix[i][j] == 2:
                    pygame.draw.rect(screen, GREEN,pygame.Rect(x,y,self.size,self.size))
        # Makes the head black
        x = (self.size+self.space) * self.snake[-1][0] + self.space
        y = (self.size+self.space) * self.snake[-1][1] + self.space + 40
        pygame.draw.rect(screen,HEAD_BLACK,pygame.Rect(x,y,self.size,self.size))

    def snake_move(self):
        head = self.snake[-1]

        if self.snake_dir[0]:
            head = [head[0] + self.snake_dir[0], head[1]]

        if self.snake_dir[1]:
            head = [head[0] , head[1]- self.snake_dir[1]]

        self.snake.append(head)
        head[0] = head[0] % self.width 
        head[1] = head[1] % self.height
        if head in self.snake[1:-1]:
            self.state = 0
            h = 0
            with open(file_path) as file:
                h = int(file.readline())
            if self.score > h:
                with open(file_path,"w") as file:
                    file.write(str(self.score))
            time.sleep(2)

    def eat(self):
        if self.snake[-1] == self.apple:
            while self.apple in self.snake:
                self.apple = [randint(0,self.width-1), randint(0,self.height-1)]
            self.matrix[self.apple[0]][self.apple[1]] = 2
            self.score += 1
        else:
            if self.lenght > 0:
                pass
            else:
                self.snake.pop(0)

game = Board(30,20,30,5)
screen = pygame.display.set_mode((game.WIDTH, game.HEIGHT+ 40))
pygame.display.set_caption("Snake")
game.draw()

# Font
font70 = pygame.font.Font("./font/Pixeltype.ttf",70)
font40 = pygame.font.Font("./font/Pixeltype.ttf",40)

def print_score():
    score_surface = font70.render(f"score: {game.score}",True,GREY)
    score_rect = score_surface.get_rect(topleft = (game.WIDTH-250,5))
    screen.blit(score_surface,score_rect)

def start_game():
    pygame.draw.rect(screen,BLACK,pygame.Rect(0,0,game.WIDTH,40))
    start_surface = font40.render("Press any key to start game",True,GREY)
    start_rect = start_surface.get_rect(topleft = (20,13))
    screen.blit(start_surface,start_rect)

def fail_game():
    pygame.draw.rect(screen,BLACK,pygame.Rect(0,0,game.WIDTH-250,40))
    start_surface = font70.render("Game Over",True,GREY)
    start_rect = start_surface.get_rect(topleft = (30,5))
    screen.blit(start_surface,start_rect)

def print_highscore():

    highscore_surface = font40.render(f"highscore: {game.highscore}",True,GREY)
    highscore_rect = highscore_surface.get_rect(topleft = (50,13))
    screen.blit(highscore_surface,highscore_rect)

# Timer
clock = pygame.time.Clock()

movement_timer = pygame.USEREVENT + 1
pygame.time.set_timer(movement_timer,450)

def main():
    run = True
    global game
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            # Game loop
            if game.state == 1:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if game.last_move != [0,-1]:
                            game.snake_dir = [0,1]
                    if event.key == pygame.K_DOWN:
                        if game.last_move != [0,1]:
                            game.snake_dir = [0,-1]
                    if event.key == pygame.K_LEFT:
                        if game.last_move != [1,0]:
                            game.snake_dir = [-1,0]
                    if event.key == pygame.K_RIGHT:
                        if game.last_move != [-1,0]:
                            game.snake_dir = [1,0]

                if event.type == movement_timer:
                    screen.fill(BLACK)
                    game.snake_move()
                    game.eat()
                    game.draw()
                    game.last_move = game.snake_dir
                    print_score()
                    print_highscore()
            
            # Game over
            elif game.state == 0:
                if event.type == pygame.KEYDOWN:
                    game = Board(30,20,30,5)
                    game.state= 1
                    if event.key == pygame.K_UP:
                        game.snake_dir = [0,1]
                    if event.key == pygame.K_DOWN:
                        game.snake_dir = [0,-1]
                    if event.key == pygame.K_LEFT:
                        game.snake_dir = [-1,0]
                    if event.key == pygame.K_RIGHT:
                        game.snake_dir = [1,0]

                fail_game()
            
            # Opening of the game
            elif game.state == 2:
                if event.type == pygame.KEYDOWN:
                    game.state= 1
                    if event.key == pygame.K_UP:
                        game.snake_dir = [0,1]
                    if event.key == pygame.K_DOWN:
                        game.snake_dir = [0,-1]
                    if event.key == pygame.K_LEFT:
                        game.snake_dir = [-1,0]
                    if event.key == pygame.K_RIGHT:
                        game.snake_dir = [1,0]

                start_game()

        
        pygame.display.update()
        clock.tick(15)
main()