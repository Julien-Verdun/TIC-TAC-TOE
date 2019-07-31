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


"""


from tkinter import *
from tkinter.messagebox import *
import random
import numpy as np
from time import sleep
import time
import neural_network as neural_network_class


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

        self.__gameMode = Label(self)
        self.__gameMode.pack(side=TOP)
        self.__gameMode.config(text="Game mode : classic_PvM")

        self.title('TIC TAC TOE PLUS')
        self.__zoneAffichage = ZoneAffichage(self)
        self.__zoneAffichage.pack(padx=5, pady=5)

        f1 = Frame(self)
        f1.pack(side=TOP, padx=5, pady=5)

        self.__boutonPlay = Button(self, text='Play', command=self.play).pack(side=LEFT, padx=5, pady=5)
        self.__boutonNewGame = Button(self, text='New game', command=self.new_game).pack(side=LEFT, padx=5, pady=5)
        self.__boutonModePvP = Button(self, text='PvP mode', command=self.modePvP).pack(side=LEFT, padx=5, pady=5)
        self.__boutonModeClassicPvM = Button(self, text='Classic PvM mode', command=self.mode_classic_PvM).pack(side=LEFT, padx=5, pady=5)
        self.__boutonModeNNPvM = Button(self, text='NN PvM mode', command=self.mode_NN_PvM).pack(side=LEFT, padx=5,pady=5)
        self.__boutonTrainNN = Button(self, text='Train NN', command=self.trainNN).pack(side=LEFT, padx=5, pady=5)
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

        #initialization of the mode (PvP or PvM)
        self.__mode = "classic_PvM"

        self.__nn = neural_network_class.NeuralNetwork()

        self.__game_recorder = neural_network_class.Game_recorder("record_games.JSON")

        t1 = time.time()
        print("Time to run the game : ",t1-t0)


    def exit(self):
        self.destroy()
    def play(self):
        self.choose_sign()
        if self.__mode == "classic_PvM" or self.__mode == "NN_PvM":
            self.__real_player_sign = self.__last_sign
        for button in self.__buttons:
            button.config(state=NORMAL)
        if self.__mode == "PvP":
            instruction_text = "Let's play the game ! Player " + self.__last_sign + " you start !"
        else:
            instruction_text = "Let's play the game ! Your turn to play !"
        self.__instructions.config(text=instruction_text)
    def new_game(self):
        self.choose_sign()
        if self.__mode == "classic_PvM" or self.__mode == "NN_PvM":
            self.__real_player_sign = self.__last_sign
        if self.__mode == "PvP":
            instruction_text = "Let's play the game ! Player " + self.__last_sign + " you start !"
        else:
            instruction_text = "Let's play the game ! Your turn to play !"
        self.__instructions.config(text = instruction_text)
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
        if self.__mode == "PvP":
            self.next_turn_PvP()
        else :
            self.next_turn_PvM(self.__mode)

    def next_turn_PvP(self):
        if self.is_won():
            self.victory()

        elif len(self.__list_signs) == 9:
            self.__instructions.config(text="The board is full, please start a new game !")
        else:
            self.__instructions.config(text="Well played, player {} it's your turn".format(self.__last_sign))

    def next_turn_PvM(self,mode):
        if self.is_won():
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
                for button in self.__buttons:
                    button.config(state=DISABLED)
                if mode == "classic_PvM":
                    self.almost_IA_turn()
                else :
                    self.IA_turn()

    def almost_IA_turn(self):
        if len(self.__list_index_signs) < 9:
            #get the critical squre to play
            i = self.look_around()
            #if no 2 square aligned for player or for IA, play randomly
            if i == -1:
                i = np.random.randint(0, 9)
                while i in self.__list_index_signs:
                    i = np.random.randint(0, 9)
            #else, stop the player or win the game
            else:
                print("Smart move")
            time.sleep(0.5)
            self.draw_sign(i)
            self.next_turn()
        else:
            print("error,board full")

    def IA_turn(self):
        if len(self.__list_index_signs) < 9:
            i = self.__nn.predict_square(np.array(self.list_square_to_input()))
            print("IA predict : ", i)
            time.sleep(0.5)
            self.draw_sign(i)
            self.next_turn()
        else:
            print("error,board full")

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
        list_signs = self.list_square_to_input(self.__list_index_signs)
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
        nb_null = 0
        for elt in list:
            if elt == 0:
                nb_null += 1
        if nb_null != 1:#si plus d'une case vide sur les trois
            return -1
        else:#une unique case vide, on renvoie son index
            return list.index(0)

    def trainNN(self):
        self.__nn.train_neural_network()

    def victory(self):
        if self.__mode == "classic_PvM" or self.__mode == "NN_PvM":
            if self.__last_sign == self.__real_player_sign:
                self.__instructions.config(text="You lose, try again")
                data = {}
                data["board_values"] = self.list_square_to_input()
                data["end_state"] =  "IA_victory"
                self.__game_recorder.add_game(data)
            else:
                self.__instructions.config(text="You won, congratulations !")
                data = {}
                data["board_values"] = self.list_square_to_input()
                data["end_state"] = "Player_victory"
                self.__game_recorder.add_game(data)
        else :
            if self.__last_sign == 'circle':
                self.__instructions.config(text="Player CROSS, congratulations !! You won")
            else:
                self.__instructions.config(text="Player CIRCLE, congratulations !! You won")
        for button in self.__buttons:
            button.config(state=DISABLED)

    def board_full(self):
        self.__instructions.config(text="The board is full, please start a new game !")
        if self.__mode == "classic_PvM" or self.__mode == "NN_PvM":
            data = {}
            data["board_values"] = self.list_square_to_input()
            data["end_state"] = "null"
            self.__game_recorder.add_game(data)

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

    def choose_sign(self):
        self.__last_sign = ["circle","cross"][np.random.randint(0,2)]

    def modePvP(self):
        self.__mode = "PvP"
        self.__gameMode.config(text="Game mode : {}".format(self.__mode))

    def mode_classic_PvM(self):
        self.__mode = "classic_PvM"
        self.__gameMode.config(text="Game mode : {}".format(self.__mode))

    def mode_NN_PvM(self):
        self.__mode = "NN_PvM"
        self.__gameMode.config(text="Game mode : {}".format(self.__mode))

    def list_square_to_input(self,input=[]):
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
