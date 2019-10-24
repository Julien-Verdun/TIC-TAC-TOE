from tkinter import *
from tkinter.messagebox import *
from utils.constantes import *
from utils import classFile as cls , functions as fct

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