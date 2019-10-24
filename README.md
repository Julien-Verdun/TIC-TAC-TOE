# TIC-TAC-TOE

## Description of the project

The project aims at programming the game "Tic Tac Toe" with Python. I decided to work on that project after I heard about AI on game. Especially, I read few articles about the famous Game of Go and the AlphaGo the awesome AI trained by DeepMind. This is what inspired me, I wanted to work on something similar, with my knowledge on python and reinforcment learning.


## The game 

This game is a two-player game. It consists in filling in a board, composed of 9 squares, with cross and circles depending on the camp, in order to aligned 3 identical signs.

The first player who achieve this goal wins the game. If all squares have been filled in by a sign but there are no 3 aligned squares, the game is lost for both players.
 
Three versions of the game have been implemented and are explained below. 


#### Python packages required

In order to play the game you will need the following python packages installed on you python :
- tkinter
- numpy
- time
- random
 
## The PVP version

The script of this version is included in the python file "tic_tac_toe_PVP.py". 

In this version, the basic elements of the game are programming and allow players to play in a PvP mode (Player versus Player).

![demo_PvP_version](image/tic_tac_toe_PvP.PNG)

## The PVM version

The script of this version is included in the python file "tic_tac_toe_PVM.py".

This version includes a PvM mode (Player versus Monster). The IA which controls the player's opponent uses simple methods in order to choose its next move.
Basically, it computes a score for each square, depending on the combinations with allied and enemy squares and chooses the square with the higher score. 


There is no real intelligence on this version, the IA doesn't predict or anticipate anything, it can only win or blocks the opponent when one has already 2 aligned squares.

![demo_PvM_version](image/tic_tac_toe_PvM.PNG)



## The reinforced version

The script of this version is included in the python file "tic_tac_toe_reinforced.py".

This version includes a PvM mode (Player versus Monster). The IA which controls the player's opponent is trained by **Reinforcement Learning** in order to give him the ability to anticipate the player's moves and to built a solid and efficient strategy to win the games.

The intelligence of the IA is based on the **Q-learning method**. 
- A reward matrix R is built : 
    - each line embodies a state of the tic-tac-toe grid, i-e an allowed placements of circles and crosses. There is a huge number of those placements which is counted below.
    - each column embodies an actions  for the IA. There are 9 different actions per turn which correspond to the 9 squares of the grid.
    - for a given couple (state,action), the matrix contains a score that inform whether the IA should make the action or not. The reward given to the IA are such as :
        * winning the game gives a great reward : 100 
        * losing a game gives a bad reward : -10
        * defending and preventing a game from the defeat gives an average reward : 10
        * otherwise the reward is : -1
    

- Then, we compute the optimal Q matrix this way (first initialise to 0 matrix), for a given number of episode (the bigger the better) : 
    - a possible state is randomly choosen
    - while the game is not ended one way or another :
        - regarding the rewards that could be got, the next action is choosen
        - for the corresponding state, we compute the maximal value of Q and update the Q matrix


With the trained Q matrix, we can predict the next move AI should do to maximise its chances to win the game. 


![demo_reinforced_version](image/tic_tac_toe_reinforced.PNG)










# Enjoy the game 