import pygame
import math

class Enemy:
    
    def __init__(self):
        self.width = 64
        self.height = 64
        self.animation_count = 0
        self.health = 1
        self.velocity = 3
        self.path = [(-10, 224), (19, 224), (177, 235), (282, 283), (526, 277), (607, 217), (641, 105), (717, 57), (796, 83), (855, 222), (973, 284), (1046, 366), (1022, 458), (894, 492), (740, 504), (580, 542), (148, 541), (85, 442), (52, 335), (1, 305), (-20, 345)] # List of points that define the path taken (currently hardcoded). Replace with path-finding algorithm
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.img = None
        self.dist = 0
        self.pathPos = 0
        self.moveCount = 0
        self.moveDist = 0
        self.images = []
        self.flipped = False


    def draw(self, win):
        # Draws enemy with given image
        self.img = self.images[self.animation_count]
        self.animation_count += 1

        # Resetting back to first animation after looping through entire list of animations 
        if self.animation_count >= len(self.images):
            self.animation_count = 0

        # for pos in self.path:
        #     pygame.draw.circle(win, (255,0,0), pos, 10, 0)

        win.blit(self.img, (self.x - self.img.get_width()/2, self.y - self.img.get_height()/2 - 35))
        self.move()

    
    def collide(self, X, Y):
        # Returns if position has hit enemy
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True

        return False
    
    
    def move(self):
        # Move enemy
        x1, y1 = self.path[self.pathPos]
        
        if self.pathPos + 1 >= len(self.path):
            x2, y2 = (-10, 355)
        else:
            x2, y2 = self.path[self.pathPos + 1]

        direction = ((x2-x1) * 2, (y2-y1) * 2)
        length = math.sqrt((direction[0]**2) + (direction[1]**2))
        direction = (direction[0]/length, direction[1]/length) # Unit vector

        # Flipping image horizontally when the enemy turns around on path (-x direction)
        if direction[0] < 0 and not(self.flipped):
            self.flipped = True
            for x, img in enumerate(self.images):
                self.images[x] = pygame.transform.flip(img, True, False)

        # Calculating how much distance moved from current point to next
        x_move, y_move = ((self.x + direction[0]), (self.y + direction[1]))

        self.x = x_move
        self.y = y_move
        
        # Go to the next point
        if direction[0] >= 0: # Moving right
            if direction[1] >= 0: # Moving downwards
                if self.x >= x2 and self.y >= y2:
                    self.pathPos += 1

            else: # Moving upwards
                if self.x >= x2 and self.y <= y2:
                    self.pathPos += 1
        
        else: # Moving left
            if direction[1] >= 0: # Moving downwards
                if self.x <= x2 and self.y >= y2:
                    self.pathPos += 1

            else: # Moving upwards
                if self.x <= x2 and self.y >= y2:
                    self.pathPos += 1
        

    def hit(self):
        # Returns if an enemy has died & removes 1 health
        self.health -= 1
        if self.health <= 0:
            return True
