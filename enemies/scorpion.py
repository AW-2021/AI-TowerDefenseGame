import pygame
import os
from .enemy import Enemy

class Scorpion(Enemy):
    images = []

    for x in range (20):
        add_str = str(x)
        if x < 10:
            add_str = "0" + add_str
        images.append(pygame.image.load(os.path.join("assets/enemies/PNG/1", "1_enemies_1_run_0" + add_str + ".png")))
            