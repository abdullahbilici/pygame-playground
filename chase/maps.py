import pygame

# Colors
BLACK = "#303030"

class Wall:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BLACK

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Map:
    def __init__(self):
        self.walls = []
    
    def add_wall(self, x, y, width, height):
        self.walls.append(Wall(x, y, width, height))
    
    def draw(self, screen):
        for wall in self.walls:
            wall.draw(screen)
    
    def check_collision(self, player_rect):
        for wall in self.walls:
            if player_rect.colliderect(wall.rect):
                return True
        return False

# Predefined maps
def get_map_1():
    map_1 = Map()
    # Add some walls for the first map layout
    map_1.add_wall(300, 200, 40, 400)  # Vertical wall
    map_1.add_wall(800, 200, 40, 400)  # Vertical wall
    map_1.add_wall(400, 300, 400, 40)  # Horizontal wall
    return map_1

def get_map_2():
    map_2 = Map()
    # Add walls for the second map layout
    map_2.add_wall(200, 200, 40, 200)  # Top left
    map_2.add_wall(900, 200, 40, 200)  # Top right
    map_2.add_wall(200, 500, 40, 200)  # Bottom left
    map_2.add_wall(900, 500, 40, 200)  # Bottom right
    map_2.add_wall(500, 300, 200, 40)  # Center
    return map_2

def get_map_3():
    map_3 = Map()
    # Add walls for the third map layout - maze-like
    map_3.add_wall(300, 150, 40, 300)   # Left vertical
    map_3.add_wall(300, 150, 300, 40)   # Top horizontal
    map_3.add_wall(600, 150, 40, 500)   # Right vertical
    map_3.add_wall(300, 600, 600, 40)   # Bottom horizontal
    return map_3

# List of all available maps
MAPS = [
    get_map_1(),
    get_map_2(),
    get_map_3()
] 