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