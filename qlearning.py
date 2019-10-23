# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 20:14:23 2019
@author: Julien Verdun
"""
# Implementation of Q-learning algorithm for TIC-TAC-TOE

import numpy as np
import random
from utils import functions as fct


global m
m = 1000000

class qlearning:
    """
    This class includes the methods that train the IA with Qlearning method.
    The optimal matrix Q is computed with the reward matrix R and uses to predict
    the best action for the IA to win the game.
    """
    def __init__(self,rfile_name = "R.txt",qfile_name = "Q.txt",list_grid_name = "all_possible_grid.txt", gamma = 0.8, alpha = 1, nb_states=100, nb_actions = 9, ini_state=[0 for k in range(9)]):
        self.__rfile_name = rfile_name
        self.__qfile_name = qfile_name
        self.__list_grid_name = list_grid_name
        self.__gamma = gamma
        self.__alpha = alpha
        self.__ini_state = ini_state
        self.__nb_states = nb_states
        self.__nb_actions = nb_actions
        self.__R = np.zeros(((self.__nb_states,self.__nb_actions)))
        self.__Q = np.zeros((self.__nb_states,self.__nb_actions))
        self.__list_grid = []

    def comput_R(self):
        """
        Nine independant squares, each can take 3 different values (-1, 0 and 1)
        It represents 3**9 different grid. 
        Index 0 -> -1 de 0 à 3**8, 0 de 3**8 à 2*3**8 puis 1
        Index 1 ->  -1 de 0 à 3**7, 0 de 3**7 à 2*3**7 puis 1
        
        #faire en sorte de generer toute les possibilites possibles

        """
        list_allowed_grid = []
        nb_combinaison = 3**9
        for i in range(0,nb_combinaison+1):
            grid = fct.index_to_grid(i)
            if self.is_allowed(grid) and (grid not in list_allowed_grid):
                list_allowed_grid.append(grid)
                print("Avancement : ", 100 * i / nb_combinaison)

        print("Nombre d'évènements possibles : ",len(list_allowed_grid))
        self.__list_grid = list_allowed_grid
        fct.save_file(self.__list_grid_name, str(list_allowed_grid))

        print("Number of different available grid: ", len(list_allowed_grid))

        self.__nb_states = len(list_allowed_grid)

        self.__R = np.zeros((self.__nb_states, self.__nb_actions))

        for i in range(self.__nb_states):
            for j in range(self.__nb_actions):
                list = list_allowed_grid[i]
                if list[j] == 0:
                    list[j] = -1 #on joue cette case
                    self.__R[i, j] = self.grid_to_reward(list)#on attribue la recompense correspondante
                # pas possible de jouer cette case
                else:
                    self.__R[i, j] = -100
        print("Matrix R computed ! ")
        fct.save_file(self.__rfile_name, fct.tab_to_str(self.__R))


    def load_R(self):
        """
        This function opens the file containing the matrix R, whose name is defined by private variable rfile_name,
        it changes the contains of the file to a matrix and stores the contains in the private variable R.
        """
        R_str = fct.read_file(self.__rfile_name)
        R_list = R_str.strip().split('\n')
        self.__R = np.zeros(((self.__nb_states,self.__nb_actions)))
        for i in range(self.__nb_states):
            R_sublist = R_list[i].strip().split(',')
            for j in range(len(R_sublist)):
                self.__R[i,j] = int(R_sublist[j])
        print("Matrix R loaded ! ")
        return self.__R

    def load_Q(self):
        """
        This function opens the file containing the matrix R, whose name is defined by private variable rfile_name,
        it changes the contains of the file to a matrix and stores the contains in the private variable R.
        """
        Q_str = fct.read_file(self.__qfile_name)
        Q_list = Q_str.strip().split('\n')
        self.__Q = np.zeros(((self.__nb_states,self.__nb_actions)))
        for i in range(self.__nb_states):
            Q_sublist = Q_list[i].strip().split(',')
            for j in range(len(Q_sublist)):
                self.__Q[i,j] = int(Q_sublist[j])
        print("Matrix Q loaded ! ")
        return self.__Q

    def load_list_grid(self):
        """
        This function opens the file containing the matrix of all grid, whose name is defined by private variable list_grid_name,
        it changes the contains of the file to a matrix and stores the contains in the private variable list_grid.
        """
        list_grid_str = fct.read_file(self.__list_grid_name)[1:-2]
        list_grid_list = list_grid_str.strip().split('], ')
        self.__list_grid = []
        for i in range(len(list_grid_list)-1):
            list_grid_sublist = list_grid_list[i][1:].split(', ')
            sublist = []
            for j in range(len(list_grid_sublist)):
                sublist.append(int(list_grid_sublist[j]))
            self.__list_grid.append(sublist)
        self.__nb_states = len(self.__list_grid)
        print("List of all grid loaded !")
        print(len(self.__list_grid))
        return self.__list_grid




    def comput_Q(self):
        """
        This functions computes the matrix Q that includes for a given state (each row
        represents a state), the overall score that IA can have by choosing a given action (each column
        represents an action, i-e a square to play).
        """

        #Initialization of the Q matrix
        self.__Q = np.zeros((self.__nb_states, self.__nb_actions))

        for k in range(m):
            print("Avancement : {}%".format(100*k/m))
            # random selection of an initial state (a grid with one more circle than cross)
            index_state = np.random.randint(0,self.__nb_states)
            state = self.__list_grid[index_state]
            #while final state isn't reached (end of the game)
            continuer = True
            while continuer :
                #if end state is reached (someone already win the game or the grid is full)
                if self.is_end_state_grid(state):
                    continuer = False
                else :
                    # selection of a new state among possible state

                    # definition of possible actions
                    action_dispo = []
                    # we select the actions that lead to a reward better or equal to -1
                    for i in range(self.__nb_actions):
                        if self.__R[index_state][i] >= -10:
                            action_dispo.append(i)
                    # if their are no possible actions, we take the better option
                    if len(action_dispo) == 0:
                        break
                    else:
                        #choix du max dans 80% des cas et dans 20% on choisit aléatoirement pour
                        #ajouter une part d'exploration
                        if np.random.randint(0,101) >= 70:
                            action = action_dispo[np.random.randint(0, len(action_dispo))]
                        else:
                            action = np.argmax(self.__R[index_state])
                    # definition of the new state with the choosen action
                    new_state = state.copy()
                    #print("Action placement -1: ",action)
                    new_state[action] = -1
                    #print("New state : ", new_state)
                    # if the action end the game, we stop this episode
                    if self.is_end_state_grid(new_state):
                        break
                    # otherwise we continue to play (player turn)
                    else :
                        # we randomly simulate the player turn and place a circle in an available square
                        #list of available square in the grid
                        liste_z = fct.list_of_0(new_state)
                        # if several square are available, we choose on of those
                        action = liste_z[np.random.randint(0,len(liste_z))]
                        # we place a circle on the selected action
                        #print("Action placement 1: ", action)
                        new_state[action] = 1

                        # we search the index of the new state in the list of posssible grid
                        index_new_state = self.__list_grid.index(new_state)

                        # We look for the maximal value of Q for the choosen state by considering all available actions
                        maxQ = np.max([self.__Q[index_new_state]])

                        # updating of Q
                        self.__Q = self.newQ(self.__Q, maxQ, index_state, action)# ou alors index_new_state et action ?
                        # mise à jour de l'état courant
                        state = new_state.copy()
                        index_state = index_new_state

        Q_norma = (100 * self.__Q / np.max(self.__Q)).astype(int)
        print("Matrix Q computed ! ")
        fct.save_file(self.__qfile_name,fct.tab_to_str(Q_norma))



    def newQ(self,lastQ, maxQ, i, j):
        """
        """
        newQ = lastQ.copy()
        newQ[i][j] = lastQ[i][j] * (1 - self.__alpha) + self.__alpha * (self.__R[i][j] + self.__gamma * maxQ)
        return newQ




    def predict_move(self,grid):
        """
        This functions takes a tic-tac-toe grid in parameter, i-e a state, and returns
        the number of the square that the IA should play in
        order to maximize its chances to win. The square is known with
        the Q-matrix computed before.
        """
        for i in range(len(self.__list_grid)):
            if self.__list_grid[i] == grid :
                return np.argmax(self.__Q[i])




    def is_allowed(self,grid):
        """
        This function takes a grid (list of 9 numbers, -1 for a cross, 1 for a circle and 0 otherwise)
        and return True if the grid is allowed and False otherwise.
        An allowed grid is a grid which contains n circles and n - 1 cross (n included in 1..5).
        """
        list_cross = []
        list_circle = []

        for i in range(len(grid)):
            if grid[i] == -1:
                list_cross.append(i)
            elif grid[i] == 1:
                list_circle.append(i)

        if len(list_circle) != len(list_cross) + 1 :
            return False

        if len(list_circle) > 5:
            return False

        if self.is_won(list_cross) and self.is_lose(list_circle):
            return False

        return True


    def grid_to_reward(self,grid):
        """
        This function takes a grid and (list of 9 values : -1 for a cross, 1 for a cricle and 0 otherwise)
        and returns the reward corresponding to this grid.
        Reward score :
        100 for a victory
        -10 for a defeat
        5 for a defense
        -1 for nothing.
        """
        reward = 0
        list_cross = []
        list_circle = []

        #fill in the list of indexes
        for i in range(len(grid)):
            if grid[i] == -1:
                list_cross.append(i)
            elif grid[i] == 1:
                list_circle.append(i)

        #change the reward depending on the grid disposition
        if self.is_won(list_cross) :
            reward += 100
        elif self.is_lose(list_circle):
            reward -= 10
        elif self.is_defense(list_circle):
            reward += 5
        else:
            reward -= 1
        return reward


    def is_won(self,list_cross):
        """
        This function returns True if the grid in parameter is a grid where the cross (value -1 in the list) have won the game,
        i-e if 3 cross squares are aligned. Otherwise it returns False.
        """

        if len(list_cross) >= 3:
            # first, sort the list
            list_cross.sort()
            for i in range(len(list_cross) - 2):
                # Check if 3 aligned cross on the lines
                if (list_cross[i] in [0,3,6]) and list_cross[i] == list_cross[
                    i + 1] - 1 == list_cross[i + 2] - 2:
                    return True
                # Check if 3 aligned cross on the columns
                if (list_cross[i] in [0,1,2]) and ((list_cross[i] + 3) in list_cross) and ((list_cross[i] + 6) in list_cross):
                    return True
                # Check if 3 aligned cross on the first diag
                if list_cross[i] == 0 and (list_cross[i] + 4) in list_cross and (list_cross[i] + 8) in list_cross:
                    return True
                # Check if 3 aligned cross on the second diag
                if list_cross[i] == 2 and (list_cross[i] + 2) in list_cross and (list_cross[i] + 4) in list_cross:
                    return True
        return False

    def is_lose(self,list_circle):
        """
        This function returns True if the grid in parameter is a grid where the cross (value -1 in the list) have lose the game,
        i-e if 3 circle squares are aligned. Otherwise it returns False.
        """
        if self.is_won(list_circle):
            return True
        return False

    def is_defense(self,list_circle):
        """
        This function returns True if the grid in parameter is a grid where 2 circles are aligned and the IA
        has to play the third square for him not to lose. Otherwise it returns False.
        """

        if len(list_circle) >= 2 :
            # first, sort the list
            list_circle.sort()
            for i in range(len(list_circle)-1):
                # Check if 2 aligned circle on the lines
                if (list_circle[i] in [0,1,3,4,6,7]) and list_circle[i] == list_circle[i + 1] - 1 :
                    return True
                # Check if 2 aligned circle on the columns
                if (list_circle[i] in [0,1,2,3,4,5]) and ((list_circle[i] + 3) in list_circle):
                        return True
                # Check if 2 aligned circle on the first diag
                if list_circle[i] in [0,4] and (list_circle[i] + 4) in list_circle :
                    return True
                # Check if 2 aligned circle on the second diag
                if list_circle[i] in [2,4] and (list_circle[i] + 2) in list_circle :
                    return True
        return False

    def is_full(self,grid):
        """
        This functions checks if there is one or more empty squares in the grid and return
        False if it is the case, Otherwise, the grid is full and the function returns True.
        """
        for elt in grid:
            if elt == 0:
                return False
        return True

    def is_end_state_grid(self,grid):
        """
         This function takes a grid and check whether the game is finished or not, i-e if
         the grid is full, or one of both players already won the game.
        """
        list_circle = []
        list_cross = []

        for i in range(len(grid)):
            if grid[i] == 1:
                list_circle.append(i)
            elif grid[i] == -1:
                list_cross.append(i)

        if self.is_full(grid) or self.is_won(list_cross) or self.is_lose(list_circle):
            return True
        return False

"""
ql = qlearning("R.txt","Q.txt","all_possible_grid.txt", 0.8, 1, 100, 9)
ql.load_list_grid()
ql.load_R()

ql.load_Q()
#ql.comput_Q()

# Testing some grid
print("Trying some prediction :")
print("Expected result : 2, got : ",ql.predict_move([1,1,0,0,-1,1,0,-1,0]))
print("Expected result : 6, got : ",ql.predict_move([1,0,-1,0,-1,1,0,0,1]))
"""