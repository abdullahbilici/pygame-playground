import pygame
import numpy as np
from random import random

pygame.init()

WIDTH,HEIGHT = 1200,800
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Chase")

# Colors
BLUE = "#3498db"
RED = "#c0392b"
PURPLE = "#9b59b6"
YELLOW = "#f1c40f"
GREEN = "#2ecc71"
GREY = "#7f8c8d"
LIGHT_BLACK = "#3d3d3d"
BLACK = "#303030"

COLORS = [BLUE,RED,PURPLE,YELLOW,GREEN,GREY]

# Define walls as rectangles (x, y, width, height)
WALLS = [
	pygame.Rect(300, 200, 40, 400),   # Vertical wall middle-left
	pygame.Rect(900, 200, 40, 400),   # Vertical wall middle-right
	pygame.Rect(400, 300, 400, 40),   # Horizontal wall middle
]

# Font
font100 = pygame.font.Font("font/Pixeltype.ttf",100)
font70 = pygame.font.Font("font/Pixeltype.ttf",70)
font40 = pygame.font.Font("font/Pixeltype.ttf",40)

# Clock
clock = pygame.time.Clock()
time_limit = pygame.USEREVENT + 1
pygame.time.set_timer(time_limit, 1000)

class Player():
	def __init__(self, loc, color, chaser):
		self.width = 70
		self.loc = np.array(loc)
		self.rect = pygame.Rect(self.loc[0], self.loc[1], self.width, self.width)
		self.pace = np.array([0.0,0.0])
		self.acc = np.array([0.0,0.0])
		self.color = color
		self.chaser = chaser
		self.keys = list()
		self.marker_rect = pygame.Rect(self.loc[0] + 2*self.width/10, self.loc[1], 6*self.width/10, 2*self.width/10)
		

		# Chaser must be slower
		if self.chaser:
			self.maks_acc = .4
			self.skill = [1, 7] # skill used, remaining ms's
		else:
			self.maks_acc = .45
			self.skill = [1, 7]

		self.point = 0


	def draw(self):
		pygame.draw.rect(SCREEN, self.color, self.rect)

		if self.chaser: # Draws the marker
			self.marker_rect = pygame.Rect(self.loc[0] + 2*self.width/10, self.loc[1], 6*self.width/10, 2*self.width/10) # Updates marker
			pygame.draw.rect(SCREEN, BLACK, self.marker_rect)
		elif self.skill[0] == 1:
			self.marker_rect = pygame.Rect(self.loc[0] + 1*self.width/10, self.loc[1] + 11*self.width/12, 8*self.width/10, self.width/12) # Updates marker
			pygame.draw.rect(SCREEN, YELLOW, self.marker_rect)


	def replace(self):
		# Store previous position for collision detection
		prev_pos = self.loc.copy()
		
		for i in self.keys[::-1]: # Updates the self.acc according to the key combination
			if i == "up":
				if self.loc[1] != 50: # Checks the border
					if self.skill[0] == 0 and self.skill[1] > 0:
						self.acc[1] = -self.maks_acc * 3
						self.skill[1] -= 1	
					else:
						self.acc[1] = -self.maks_acc
			elif i == "down":
				if self.loc[1] != HEIGHT - self.width: # Checks the border
					if self.skill[0] == 0 and self.skill[1] > 0:
						self.acc[1] = self.maks_acc * 3
						self.skill[1] -= 1	
					else:
						self.acc[1] = self.maks_acc
			elif i == "right":
				if self.loc[0] != WIDTH - self.width: # Checks the border
					if self.skill[0] == 0 and self.skill[1] > 0:
						self.acc[0] = self.maks_acc * 3
						self.skill[1] -= 1	
					else:
						self.acc[0] = self.maks_acc
			elif i == "left":
				if self.loc[0] != 0: # Checks the border
					if self.skill[0] == 0 and self.skill[1] > 0:
						self.acc[0] = -self.maks_acc * 3
						self.skill[1] -= 1	
					else:
						self.acc[0] = -self.maks_acc

		# If user doesn't press keys makes self.acc zero
		if "up" not in self.keys and "down" not in self.keys: # != if "up" and "down" not in self.keys:
			self.acc[1] = 0.0
		if "right" not in self.keys and "left" not in self.keys:
			self.acc[0] = 0.0

		# If user preses two keys in 1D at the same time makes self.acc zero.
		if "up" in self.keys and "down" in self.keys:
			self.acc[1] = 0.0
		if "left" in self.keys and "right" in self.keys:
			self.acc[0] = 0.0
			
		# Checks the right border
		if self.loc[0] + self.width + self.pace[0] > WIDTH:
			self.loc[0] = WIDTH - self.width
			self.pace[0] = 0.0
			self.acc[0] = 0.0
			
		# Checks the left border
		if self.loc[0] + self.pace[0] < 0:
			self.loc[0] = 0
			self.pace[0] = 0.0
			self.acc[0] = 0.0

		# Checks the bottom border
		if self.loc[1] + self.width + self.pace[1] > HEIGHT:
			self.loc[1] = HEIGHT - self.width
			self.pace[1] = 0.0
			self.acc[1] = 0.0
		
		# Checks the top border
		if self.loc[1] + self.pace[1] < 50:
			self.loc[1] = 50
			self.pace[1] = 0.0
			self.acc[1] = 0.0

		# Makes the updates
		self.loc += self.pace
		self.pace *= 0.94
		self.pace += self.acc
		
		# Create temporary rect at new position
		new_rect = pygame.Rect(self.loc[0], self.loc[1], self.width, self.width)
		
		# Check wall collisions
		for wall in WALLS:
			if new_rect.colliderect(wall):
				# Determine collision axis by checking previous position
				if prev_pos[0] + self.width <= wall.left or prev_pos[0] >= wall.right:
					# X-axis collision
					self.loc[0] -= self.pace[0]
					self.pace[0] = 0.0
					self.acc[0] = 0.0
				
				if prev_pos[1] + self.width <= wall.top or prev_pos[1] >= wall.bottom:
					# Y-axis collision
					self.loc[1] -= self.pace[1]
					self.pace[1] = 0.0
					self.acc[1] = 0.0

		# Update rect position
		self.rect = pygame.Rect(self.loc[0], self.loc[1], self.width, self.width)

	
	def random_loc(self):
		while True:
			# Creates random location
			if self.chaser:
				self.loc = np.array([random()*(WIDTH/2 - self.width), random() * (HEIGHT - self.width - 50) + 50])
			else:
				self.loc = np.array([random()*(WIDTH/2 - self.width) + (WIDTH/2), random() * (HEIGHT - self.width - 50) + 50])
			
			# Check if the new location collides with any wall
			test_rect = pygame.Rect(self.loc[0], self.loc[1], self.width, self.width)
			if not any(test_rect.colliderect(wall) for wall in WALLS):
				break  # Valid position found, exit loop
	
	
