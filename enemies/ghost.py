import pygame
import os
from .enemy import Enemy

class Ghost(Enemy):
    images = []

    for x in range (20):
        add_str = str(x)
        if x < 10:
            add_str = "0" + add_str
        images.append(pygame.transform.scale(pygame.image.load(os.path.join("assets/enemies/PNG/9", "9_enemies_1_run_0" + add_str + ".png")), (64, 64) ))
            