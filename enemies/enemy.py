import pygame

class Enemy:
    images = []

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animation_count = 0
        self.health = 1
        self.path = [(19, 224), (177, 235), (282, 283), (526, 277), (607, 217), (641, 105), (717, 57), (796, 83), (855, 222), (973, 284), (1046, 366)] # List of points that define the path taken (currently hardcoded). Replace with path-finding algorithm
        self.img = None

    def draw(self, win):
        # Draws enemy with given image
        self.animation_count += 1
        self.img = self.images[self.animation_count]
        
        # Resetting back to first animation after looping through entire list of animations 
        if self.animation_count >= len(self.images):
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
        pass
    
    def hit(self):
        # Returns if an enemy has died and removes one health
        self.health -= 1
        if self.health <= 0:
            return True
