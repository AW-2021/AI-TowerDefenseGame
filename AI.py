'''
This is the AI that will run the game

Verison 1: Heuristic Approach:
Heuristic:
•	Easier, less memory cosuming
•	Issue: How do we give values to the heuristic, 
•	Solution :Calculate heuristic according to current variables:

    TENTATIVE: Limit the AI to only make changes during a wave, not between waves.
    Limit the AI to only: Moves: Wait, add tower, upgrade tower
        
    *** Add a variable to every tower which states how many enemies it can kill within its radius,given the amount
    and speed of the enemies , calculated by successive runs of the game***
    
    Should AI add another tower? (default = add where the enemies are the most)
    > Number of enemies left: If number of enemies more, better to add a tower
    > All enemies near existing towers: If all enemies are near existing towers and the towers are not capable of killing the enemies, 
    better to add a tower
    > Enemies distance from end: If alot of enemies closer to end, better to add a tower
    > MAYBE: Tower radius overlapping: Better if it does not overlap
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
game_layout = np.array([(0,0,0,0,0,0,1,1,1,1,1,1,0),
(1,1,1,1,1,1,1,0,0,0,0,1,0),
(0,0,0,0,0,0,0,0,0,0,0,1,0),
(0,0,0,0,0,0,0,0,0,0,0,1,0),
(1,1,1,0,0,0,0,0,1,1,1,1,0),
(0,0,1,0,0,0,0,0,1,0,1,1,0),
(0,0,1,1,1,1,1,1,1,0,0,0,0)])


#57 possible tower positions
towerpositions = [(50, 50), (50, 150), (50, 250), (50, 350), (50, 450), (50, 550), (50, 1250), (150, 750), (150, 850), (150, 950),
                  (150, 1050), (150, 1250), (250, 50), (250, 150), (250, 250), (250, 350), (250, 450), (250, 550), (250, 650), (250, 750), 
                  (250, 850), (250, 950), (250, 1050), (250, 1250), (350, 50), (350, 150), (350, 250), (350, 350), (350, 450), (350, 550), 
                  (350, 650), (350, 750), (350, 850), (350, 950), (350, 1050), (350, 1250), (450, 350), (450, 450), (450, 550), (450, 650),
                  (450, 750), (450, 1250), (550, 50), (550, 150), (550, 350), (550, 450), (550, 550), (550, 650), (550, 750), (550, 950),
                  (550, 1250), (650, 50), (650, 150), (650, 950), (650, 1050), (650, 1150), (650, 1250)]

    
