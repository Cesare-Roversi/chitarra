from music_classes import *
from ui_classes import *

class SparitoChitarra():
    def __init__(self):
        self.x = None
        self.y = None
        self.grid:list[list[ButtonNota]]
        self.tempo = 1
        self.width = 1000
        self.distanza_tra_corde = 10 #MID = 10
        self.distanza_tra_note = 15 #MID = 15
        self.distanza_separatore = 30 #MID = 30
        self.distanza_tra_spartiti = 100
        self.screen = None
        pass

    def build(self, x= None, y= None, list_groups:list[list[Nota]] = None, screen = None):
        if(x):
            self.x = x
        if(y):
            self.y = y
        if(screen):
            self.screen = screen

        if(list_groups):
            for gx in range(len(list_groups)):
                for gy in range(6):
                    self.grid[gx][gy] = ButtonNota(None, (gx,gy), 100, 100)
            
                for n in list_groups[gx]:
                    gy = n.corda
                    self.grid[gx][gy].set_internal_note(n)

        counter = 0
        for gx in range(len(self.grid)):
            for gy in range(6):
                nx = self.x+gx*self.distanza_tra_note*normX(self.screen)
                ny = self.y+gy*normY(self.screen)
                if(nx > self.x+self.width):
                    nx = self.x
                    ny = self.y+6*normY(self.screen)+self.distanza_tra_spartiti*normY(self.screen)
                self.grid[gx][gy].build(None, nx, ny, (gx, gy), screen)

    
