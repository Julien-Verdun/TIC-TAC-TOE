# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 18:14:23 2019
@author: Julien Verdun
"""


"""
TO-DO LIST

Reinforcement learning
- on fait jouer aléatoirement une partie
- chaque fois qu'on gagne une partie on récompense ?








Sauvegarde pour chaque mouvement :
- du damier +1 0 -1
- du prochain mouvement, signe et case
- du résultat finale appliqué à la fin de la partie à chaque ligne issues de la partie


Mettre en place un index et un sous index dans les JSON pour suivre les parties
Verifier qu'on enregistre aussi les mouvements du joueur.




"""


from tkinter import *
from tkinter.messagebox import *
import random
import numpy as np
from time import sleep
import time
import neural_network_trained as neural_network_class


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

        self.__list_turn_record = []

        self.__nn = neural_network_class.NeuralNetwork()

        self.__game_recorder = neural_network_class.Game_recorder("record_games.JSON")

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
                self.IA_turn()
        self.add_turn_to_record()

    def IA_turn(self):
        if len(self.__list_index_signs) < 9:
            i = self.__nn.predict_square(np.array(self.list_square_to_input()))
            print("IA predict : ", i)
            time.sleep(0.5)
            self.draw_sign(i)
            self.next_turn()
        else:
            print("error,board full")

    def trainNN(self):
        self.__nn.train_neural_network()

    def victory(self):
        if self.__last_sign == self.__real_player_sign:
            self.__instructions.config(text="You lose, try again")
            """
            data = {}
            data["board_values"] = self.list_square_to_input()
            data["end_state"] =  "IA_victory"
            self.__game_recorder.add_game(data)
            """
            self.record_data("IA_victory")
        else:
            self.__instructions.config(text="You won, congratulations !")
            """
            data = {}
            data["board_values"] = self.list_square_to_input()
            data["end_state"] = "Player_victory"
            self.__game_recorder.add_game(data)
            """
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
        #data["index"] = index + 1 # avec un index par partie et un sous index index par mouvement
        data["board_values"] = self.list_square_to_input()
        if self.__last_sign == self.__real_player_sign:
            data["player"] = "IA"
        else:
            data["player"] = "real_player"
        self.__list_turn_record.append(data)

    def record_data(self,result):
        index = self.__game_recorder.get_index()
        i = 1
        for data in self.__list_turn_record:
            data["index"] = index
            data["sub_index"] = i
            data["end_state"] = result
            self.__game_recorder.add_game(data)
            i += 1

    def choose_sign(self):
        self.__last_sign = ["circle","cross"][np.random.randint(0,2)]

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