def ingame_texts(timer, limit):
	# RED's points
	player2_score_surface = font40.render(f"RED: {player1.point}", True, GREEN)
	player2_score_rect = player2_score_surface.get_rect(midright = (WIDTH-15,25))
	SCREEN.blit(player2_score_surface,player2_score_rect)

	# BLUE's points
	player1_score_surface = font40.render(f"BLUE: {player2.point}", True, GREEN)
	player1_score_rect = player1_score_surface.get_rect(midleft = (75,25))
	SCREEN.blit(player1_score_surface,player1_score_rect)

	if player1.chaser:
		chaser = "RED"
	else:
		chaser = "BLUE"

	# Who's turn
	turn_surface = font40.render(f"{chaser}'s turn", True, GREEN)
	turn = turn_surface.get_rect(center = (2*WIDTH/5,25))
	SCREEN.blit(turn_surface,turn)

	# Timer
	timer_surface = font40.render(f"time : {limit - timer}", True, GREEN)
	timer_rect = timer_surface.get_rect(center = (3*WIDTH/5,25))
	SCREEN.blit(timer_surface,timer_rect)

	pygame.draw.line(SCREEN, BLACK, (0,50), (WIDTH,50))


# Creates players
player1 = Player([1000.0,100.0], RED, chaser = False)
player2 = Player([100.0,100.0], BLUE, chaser = True)

