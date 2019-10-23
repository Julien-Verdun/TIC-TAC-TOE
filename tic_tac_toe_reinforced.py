# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 18:14:23 2019
@author: Julien Verdun
"""

from tkinter import *
from tkinter.messagebox import *
import random
import numpy as np
from time import sleep
import time
from constantes import *
import qlearning as ql
from utils import functions as fct

global t0,t1
t0 = time.time()
t1 = time.time()
# --------------------------------------------------------

global width, height
width = 400
height = 400

class ZoneAffichage(Canvas):
    def __init__(self, parent, w=width, h=height, _bg='white'):
        self.__w = w
        self.__h = h
        self.__fen_parent=parent
        Canvas.__init__(self, parent, width=w, height=h, bg=_bg, relief=RAISED, bd=5)
        self.create_rectangle(10,10,w,h,outline="black",width=2)
        self.create_line(10, h // 3, w, h // 3, fill="black", width=2)
        self.create_line(w//3, 10, w//3, h, fill="black", width=2)
        self.create_line(10, 2* h // 3, w, 2* h // 3, fill="black", width=2)
        self.create_line(2* w//3, 10, 2* w//3, h, fill="black", width=2)

class FenPrincipale(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.__instructions = Label(self)
        self.__instructions.pack(side=TOP)
        self.__instructions.config(text="Welcome on board, please start the game !")


        self.title('TIC TAC TOE REINFORCED')
        self.__zoneAffichage = ZoneAffichage(self)
        self.__zoneAffichage.pack(padx=5, pady=5)

        f1 = Frame(self)
        f1.pack(side=TOP, padx=5, pady=5)

        self.__boutonPlay = Button(self, text='Play', command=self.play).pack(side=LEFT, padx=5, pady=5)
        self.__boutonNewGame = Button(self, text='New game', command=self.new_game).pack(side=LEFT, padx=5, pady=5)
        self.__boutonExit = Button(self, text='Exit', command=self.exit).pack(side=LEFT, padx=5, pady=5)

        self.__buttons = []
        for i in range(9):
            button = MonBoutton(self, f1, '*',i)
            button.grid(row=(i // 3) + 2, column=i - 3 * (i // 3) + 2)
            self.__buttons.append(button)
            self.__buttons[i].config(command=self.__buttons[i].cliquer, state = DISABLED)
        self.__list_signs = []
        self.__list_index_signs = []

        #initialization of the first sign to play (circle for player and cross for IA)
        self.__last_sign = "circle"

        self.__real_player_sign = self.__last_sign
        #initialization of the qlearning class
        self.__qlearning = ql.qlearning("R.txt", "Q.txt", "all_possible_grid.txt", 0.8, 1, 100, 9)
        #loading the needy lists
        self.__qlearning.load_list_grid()
        self.__qlearning.load_R()
        self.__qlearning.load_Q()
        #self.__qlearning.comput_Q()
        t1 = time.time()
        print("Time to run the game : ",t1-t0)


    def exit(self):
        self.destroy()

    def play(self):
        self.__last_sign = "circle"
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
        self.__list_signs = []
        self.__list_index_signs = []

    def draw_sign(self,i):
        x1 = (i - 3 * (i // 3)) * (height // 3) + 15
        y1 = (i // 3) * (width // 3) + 15
        x2 = (i - 3 * (i // 3)) * (height // 3) + height // 3 - 10
        y2 = (i // 3) * (width // 3) + width // 3 - 10
        if self.__last_sign == 'cross':
            self.__list_signs.append([self.__zoneAffichage.create_line(x1, y1, x2, y2, fill="red", width=4),self.__zoneAffichage.create_line(x1, y2, x2, y1, fill="red", width=4)])
            self.__list_index_signs.append(i)
            self.__last_sign = "circle"
        elif self.__last_sign == 'circle':
            self.__list_signs.append(self.__zoneAffichage.create_oval(x1, y1, x2, y2, outline="green", width=4))
            self.__list_index_signs.append(i)
            self.__last_sign = "cross"

    def next_turn(self):
        if fct.is_won(self.__list_signs,self.__list_index_signs):
            self.victory()
        elif len(self.__list_signs) == 9:
            self.board_full()
        else:
            if self.__last_sign == self.__real_player_sign:
                self.__instructions.config(text="Your turn to play")
                for i in range(9):
                    if i in self.__list_index_signs :
                        self.__buttons[i].config(state=DISABLED) #est-ce necessaire
                    else:
                        self.__buttons[i].config(state=NORMAL)
            else:
                self.__instructions.config(text="Please wait for the IA to play")
                self.disable_buttons()
                self.IA_turn()

    def list_index_to_grid(self):
        # if the first one was a cross
        if type(self.__list_signs[0]) == list:
            beg = 0
        else:
            beg = 1
        # list of the index of al crosses and all circles.
        list_cross = self.__list_index_signs[beg::2]
        list_circle = self.__list_index_signs[1 - beg::2]
        grid = [0 for k in range(9)]
        for elt in list_cross:
            grid[elt] = -1
        for elt in list_circle:
            grid[elt] = 1
        return grid


    def IA_turn(self):
        if len(self.__list_index_signs) < 9:
            square_to_play = self.__qlearning.predict_move(self.list_index_to_grid())
            print("IA plays : ",square_to_play)
            time.sleep(0.5)
            self.draw_sign(square_to_play)
            self.next_turn()
        else:
            print("error,board full")

    def victory(self):
        if self.__last_sign == self.__real_player_sign:
            self.__instructions.config(text="You lose, try again")
        else:
            self.__instructions.config(text="You won, congratulations !")
        self.disable_buttons()

    def board_full(self):
        self.__instructions.config(text="The board is full, please start a new game !")
        self.disable_buttons()

    def disable_buttons(self):
        for button in self.__buttons:
            button.config(state=DISABLED)
    def normal_buttons(self):
        for button in self.__buttons:
            button.config(state=NORMAL)

class MonBoutton(Button):
    def __init__(self,fen,f,tex,i):
        Button.__init__(self,master=f,text=tex)
        self.__pos = i
        self.__t = tex
        self.fen = fen
        self.config(command = self.cliquer)
    def cliquer(self):
        """Lance la procedure de traitement a chaque clique sur une lettre """
        self.config(state = DISABLED)
        i = self.__pos
        self.fen.draw_sign(i)
        self.fen.next_turn()





# --------------------------------------------------------
if __name__ == "__main__":
    fen = FenPrincipale()
    fen.mainloop()
