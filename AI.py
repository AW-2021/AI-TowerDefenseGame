'''
This is the AI that will run the game

Version 2 - Heuristic Approach:
HEURISTIC:
•	Easier, less memory consuming
•	Issue: How do we give values to the heuristic, 
•	Solution :Calculate heuristic according to current variables:

    TENTATIVE: Limit the AI to only make changes during a wave, not between waves.
    Limit the AI to only: Moves: Wait, add tower, upgrade tower
        
    *** Add a variable to every tower which states how many enemies it can kill within its radius,given the amount
    and speed of the enemies , calculated by successive runs of the game***
    
    Should AI add another tower? (default = add where the enemies are the most)
    > Number of enemies left: If number of enemies more, better to add a tower
    > All enemies near existing towers: If all enemies are near existing towers and the towers are not capable of 
        killing the enemies, better to add a tower
    > Enemies distance from end: If alot of enemies closer to end, better to add a tower
    > Tower radius overlapping: Better if it does not overlap
    > How much of the road does this position cover: Better if more road is covered
    
    
Game layout

|   0   0   0   0   0   0   1   1   1   1   1   1   0   |
|   1   1   1   1   1   1   1   0   0   0   0   1   0   |
|   0   0   0   0   0   0   0   0   0   0   0   1   0   |
|   0   0   0   0   0   0   0   0   0   0   0   1   0   |
|   1   1   1   0   0   0   0   0   1   1   1   1   0   |
|   0   0   1   0   0   0   0   0   1   0   1   1   0   |
|   0   0   1   1   1   1   1   1   1   0   0   0   0   |

'''

import numpy as np
import pygame
import os
from enemies.scorpion import Scorpion
from enemies.wizard import Wizard
from enemies.ogre import Ogre
from towers.archerTower import ArcherTowerLong, ArcherTowerShort
from towers.supportTower import DamageTower, RangeTower
from menu.menu import VerticalMenu, PlayPauseButton
import time
import random
import math
pygame.font.init()
pygame.init()


# Grid layout of the game , 1 is path , 0 is free space

game_layout = np.array([
(0,0,0,0,0,0,1,1,1,1,1,1,0),
(1,1,1,1,1,1,1,0,0,0,0,1,0),
(0,0,0,0,0,0,0,0,0,0,0,1,0),
(0,0,0,0,0,0,0,0,0,0,0,1,0),
(1,1,1,0,0,0,0,0,1,1,1,1,0),
(0,0,1,0,0,0,0,0,1,0,1,1,0),
(0,0,1,1,1,1,1,1,1,0,0,0,0)])


# 57 possible tower positions
towerpositions = [(50, 50), (150, 50), (250, 50), (350, 50), (450, 50), (550, 50), (1250, 50), (750, 150), (850, 150), (950, 150), (1050, 150),
                   (1250, 150), (50, 250), (150, 250), (250, 250), (350, 250), (450, 250), (550, 250), (650, 250), (750, 250), (850, 250), 
                   (950, 250), (1050, 250), (1250, 250), (50, 350), (150, 350), (250, 350), (350, 350), (450, 350), (550, 350), (650, 350), 
                   (750, 350), (850, 350), (950, 350), (1050, 350), (1250, 350), (350, 450), (450, 450), (550, 450), (650, 450), (750, 450),
                   (1250, 450), (50, 550), (150, 550), (350, 550), (450, 550), (550, 550), (650, 550), (750, 550), (950, 550), (1250, 550),
                   (50, 650), (150, 650), (950, 650), (1050, 650), (1150, 650), (1250, 650)]
path_positions =[(650, 50), (750, 50), (850, 50), (950, 50), (1050, 50), (1150, 50), (50, 150), (150, 150), (250, 150), (350, 150), 
                 (450, 150), (550, 150), (650, 150), (1150, 150), (1150, 250), (1150, 350), (50, 450), (150, 450), (250, 450),
                 (850, 450), (950, 450), (1050, 450), (1150, 450),(250, 550), (850, 550), (1050, 550), (1150, 550), (250, 650), 
                 (350, 650), (450, 650), (550, 650), (650, 650), (750, 650), (850, 650)]


