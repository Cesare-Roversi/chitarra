from __future__ import annotations
import pygame
import math
from .Helpers import *
pygame.init()


class Slide():
    def __init__(self, nota1:"Nota", nota2:"Nota"):
        # var logiche
        self.nota1 = nota1
        self.nota2 = nota2

        # var visuali
        self.sx = None
        self.sy = None
        self.ex = None
        self.ey = None
        self.screen = None

    def build(self, screen=None):
        if screen:
            self.screen = screen

        left_1, top_1, width_1, height_1 = self.nota1.get_bbox()
        left_2, top_2, width_2, height_2 = self.nota2.get_bbox()

        self.sx = left_1 + width_1 + 3
        self.sy = top_1 + 3
        self.ex = left_2 - 3
        self.ey = top_2 + height_2 - 3

        # todo: completare logica avanzata

    def show(self):
        if self.nota1.get_depth() == self.nota2.get_depth():  # todo rimuovere quando fixi ^
            aaline_thick(self.screen, (0,0,0), (self.sx, self.sy), (self.ex, self.ey), 2)
