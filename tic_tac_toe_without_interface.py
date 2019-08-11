import random
import numpy as np
import time


global t0,t1
t0 = time.time()
t1 = time.time()
# --------------------------------------------------------

global width, height
width = 400
height = 400





class TicTacToe:
    def __init__(self,width = width, height = height):
        self.__width = width
        self.__height = height
        self.__grid = np.zeros((width,height))-1

    def display_grid(self):
        print("--------")
        for i in range(self.__grid[0]):
            line = "|"
            for j in range(self.__grid[1]):
                line += ["x","o"," "][self.__grid[i,j]]
                line += "|"
            print(line)
            print("--------")


    def player_entry(self):
        player_entry = int(input("Entrer the number of square you want to fill"))
        if self.__grid[i,j] == -1:
                    player_entry = int(input("Entrer the number of square you want to fill"))


game = TicTacToe()

continuer = 1

while continuer == 1:
