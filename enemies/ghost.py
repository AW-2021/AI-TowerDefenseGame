import pygame
import os
from .enemy import Enemy

class Ghost(Enemy):

    def __init__(self):
        super().__init__()
        self.images = []
        self.money = 10
        self.max_health=10
        self.health = self.max_health
        for x in range (20):
            add_str = str(x)
            if x < 10:
                add_str = "0" + add_str
            self.images.append(pygame.transform.scale(pygame.image.load(os.path.join("game_assets/enemies/PNG/9", "9_enemies_1_run_0" + add_str + ".png")), (128, 64) ))
            
            