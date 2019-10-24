# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 18:14:23 2019
@author: Julien Verdun
"""

import random
import numpy as np
import time
from utils.constantes import *
from utils import functions as fct, classFile as cls
from tkinter import *
from tkinter.messagebox import *



global t0,t1
t0 = time.time()
t1 = time.time()




class FenPrincipale(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.__instructions = Label(self)
        self.__instructions.pack(side=TOP)
        self.__instructions.config(text="Welcome on board, please start the game !")

        self.title('TIC TAC TOE PVM')
        self.__zoneAffichage = cls.ZoneAffichage(self)
        self.__zoneAffichage.pack(padx=5, pady=5)

        f1 = Frame(self)
        f1.pack(side=TOP, padx=5, pady=5)

        self.__boutonPlay = Button(self, text='Play', command=self.play).pack(side=LEFT, padx=5, pady=5)
        self.__boutonNewGame = Button(self, text='New game', command=self.new_game).pack(side=LEFT, padx=5, pady=5)
        self.__boutonExit = Button(self, text='Exit', command=self.exit).pack(side=LEFT, padx=5, pady=5)

        self.__buttons = []
        for i in range(9):
            button = cls.MonBoutton(self, f1, '*',i)
            button.grid(row=(i // 3) + 2, column=i - 3 * (i // 3) + 2)
            self.__buttons.append(button)
            self.__buttons[i].config(command=self.__buttons[i].cliquer, state = DISABLED)
        self.__list_signs = []
        self.__list_index_signs = []

        #initialization of the first sign to play (circle or cross)
        self.__last_sign = "circle"

        self.__real_player_sign = self.__last_sign

        self.__depth = depth

        t1 = time.time()
        print("Time to run the game : ",t1-t0)


    def exit(self):
        self.destroy()

    def play(self):
        self.choose_sign()
        self.__real_player_sign = self.__last_sign
        self.normal_buttons()
    def new_game(self):
        self.play()
        for elt in self.__list_signs:
            if type(elt) == list:
                for line in elt:
                    self.__zoneAffichage.delete(line)
            else:
                self.__zoneAffichage.delete(elt)
        self.__instructions.config(text="New game, please start !")
        self.__list_signs = []
        self.__list_index_signs = []

    def draw_sign(self,i):
        x1 = (i - 3 * (i // 3)) * (height // 3) + 15
        y1 = (i // 3) * (width // 3) + 15
        x2 = (i - 3 * (i // 3)) * (height // 3) + height // 3 - 10
        y2 = (i // 3) * (width // 3) + width // 3 - 10
        if self.__last_sign == 'cross':
            self.__list_signs.append([self.__zoneAffichage.create_line(x1, y1, x2, y2, fill="red", width=4),self.__zoneAffichage.create_line(x1, y2, x2, y1, fill="red", width=4)])
            self.__last_sign = "circle"
        elif self.__last_sign == 'circle':
            self.__list_signs.append(self.__zoneAffichage.create_oval(x1, y1, x2, y2, outline="green", width=4))
            self.__last_sign = "cross"
        self.__list_index_signs.append(i)
        return

    def next_turn(self):
        if fct.is_won(self.__list_signs,self.__list_index_signs):
            self.victory()
        elif len(self.__list_signs) == 9:
            self.board_full()
        else:
            if self.__last_sign == self.__real_player_sign:
                self.__instructions.config(text="Let's play !")
                for i in range(9):
                    if i in self.__list_index_signs :
                        self.__buttons[i].config(state=DISABLED) #est-ce necessaire
                    else:
                        self.__buttons[i].config(state=NORMAL)
            else:
                time.sleep(0.2)
                self.disable_buttons()
                self.almost_IA_turn()



    def almost_IA_turn(self):
        if len(self.__list_index_signs) < 9:
            j = self.look_depth(self.__depth)
            if j == -1:
                free_squares = fct.freeSquares(self.__list_index_signs)
                i = free_squares[np.random.randint(0,len(free_squares))]
            #else, stop the player or win the game
            else:
                i = j
            time.sleep(0.5)
            self.draw_sign(i)
            self.next_turn()
        else:
            print("error,board full")

    def look_depth(self,depth):
        """
        Return the index of the next square that the IA should play based on the
        computation of a score for each square.
        Depending on the depth given in parameter, the index of the returned square can be
        randomly returned, computed with the available next IA moves, or even with the IA and player moves.
        """
        if depth == 0:
            #AI choose randomly
            return -1
        elif depth == 1:
            grid = fct.list_square_to_input(self.__list_signs,self.__list_index_signs) # grid translated by a 9 length vector with -1 for x 1 for o and 0 for empty squares
            score_list = self.min_max(grid)
            if np.max(score_list) == 0 and len(np.where(np.array(score_list) == 0)[0]) > 6:
                return -1
            return np.argmax(score_list)
        else :
            print("Error with the depth asked")
            return self.look_depth(1)

    def min_max(self,grid):
        score_list = [0 for k in range(9)]
        for i in range(9):
            if grid[i] != 0: # if IA can't play this square : bad score
                score_list[i] = full_square
            else: # if square empty
                grid_modif = np.copy(grid)
                if self.__real_player_sign == "circle":
                    # if player have circles (1) then IA have crosses (-1)
                    grid_modif[i] = -1
                    IA_sign = -1
                else:
                    # if player have crosses (-1) then IA have circles (1)
                    grid_modif[i] = 1
                    IA_sign = 1
                score = self.score_grid(grid_modif,IA_sign)
                score_list[i] = score
        return score_list

    def score_grid(self,grid,IA_sign):
        """
        This function takes a grid (list of 9 numbers -1 and 1 for player and IA and 0 for empty square),
        the IA number is given by parameter IA_number, and returnsthe score regarding player_sign (-1 or 1).
        """
        score = 0
        list_of_possibilites = self.build_list_of_possibilities(grid,IA_sign)
        for i in range(0,len(list_of_possibilites),2):
            if list_of_possibilites[i] == -1: #immediate_finish
                score += 50
            else: #2 aligned square
                if list_of_possibilites[i+1] == "sign": #a possibility for IA
                    score += next_victory
                else: #possibility for player
                    score += urgent_save
        return score


    def build_list_of_possibilities(self,grid,IA_sign):
        """
        Take a grid and a player sign and return the list of all
        possibilities that could be played by IA_sign.
        """
        list_sign_to_play = []
        for i in range(0,len(grid),3):
            if fct.unique_sign(grid[i:i+3]):#if the squares include similar signs or are empty
                j = fct.position_empty_square(grid[i:i+3])
                if j == -2 : #if 3 same squared aligned
                    list_sign_to_play.append(-1)
                    list_sign_to_play.append("immediate_finish")
                elif j != -1: #if 2 squared aligned and an other empty (index j)
                    list_sign_to_play.append(j+i)
                    # check the sign of a non null square
                    if j == 0:
                        sign = grid[i+1]
                    else:
                        sign = grid[i]
                    # add the kind of situation of the 3 aligned squares
                    if sign == IA_sign:
                        list_sign_to_play.append("sign")
                    else:
                        list_sign_to_play.append("other_sign")
        # for the 3 columns
        for i in range(3):
            sub_list_signs = [grid[i],grid[i+3],grid[i+6]]
            if fct.unique_sign(sub_list_signs):
                j = fct.position_empty_square(sub_list_signs)
                if j == -2 :
                    list_sign_to_play.append(-1)
                    list_sign_to_play.append("immediate_finish")
                elif j != -1:
                    list_sign_to_play.append(i+[0,3,6][j])
                    #check the sign of a non null square
                    if j == 0:
                        sign = grid[i+3]
                    else:
                        sign = grid[i]
                    # add the kind of situation of the 3 aligned squares
                    if sign == IA_sign:
                        list_sign_to_play.append("sign")
                    else:
                        list_sign_to_play.append("other_sign")
        #for diagonals
        diag1 = [2,4,6]
        signs_diag1 = [grid[k] for k in diag1]
        if fct.unique_sign(signs_diag1):
            j = fct.position_empty_square(signs_diag1)
            if j == -2:
                list_sign_to_play.append(-1)
                list_sign_to_play.append("immediate_finish")
            elif j != -1:
                list_sign_to_play.append(diag1[j])
                # check the sign of a non null square
                if j == 0:
                    sign = grid[diag1[1]]
                else:
                    sign = grid[diag1[0]]
                # add the kind of situation of the 3 aligned squares
                if sign == IA_sign:
                    list_sign_to_play.append("sign")
                else:
                    list_sign_to_play.append("other_sign")

        diag2 = [0, 4, 8]
        signs_diag2 = [grid[k] for k in diag2]
        if fct.unique_sign(signs_diag2):
            j = fct.position_empty_square(signs_diag2)
            if j == -2:
                list_sign_to_play.append(-1)
                list_sign_to_play.append("immediate_finish")
            elif j != -1:
                list_sign_to_play.append(diag2[j])
                # check the sign of a non null square
                if j == 0:
                    sign = grid[diag2[1]]
                else:
                    sign = grid[diag2[0]]
                # add the kind of situation of the 3 aligned squares
                if sign == IA_sign:
                    list_sign_to_play.append("sign")
                else:
                    list_sign_to_play.append("other_sign")
        return list_sign_to_play








    def victory(self):
        if self.__last_sign == self.__real_player_sign:
            self.__instructions.config(text="You lose, try again")
        else:
            self.__instructions.config(text="You won, congratulations !")
        self.disable_buttons()

    def board_full(self):
        self.__instructions.config(text="The board is full, please start a new game !")
        self.disable_buttons()

    def choose_sign(self):
        self.__last_sign = ["circle","cross"][np.random.randint(0,2)]



    def disable_buttons(self):
        for button in self.__buttons:
            button.config(state=DISABLED)
    def normal_buttons(self):
        for button in self.__buttons:
            button.config(state=NORMAL)










# --------------------------------------------------------
if __name__ == "__main__":
    fen = FenPrincipale()
    fen.mainloop()
