from __future__ import annotations
import pygame
import math
from .Helpers import *
pygame.init()

class Arco():
    def build(self, screen, nota1:"Nota", nota2:"Nota"):
        self.nota1 = nota1
        self.nota2 = nota2
        self.sx = nota1.center_x
        self.sy = nota1.get_bbox()[1] -3
        self.ex = nota2.center_x
        self.ey = nota2.get_bbox()[1] -3

        if(nota1.get_depth() == nota2.get_depth()):
            height = 20
            self.rect = pygame.Rect(self.sx, self.sy-height/2, self.ex-self.sx, height)  # x, y, width, height
            self.start_angle = 0   # pi radians (left side)
            self.end_angle = 3.14      # 0 radians (right side)
        else:
            pass
            #todo NON ho voglia
    
    def show(self, screen):
        if(self.nota1.get_depth() == self.nota2.get_depth()): #todo rimuovere quando fixi ^
            # use anti-aliased arc approximation
            aarc(screen, (0,0,0), self.rect, self.start_angle, self.end_angle, 2)