lives_img = pygame.image.load(os.path.join("game_assets","heart.png")).convert_alpha()
star_img = pygame.image.load(os.path.join("game_assets","star.png")).convert_alpha()
side_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","side.png")).convert_alpha(), (120, 500))

buy_archer = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","buy_archer_4.png")).convert_alpha(), (75, 75))
buy_archer_2 = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","buy_archer_5.png")).convert_alpha(), (75, 75))
#buy_damage = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","buy_damage.png")).convert_alpha(), (75, 75))
#buy_range = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","buy_range.png")).convert_alpha(), (75, 75))

play_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","button_start.png")).convert_alpha(), (75, 75))
pause_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","button_pause.png")).convert_alpha(), (75, 75))

sound_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","button_sound.png")).convert_alpha(), (75, 75))
sound_btn_off = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","button_sound_off.png")).convert_alpha(), (75, 75))

wave_bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assets","wave.png")).convert_alpha(), (225, 75))

attack_tower_names = ["archer", "archer2"]
support_tower_names = ["range", "damage"]

# waves are in form
# frequency of enemies
# (# scorpions, # wizards, # ogre)
waves = [
    [20, 0, 0],
    [50, 0, 0],
    [100, 0, 0],
    [0, 20, 0],
    [0, 50, 0],
    [0, 100, 0],
    [20, 100, 5],
    [50, 100, 10],
    [100, 100, 25],
    [0, 0, 50],
    [20, 0, 100],
    [20, 0, 150],
    [200, 100, 200],
]

