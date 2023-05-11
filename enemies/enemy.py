import pygame
import math

class Enemy:
    
    def __init__(self):
        self.width = 64
        self.height = 64
        self.animation_count = 0
        self.max_health=1
        self.health = 1
        self.velocity = 3
        self.path = [(-10,170),(650,170),(650,70),(1150,70),(1150,570),(1050,570),(1050,470),(850,470),(850,670),(250,670),(250,470),(-20,470)] # List of points that define the path taken (currently hardcoded). Replace with path-finding algorithm
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
        self.draw_health_bar(win)
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
        

    def hit(self, damage):
        """
        Returns if an enemy has died and removes one health
        each call
        :return: Bool
        """
        self.health -= damage
        if self.health <= 0:
            return True
        return False
    
    def draw_health_bar(self, win):
        """
        draw health bar above enemy
        :param win: surface
        :return: None
        """
        length = 50
        move_by = length / self.max_health
        health_bar = round(move_by * self.health)

        pygame.draw.rect(win, (255,0,0), (self.x-30, self.y-75, length, 10), 0)
        pygame.draw.rect(win, (0, 255, 0), (self.x-30, self.y - 75, health_bar, 10), 0)
