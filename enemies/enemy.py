import pygame
import math

class Enemy:
    images = []

    def __init__(self):
        self.width = 64
        self.height = 64
        self.animation_count = 0
        self.health = 1
        self.velocity = 3
        self.path = [(19, 224), (177, 235), (282, 283), (526, 277), (607, 217), (641, 105), (717, 57), (796, 83), (855, 222), (973, 284), (1046, 366), (1022, 458), (894, 492), (740, 504), (580, 542), (148, 541), (85, 452), (52, 345), (1, 335), (-20, 355)] # List of points that define the path taken (currently hardcoded). Replace with path-finding algorithm
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.img = None
        self.dist = 0
        self.pathPos = 0
        self.moveCount = 0
        self.moveDist = 0


    def draw(self, win):
        # Draws enemy with given image
        self.img = self.images[self.animation_count//3]
        self.animation_count += 1

        # Resetting back to first animation after looping through entire list of animations 
        if self.animation_count >= len(self.images)*3:
            self.animation_count = 0

        win.blit(self.img, (self.x, self.y))
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

        # Total distance needed to move to reach destination pt
        moveDist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        self.moveCount += 1
        direction = (x2-x1, y2-y1)

        # Calculating how much distance moved from current point to next
        x_move, y_move = (self.x + direction[0] * self.moveCount, self.y + direction[1] * self.moveCount)
        self.dist += math.sqrt((x_move - x1) ** 2 + (y_move - y1) ** 2)
        
        # Go to next point
        if self.dist >= moveDist:
            self.dist = 0
            self.moveCount = 0
            self.pathPos += 1
            if self.pathPos >= len(self.path):
                return False

        self.x = x_move
        self.y = y_move
        return True

    def hit(self):
        # Returns if an enemy has died and removes one health
        self.health -= 1
        if self.health <= 0:
            return True
