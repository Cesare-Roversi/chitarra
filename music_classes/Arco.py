from __future__ import annotations
import pygame
import math
from .Helpers import *
pygame.init()

class Arco():
    def __init__(self, nota1:"Nota", nota2:"Nota"):
        #var logiche
        self.nota1 = nota1
        self.nota2 = nota2

        #var visuali
        self.sx = None
        self.sy = None
        self.ex = None
        self.ey = None
        self.start_angle = None
        self.end_angle = None 
        self.screen = None

    def build(self, screen= None):
        if(screen):
            self.screen = None
        self.sx = self.nota1.center_x
        self.sy = self.nota1.get_bbox()[1] -3
        self.ex = self.nota2.center_x
        self.ey = self.nota2.get_bbox()[1] -3


        if(self.nota1.get_depth() == self.nota2.get_depth()):
            height = 20
            self.rect = pygame.Rect(self.sx, self.sy-height/2, self.ex-self.sx, height)  # x, y, width, height
            self.start_angle = 0   # pi radians (left side)
            self.end_angle = 3.14      # 0 radians (right side)
        else:
            pass
            #todo NON ho voglia
    
    def show(self):
        if(self.nota1.get_depth() == self.nota2.get_depth()): #todo rimuovere quando fixi ^
            # use anti-aliased arc approximation
            aarc(self.screen, (0,0,0), self.rect, self.start_angle, self.end_angle, 2)