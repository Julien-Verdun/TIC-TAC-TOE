import numpy as np

def index_to_grid(i):
    """
    Convert an index i into a list that give the element of this number
    converted in base 3.
    """
    grid = [0 for k in range(9)]
    j = 0
    nb = i
    while nb >= 0 and j <= 8:
        if nb // (3 ** (8 - j)) > 0:
            grid[8 - j] = nb // (3 ** (8 - j))
            nb -= (3 ** (8 - j)) * (nb // (3 ** (8 - j)))
        j += 1
    for i in range(len(grid)):
        grid[i] -= 1
    return grid


def grid_to_index(grid):
    index = 0
    for i in range(0, len(grid)):
        index += (grid[i]+1) * (3 ** i)
    return index

def read_file(file_name):
    """
    This function returns the contents of the file named
    file_name.
    """
    with open(file_name,"r") as file:
        return file.read()


def save_file(file_name,text):
    """
    This function overwrites the file named file_name
    and changes its contents with variable text.
    """
    with open(file_name,"w") as file:
        file.write(text)



def tab_to_str(tab):
    texte = ""
    for i in range(np.shape(tab)[0]):
        for j in range(np.shape(tab)[1]):
            texte += str(int(tab[i, j])) + ","
        texte = texte[:-1] + '\n'
        # texte+='\n'
    return texte



def list_of_0(liste):
    """
    This function returns for a given list, a list of number that represent the index of 0 elements
    in the given list.
    """
    liste_z = []
    for i in range(len(liste)):
        if liste[i] == 0:
            liste_z.append(i)
    return liste_z





   def is_won(list_signs,list_index_signs):
        if len(list_signs) <= 4:
            return False
        #if the first one was a cross
        if type(list_signs[0]) == list:
            beg = 0
        else :
            beg = 1
        #list of the index of al crosses and all circles.
        list_cross = list_index_signs[beg::2]
        list_circle = list_index_signs[1-beg::2]

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

