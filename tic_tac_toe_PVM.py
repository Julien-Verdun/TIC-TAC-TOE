# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 18:14:23 2019
@author: Julien Verdun
"""


"""
TO-DO LIST

Choix aleatoire du joueur qui commence


Entrainement de l'IA : trouver comment générer et sous quelle forme générer les données d'apprentissage

Modifier les données sauvegardées afin d'avoir des données exploitables pour l'entrainement
Sauvegarde pour chaque mouvement :
- du damier +1 0 -1
- du prochain mouvement, signe et case
- du résultat finale appliqué à la fin de la partie à chaque ligne issues de la partie


attendre la fin de la partie avant de les enregistrer pour donner le resultat

Mettre en place un index et un sous index dans les JSON pour suivre les parties
Verifier qu'on enregistre aussi les mouvements du joueur.

"""


from tkinter import *
from tkinter.messagebox import *
import random
import numpy as np
from time import sleep
import time
import game_recorder as game_recorder
from constantes import *



global t0,t1
t0 = time.time()
t1 = time.time()
# --------------------------------------------------------



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

        self.title('TIC TAC TOE PVM')
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

        #initialization of the first sign to play (circle or cross)
        self.__last_sign = "circle"

        self.__real_player_sign = self.__last_sign

        self.__depth = depth

        self.__list_turn_record = []

        self.__game_recorder = game_recorder.Game_recorder("record_games.JSON")

        self.__index = self.__game_recorder.get_index()

        self.__sub_index = 0
        t1 = time.time()
        print("Time to run the game : ",t1-t0)


    def exit(self):
        self.destroy()

    def play(self):
        self.choose_sign()
        self.__real_player_sign = self.__last_sign
        for button in self.__buttons:
            button.config(state=NORMAL)
    def new_game(self):
        self.__index += 1
        self.choose_sign()
        self.__real_player_sign = self.__last_sign
        for button in self.__buttons:
            button.config(state=NORMAL)
        for elt in self.__list_signs:
            if type(elt) == list:
                for line in elt:
                    self.__zoneAffichage.delete(line)
            else:
                self.__zoneAffichage.delete(elt)
        self.__list_signs = []
        self.__list_index_signs = []
        self.__instructions.config(text="New game, please start !")

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
        self.add_turn_to_record()
        self.__sub_index += 1
        if self.is_won():
            self.victory()
            self.add_turn_to_record()
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
                for button in self.__buttons:
                    button.config(state=DISABLED)
                self.almost_IA_turn()
                self.add_turn_to_record()


    def almost_IA_turn(self):
        if len(self.__list_index_signs) < 9:
            #get the critical squre to play
            #j = self.look_around()
            j = self.look_depth(self.__depth)
            #print("IA choose index : ", j)
            #if no 2 square aligned for player or for IA, play randomly
            if j == -1:
                i = np.random.randint(0, 9)
                while i in self.__list_index_signs:
                    i = np.random.randint(0, 9)
            #else, stop the player or win the game
            else:
                #print("Smart move")
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
            return -1
        elif depth == 1:
            grid = self.list_square_to_input() # grid translated by a 9 length vector with -1 for x 1 for o and 0 for empty squares
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
        print("List of score : ", score_list)
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

        #print("Grid : ",grid)
        #print("List of IA possible moves : ", list_of_possibilites)

        return score


    def build_list_of_possibilities(self,grid,IA_sign):
        """
        Take a grid and a player sign and return the list of all
        possibilities that could be played by IA_sign.
        """
        list_sign_to_play = []
        for i in range(0,len(grid),3):
            if self.unique_sign(grid[i:i+3]):#if the squares include similar signs or are empty
                j = self.position_empty_square(grid[i:i+3])
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
            if self.unique_sign(sub_list_signs):
                j = self.position_empty_square(sub_list_signs)
                print("j = ",j)
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
        if self.unique_sign(signs_diag1):
            j = self.position_empty_square(signs_diag1)
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
        if self.unique_sign(signs_diag2):
            j = self.position_empty_square(signs_diag2)
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



    def look_around(self):
        """
        The function is looking for 2 aligned signs that could let the player win during
        the next game or 2 aligned signs that could be completed by a third one in order
        to the IA to win the game.
        The function create a list of all critical squares (that could be a threat or an opportunity)
        and then choose the more critical square by giving priority to the defense better than to the attack.
        The function returns then the index of the square that IA should play.
        """
        #defining the IA sign
        if self.__real_player_sign == "circle":
            IA_sign = -1 # "cross"
        else:
            IA_sign = 1 #"circle"
        list_sign_to_play = []
        #list of the sign convert to -1 0 and 1
        list_signs = self.list_square_to_input()
        # for the 3 lines
        for i in range(0,len(self.__list_index_signs),3):
            if self.unique_sign(list_signs[i:i+3]):#if the squares include similar signs or are empty
                j = self.position_empty_square(list_signs[i:i+3])
                if j != -1:
                    list_sign_to_play.append(j+i)
                    # check the sign of a non null square
                    if j == 0:
                        sign = list_signs[i+1]
                    else:
                        sign = list_signs[i]
                    # add the kind of situation of the 3 aligned squares
                    if sign == IA_sign :
                        list_sign_to_play.append("Attacking")
                    else:
                        list_sign_to_play.append("Defending")
                    print("Critical square : ")
                    print(list_sign_to_play[-2:])
        # for the 3 columns
        for i in range(3):
            sub_list_signs = [list_signs[i],list_signs[i+3],list_signs[i+6]]
            if self.unique_sign(sub_list_signs):
                j = self.position_empty_square(sub_list_signs)
                if j != -1:
                    list_sign_to_play.append(i+[0,3,6][j])
                    #check the sign of a non null square
                    if j == 0:
                        sign = list_signs[i+3]
                    else:
                        sign = list_signs[i]
                    # add the kind of situation of the 3 aligned squares
                    if sign == IA_sign:
                        list_sign_to_play.append("Attacking")
                    else:
                        list_sign_to_play.append("Defending")
                    print("Critical square : ")
                    print(list_sign_to_play[-2:])
        #for diagonals
        diag1 = [2,4,6]
        signs_diag1 = [list_signs[k] for k in diag1]
        if self.unique_sign(signs_diag1):
            j = self.position_empty_square(signs_diag1)
            if j != -1:
                list_sign_to_play.append(diag1[j])
                # check the sign of a non null square
                if j == 0:
                    sign = list_signs[diag1[1]]
                else:
                    sign = list_signs[diag1[0]]
                # add the kind of situation of the 3 aligned squares
                if sign == IA_sign:
                    list_sign_to_play.append("Attacking")
                else:
                    list_sign_to_play.append("Defending")
                print("Critical square : ")
                print(list_sign_to_play[-2:])
        diag2 = [0, 4, 8]
        signs_diag2 = [list_signs[k] for k in diag2]
        if self.unique_sign(signs_diag2):
            j = self.position_empty_square(signs_diag2)
            if j != -1:
                list_sign_to_play.append(diag2[j])
                # check the sign of a non null square
                if j == 0:
                    sign = list_signs[diag2[1]]
                else:
                    sign = list_signs[diag2[0]]
                #add the kind of situation of the 3 aligned squares
                if sign == IA_sign:
                    list_sign_to_play.append("Attacking")
                else:
                    list_sign_to_play.append("Defending")
                print("Critical square : ")
                print(list_sign_to_play[-2:])
        # we now have the list of critical squares and the information, filled in this square is
        # a defense strategy or an attack strategy, we must choose the more critical one
        if len(list_sign_to_play) == 0:
            print("No free square")
            return -1
        elif len(list_sign_to_play) == 2:
            print("one free square : ", list_sign_to_play)
            return list_sign_to_play[0]
        else:
            if "Attacking" not in list_sign_to_play:
                print("Square defended : ", list_sign_to_play[0:2])
                return list_sign_to_play[0]
            else:
                print("Square attacked : ", list_sign_to_play[list_sign_to_play.index("Attacking")-1:list_sign_to_play.index("Attacking")+1])
                return list_sign_to_play[list_sign_to_play.index("Attacking")-1]


    def unique_sign(self,list):
        #check if on the variable list there are only signs with the same symbol or empty square.
        sign = list[0]
        for i in range(1,len(list)):
            if list[i] != 0 and list[i] != sign :
                return False
        return True

    def position_empty_square(self,list):
        """
        If there are more than one or no empty squares among the 3 squares defined by list
        the function returns -1, else it returns the index of the empty square.
        """
        print(list)
        list_null = np.where(np.array(list) == 0)[0]
        print(list_null)
        if len(list_null) == 0:  # si aucune case vide
            return -2
        elif len(list_null) == 1:  # si une case vide sur les trois
            return list_null[0]
            # return list.index(0)
        else:  # plus d'une case vide (2 ou 3)
            return -1


    def victory(self):
        if self.__last_sign == self.__real_player_sign:
            self.__instructions.config(text="You lose, try again")
            self.record_data("IA_victory")
        else:
            self.__instructions.config(text="You won, congratulations !")
            self.record_data("Player_victory")
        for button in self.__buttons:
            button.config(state=DISABLED)

    def board_full(self):
        self.__instructions.config(text="The board is full, please start a new game !")
        self.record_data("null")

    def is_won(self):
        if len(self.__list_signs) <= 4:
            return False
        #if the first one was a cross
        if type(self.__list_signs[0]) == list:
            beg = 0
        else :
            beg = 1
        #list of the index of al crosses and all circles.
        list_cross = self.__list_index_signs[beg::2]
        list_circle = self.__list_index_signs[1-beg::2]

        #sorting of the list
        list_cross = np.sort(list_cross)
        list_circle = np.sort(list_circle)

        #check if there are 3 aligned signs
        if len(list_cross) >= 3:
            for i in range(0,len(list_cross)-2):
                #Check if 3 aligned cross on the lines
                if (list_cross[i] == 0 or list_cross[i] == 3 or list_cross[i] == 6) and list_cross[i]==list_cross[i+1]-1==list_cross[i+2]-2:
                    return True
                # Check if 3 aligned cross on the columns
                if (list_cross[i] == 0 or list_cross[i] == 1 or list_cross[i] == 2) and ((list_cross[i]+3) in list_cross) and ((list_cross[i]+6) in list_cross):
                    return True
                # Check if 3 aligned cross on the first diag
                if list_cross[i] == 0 and (list_cross[i]+4) in list_cross and (list_cross[i]+8) in list_cross:
                    return True
                # Check if 3 aligned cross on the second diag
                if list_cross[i] == 2 and (list_cross[i]+2) in list_cross and (list_cross[i]+4) in list_cross:
                    return True
        if len(list_circle) >= 3:
            for i in range(0,len(list_circle)-2):
                #Check if 3 aligned circle on the lines
                if (list_circle[i] == 0 or list_circle[i] == 3 or list_circle[i] == 6) and list_circle[i]==list_circle[i+1]-1==list_circle[i+2]-2:
                    return True
                # Check if 3 aligned circle on the columns
                if (list_circle[i] == 0 or list_circle[i] == 1 or list_circle[i] == 2) and ((list_circle[i]+3) in list_circle) and ((list_circle[i]+6) in list_circle):
                    return True
                # Check if 3 aligned circle on the first diag
                if list_circle[i] == 0 and (list_circle[i]+4) in list_circle and (list_circle[i]+8) in list_circle:
                    return True
                # Check if 3 aligned circle on the second diag
                if list_circle[i] == 2 and (list_circle[i]+2) in list_circle and (list_circle[i]+4) in list_circle:
                    return True
        return False

    def add_turn_to_record(self):
        data = {}
        data["index"] = self.__index # avec un index par partie et un sous index index par mouvement
        data["sub_index"] = self.__sub_index
        data["board_values"] = self.list_square_to_input()
        if self.__last_sign == self.__real_player_sign:
            data["player"] = "IA"
        else:
            data["player"] = "real_player"
        self.__list_turn_record.append(data)

    def record_data(self,result):
        for data in self.__list_turn_record:
            data["end_state"] = result
            self.__game_recorder.add_game(data)

    def choose_sign(self):
        self.__last_sign = ["circle","cross"][np.random.randint(0,2)]

    def list_square_to_input(self):
        """
        Take the list of squares fill in by a sign and create a 9x1
        array (input_layer for neural network) with values -1 for a cross,
        0 if empty square and 1 for a circle.
        """
        input_layer = [0 for k in range(9)]
        for i in range(len(self.__list_signs)):
            if type(self.__list_signs[i]) == list:
                input_layer[self.__list_index_signs[i]] = -1
            else:
                input_layer[self.__list_index_signs[i]] = 1
        return input_layer






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