class Game:
    def __init__(self, win):
        self.width = 1350
        self.height = 700
        self.win = win
        self.enemys = []
        self.attack_towers = []
        self.support_towers = []
        self.tower_list = []
        self.lives = 10
        self.money = 2000
        self.bg = pygame.image.load(os.path.join("game_assets", "bg.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.timer = time.time()
        self.life_font = pygame.font.SysFont("comicsans", 40)
        self.selected_tower = None
        self.menu = VerticalMenu(self.width - side_img.get_width() + 70, 250, side_img)
        self.menu.add_btn(buy_archer, "buy_archer", 500)
        self.menu.add_btn(buy_archer_2, "buy_archer_2", 750)
        #self.menu.add_btn(buy_damage, "buy_damage", 1000)
        #self.menu.add_btn(buy_range, "buy_range", 1000)
        self.moving_object = None
        self.wave = 0
        self.current_wave = waves[self.wave][:]
        self.pause = True
        self.music_on = True
        self.playPauseButton = PlayPauseButton(play_btn, pause_btn, 10, self.height - 85)
        self.soundButton = PlayPauseButton(sound_btn, sound_btn_off, 90, self.height - 85)
        self.lose = True
        tower_list = []

    def gen_enemies(self):
        """
        generate the next enemy or enemies to show
        :return: enemy
        """
        if sum(self.current_wave) == 0:
            if len(self.enemys) == 0:
                self.wave += 1
                self.current_wave = waves[self.wave]
                self.pause = True
                self.playPauseButton.paused = self.pause
        else:
            wave_enemies = [Scorpion(),Wizard(), Ogre()]
            for x in range(len(self.current_wave)):
                if self.current_wave[x] != 0:
                    self.enemys.append(wave_enemies[x])
                    self.current_wave[x] = self.current_wave[x] - 1
                    break

    def run(self):
        #pygame.mixer.music.play(loops=-1)
        run = True
        clock = pygame.time.Clock()
        # tower_list = []
        while run:
            clock.tick(100)

            if self.pause == False:
                # generate monsters
                if time.time() - self.timer >= random.randrange(1,6)/3:
                    self.timer = time.time()
                    self.gen_enemies()

            pos = pygame.mouse.get_pos()
            
            # main event loop below
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONUP:
                    # check for play or pause
                    if self.playPauseButton.click(pos[0], pos[1]):
                        self.pause = not(self.pause)
            # loop through enemies
            if not self.pause:
                to_del = []
                for en in self.enemys:
                    en.move()
                    if en.x < -15:
                        to_del.append(en)

                # delete all enemies off the screen
                for d in to_del:
                    self.lives -= 1
                    self.enemys.remove(d)

                # loop through attack towers
                for tw in self.attack_towers:
                    self.money += tw.attack(self.enemys)

                # loop through attack towers
                for tw in self.support_towers:
                    tw.support(self.attack_towers)

                # if you lose
                if self.lives <= 0:
                    self.lose = True
                    print("You Lost! :(")
                    run = False
               
                        
            ##################################################################
            #        AI WORKING 
            ##################################################################
            
            numberOfEnemies = len(self.enemys)
            placeTower = False # bool - should we buy a tower or not
            
            # self.assignWeightHeuristics(placeTower, playerLife = self.lives, currentMoney = self.money, filledPositions = self.tower_list)
            self.add_tower(placeTower)
            self.draw()

        

    def add_tower(self, placeTower):
        flag_tower750 = False

        # AI inner working, should we buy tower or not , and the x and y calculation
        if self.money > 500:
            
            max_combined = 0
            weightList = []
            bestPos = []

            # Loop through all tower positions & check which position is the best option
            for position in towerpositions: # Check which positions are closest to path

                # Looping through path positions for each tower position & counting no. of path pieces right next to tower
                numberOfOneHopPathPieces = 0
                for pathCoordinate in path_positions:
                    if distance(position,pathCoordinate) < 145: # Each square in the grid is almost 100 px
                        numberOfOneHopPathPieces += 1
                
                bestPos.append(numberOfOneHopPathPieces)

                # ASSIGN POSITION WEIGHTS BASED ON NO. OF PATH PIECES 1 HOP AWAY FROM CURRENT TOWER POSITION
                if numberOfOneHopPathPieces >= 4:
                    positionWeight = 5
                elif numberOfOneHopPathPieces == 3:
                    positionWeight = 4
                elif numberOfOneHopPathPieces == 2:
                    positionWeight = 3
                elif numberOfOneHopPathPieces == 1:
                    positionWeight = 2
                elif numberOfOneHopPathPieces == 0:
                    positionWeight = 1

                # COUNT NO. OF NEIGHBOURS FOR EACH TOWER POSITION & ASSIGN (NEIGHBOUR) WEIGHTS
                neighbour_count = 0
                for tower in self.tower_list:
                    if distance(position,tower) < 145: # Each square in the grid is 100 px
                        neighbour_count += 1
                if neighbour_count == 0:
                    neighbourWeight = 2
                elif neighbour_count == 1:
                    neighbourWeight = 1
                if neighbour_count >= 2:
                    neighbourWeight = 0
        
                weightList.append([positionWeight, neighbourWeight]) 
            
            combinedWeightList = []
            for weights in weightList:
                combinedWeightList.append(weights[0] * weights[1])
            
            max_combined = max(combinedWeightList)
            if max_combined ==  0:
                flag_tower750 = True
            
            place = combinedWeightList.index(max_combined)
            x = (towerpositions[place])[0]
            y = (towerpositions[place])[1]
                
            
            if flag_tower750:
                if self.money >= 750:
                    if bestPos[place] != 0:
                        self.attack_towers.append(ArcherTowerShort(x,y))
                        self.money -= 750
                    else:
                        self.attack_towers.append(ArcherTowerLong(x,y))
                        self.money -= 750

                    del towerpositions[place]
                    del combinedWeightList[place]
                    del weightList[place]
                    placeTower = True   

                else:
                    placeTower = False
            else:
                self.attack_towers.append(ArcherTowerLong(x,y))
                self.money -= 500

                del towerpositions[place]
                del combinedWeightList[place]
                del weightList[place]
                placeTower = True

            if placeTower:
                self.tower_list.append([x,y])
                


    def draw(self):
        
        self.win.blit(self.bg, (0,0))
        #draw grid:
        #for linex in range(00,1351):
        linex=100
        pygame.draw.line(self.win,(255,255,255),(linex,0),(linex,700),1)
        pygame.draw.line(self.win,(255,255,255),(0,linex),(1350,linex),1)
        linex = linex +100
        pygame.draw.line(self.win,(255,255,255),(linex,0),(linex,700),1)
        pygame.draw.line(self.win,(255,255,255),(0,linex),(1350,linex),1)
        linex = linex +100
        pygame.draw.line(self.win,(255,255,255),(linex,0),(linex,700),1)
        pygame.draw.line(self.win,(255,255,255),(0,linex),(1350,linex),1)
        linex = linex +100
        pygame.draw.line(self.win,(255,255,255),(linex,0),(linex,700),1)
        pygame.draw.line(self.win,(255,255,255),(0,linex),(1350,linex),1)
        linex = linex +100
        pygame.draw.line(self.win,(255,255,255),(linex,0),(linex,700),1)
        pygame.draw.line(self.win,(255,255,255),(0,linex),(1350,linex),1)
        linex = linex +100
        pygame.draw.line(self.win,(255,255,255),(linex,0),(linex,700),1)
        pygame.draw.line(self.win,(255,255,255),(0,linex),(1350,linex),1)
        linex = linex +100
        pygame.draw.line(self.win,(255,255,255),(linex,0),(linex,700),1)
        pygame.draw.line(self.win,(255,255,255),(0,linex),(1350,linex),1)
        linex = linex +100
        pygame.draw.line(self.win,(255,255,255),(linex,0),(linex,700),1)
        pygame.draw.line(self.win,(255,255,255),(0,linex),(1350,linex),1)
        linex = linex +100
        pygame.draw.line(self.win,(255,255,255),(linex,0),(linex,700),1)
        linex = linex +100
        pygame.draw.line(self.win,(255,255,255),(linex,0),(linex,700),1)
        linex = linex +100
        pygame.draw.line(self.win,(255,255,255),(linex,0),(linex,700),1)
        linex = linex +100
        pygame.draw.line(self.win,(255,255,255),(linex,0),(linex,700),1)
        linex = linex +100
        pygame.draw.line(self.win,(255,255,255),(linex,0),(linex,700),1)
        linex = linex +100
        pygame.draw.line(self.win,(255,255,255),(linex,0),(linex,700),1)
        linex = linex +100
        
        
        # draw placement rings
        if self.moving_object:
            for tower in self.attack_towers:
                tower.draw_placement(self.win)

            for tower in self.support_towers:
                tower.draw_placement(self.win)

            self.moving_object.draw_placement(self.win)

        # draw attack towers
        for tw in self.attack_towers:
            tw.draw(self.win)
            #tw.draw_radius(self.win)

        # draw support towers
        for tw in self.support_towers:
            tw.draw(self.win)

        # draw enemies
        for en in self.enemys:
            en.draw(self.win)

        # redraw selected tower
        if self.selected_tower:
            self.selected_tower.draw(self.win)

        # draw moving object
        if self.moving_object:
            self.moving_object.draw(self.win)

        # draw menu
        self.menu.draw(self.win)

        # draw play pause button
        self.playPauseButton.draw(self.win)

        # draw music toggle button
        self.soundButton.draw(self.win)

        # draw lives
        text = self.life_font.render(str(self.lives), 1, (255,255,255))
        life = pygame.transform.scale(lives_img,(50,50))
        start_x = self.width - life.get_width() - 10

        self.win.blit(text, (start_x - text.get_width() - 10, 10))
        self.win.blit(life, (start_x, 10))

        # draw money
        text = self.life_font.render(str(self.money), 1, (255, 255, 255))
        money = pygame.transform.scale(star_img, (50, 50))
        start_x = self.width - life.get_width() - 10

        self.win.blit(text, (start_x - text.get_width() - 10, 70))
        self.win.blit(money, (start_x, 65))

        # draw wave
        #self.win.blit(wave_bg, (10,10))
        text = self.life_font.render("Wave #" + str(self.wave), 1, (255,255,255))
        self.win.blit(text, (10 , 20))

        pygame.display.update()

    
        
# To calculate Euclidean distance between any two points on the grid.
# Right now we're passing current tower position and path position    
def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)