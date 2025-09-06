from __future__ import annotations
import pygame
import math
from .Helpers import *
from .Nota import *
from .Separatore import *
from .Arco import *
from .Slide import *
from .Bend import *
pygame.init()


class Linee_spartito():
    def build(self, screen, x, y, distanza_tra_corde, width, depth):
        self.x = x
        self.y = y
        self.distanza_tra_corde = distanza_tra_corde
        self.width = width
        self.depth = depth

    def show(self, screen):
        for i in range(6):
            aaline_thick(screen, (0,0,0), (self.x, self.y+self.distanza_tra_corde*i), (self.width, self.y+self.distanza_tra_corde*i), 1)



class Spartito_chitarra():
    def __init__(self, tempo = 1, list_note = []):
        self.list_note:list[list] = list_note
        self.tempo = tempo

    def build(self, screen, x, y, width):
        #parametri visuali
        screen_width, screen_height = screen.get_size()
        distanza_tra_corde = 10*normY(screen) #MID = 10
        distanza_tra_note = 15*normX(screen) #MID = 15
        distanza_separatore = 30*normX(screen) #MID = 30
        distanza_tra_spartiti = 100*normY(screen)
        font_size = 30 #!font size
        self.x = x #angolo in alto a sx spartito
        self.y = y #
        self.width = width

        #variabili
        self.list_figli = []
        
        count_depth_spartiti = 0 
        x_relativa = x
        y_relativa = y
        linee = Linee_spartito()
        linee.build(screen, x, y, distanza_tra_corde, width, count_depth_spartiti)
        self.list_figli.append(linee)
        count_durata_note = 0
        for note_contemporanee in self.list_note:

            note_contemporanee:Nota
            count_durata_note += note_contemporanee[0].durata
            if(count_durata_note > self.tempo):
                count_durata_note = 0
                sep = Separatore() 
                x_relativa += distanza_separatore
                sep.build(screen, x_relativa, y_relativa, distanza_tra_corde*5)
                self.list_figli.append(sep)
                x_relativa += distanza_separatore

            if(x_relativa > self.width-50):
                x_relativa = x
                y_relativa += distanza_tra_corde*5 +distanza_tra_spartiti
                linee = Linee_spartito()
                count_depth_spartiti +=1
                linee.build(screen, x_relativa, y_relativa, distanza_tra_corde, width, count_depth_spartiti)
                self.list_figli.append(linee)

            x_relativa += distanza_tra_note
            for nota in note_contemporanee: #add Note objects
                y_nota = y_relativa + distanza_tra_corde*(nota.corda-1)
                nota.build(screen, x_relativa, y_nota, font_size)
                nota.spartito = linee
                self.list_figli.append(nota)
            x_relativa += distanza_tra_note

        #*archi, slide, bend
        for note in self.list_note:
            for nota in note:
                nota:Nota
                if(nota.dest_arco != None):
                    arco = Arco()
                    arco.build(screen, nota, nota.dest_arco)
                    self.list_figli.append(arco)

                if(nota.dest_slide != None):
                    slide = Slide()
                    slide.build(screen, nota, nota.dest_slide)
                    self.list_figli.append(slide)

                if(nota.bend != 0):
                    bend = Bend()
                    bend.build(screen, nota, nota.bend)
                    self.list_figli.append(bend)

        #self.list_figli.append(RedDot(50,500,30))


    def show(self, screen):
        for f in self.list_figli:
            f.show(screen)
