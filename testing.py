import numpy as np
towerpositions = []

game_layout = np.array([
(0,0,0,0,0,0,1,1,1,1,1,1,0),
(1,1,1,1,1,1,1,0,0,0,0,1,0),
(0,0,0,0,0,0,0,0,0,0,0,1,0),
(0,0,0,0,0,0,0,0,0,0,0,1,0),
(1,1,1,0,0,0,0,0,1,1,1,1,0),
(0,0,1,0,0,0,0,0,1,0,1,1,0),
(0,0,1,1,1,1,1,1,1,0,0,0,0)])

for row in range(0,7):
    for column in range(0,13):
        if game_layout[row][column] == 1:
            towerpositions.append((column*100 +50,row*100 + 50))
    
print(towerpositions)