def main():
	run = True
	timer = 0
	limit = 15

	while run:
		SCREEN.fill(LIGHT_BLACK)
		
		# Add wall drawing before player drawing
		for wall in WALLS:
			pygame.draw.rect(SCREEN, BLACK, wall)
			
		for event in pygame.event.get():
			
			if event.type == pygame.QUIT: run = False

			# Key presses
			if event.type == pygame.KEYDOWN:

				# RED's key presses
				if event.key == pygame.K_UP:
					if "up" in player1.keys:
						player1.keys.remove("up")
					player1.keys.insert(0, "up")
				if event.key == pygame.K_LEFT:
					if "left" in player1.keys:
						player1.keys.remove("left")
					player1.keys.insert(0, "left")
				if event.key == pygame.K_RIGHT:
					if "right" in player1.keys:
						player1.keys.remove("right")
					player1.keys.insert(0, "right")
				if event.key == pygame.K_DOWN:
					if "down" in player1.keys:
						player1.keys.remove("down")
					player1.keys.insert(0, "down")

				# BLUE's key presses
				if event.key == pygame.K_w:
					if "up" in player2.keys:
						player2.keys.remove("up")
					player2.keys.insert(0, "up")
				if event.key == pygame.K_a:
					if "left" in player2.keys:
						player2.keys.remove("left")
					player2.keys.insert(0, "left")
				if event.key == pygame.K_d:
					if "right" in player2.keys:
						player2.keys.remove("right")
					player2.keys.insert(0, "right")
				if event.key == pygame.K_s:
					if "down" in player2.keys:
						player2.keys.remove("down")
					player2.keys.insert(0, "down")
				
				# Skill for RED
				if event.key in (pygame.K_RCTRL, pygame.K_RSUPER):
					if not player1.chaser:
						if player1.skill[0] == 1:
							player1.skill = [0, 7]
				
				# Skill for BLUE
				if event.key == pygame.K_SPACE:
					if not player2.chaser:
						if player2.skill[0] == 1:
							player2.skill = [0, 7]

			# Key releases
			if event.type == pygame.KEYUP:
				# RED's releases
				if event.key == pygame.K_UP:
					if "up" in player1.keys: player1.keys.remove("up")
				if event.key == pygame.K_LEFT:
					if "left" in player1.keys: player1.keys.remove("left")
				if event.key == pygame.K_RIGHT:
					if "right" in player1.keys: player1.keys.remove("right")
				if event.key == pygame.K_DOWN:
					if "down" in player1.keys: player1.keys.remove("down")
				# BLUE's releases
				if event.key == pygame.K_w:
					if "up" in player2.keys: player2.keys.remove("up")
				if event.key == pygame.K_a:
					if "left" in player2.keys: player2.keys.remove("left")
				if event.key == pygame.K_d:
					if "right" in player2.keys: player2.keys.remove("right")
				if event.key == pygame.K_s:
					if "down" in player2.keys: player2.keys.remove("down")
			
			# Checks the time
			if event.type == time_limit:
				timer += 1
				if timer == limit: # After 15 seconds
					# Gives points
					if player1.chaser:
						player2.point += 1
					else:
						player1.point += 1

					# Changes the self.acc and self.chaser state.
					player1.maks_acc, player2.maks_acc = player2.maks_acc, player1.maks_acc
					player1.chaser, player2.chaser = player2.chaser, player1.chaser
					# Makes pace zero
					player1.pace = np.array([0.0, 0.0]) 
					player2.pace = np.array([0.0, 0.0])
					# Changes position
					player1.random_loc()
					player2.random_loc()
					# Reset timer
					timer = 0
					# Reset the clock
					pygame.time.set_timer(time_limit, 1000)
			
		if	player1.rect.colliderect(player2.rect):
			# Gives points
			if player1.chaser:
				player1.point += 1
			else:
				player2.point += 1

			# Changes the self.acc and self.chaser state.
			player1.maks_acc, player2.maks_acc = player2.maks_acc, player1.maks_acc
			player1.chaser, player2.chaser = player2.chaser, player1.chaser
			# Makes pace zero
			player1.pace = np.array([0.0, 0.0]) 
			player2.pace = np.array([0.0, 0.0])
			# Changes position
			player1.random_loc()
			player2.random_loc()
			# Reset timer
			timer = 0
			# Reset skill
			player1.skill = player2.skill = [1, 0]
			# Reset the clock
			pygame.time.set_timer(time_limit, 1000)

		ingame_texts(timer, limit)
		player1.replace()
		player2.replace()
		player1.draw()
		player2.draw()
		
		pygame.display.update()
		clock.tick(60)

	pygame.quit()

main()