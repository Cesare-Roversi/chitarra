from __future__ import annotations
import pygame
import math
from .Helpers import *
pygame.init()


class Separatore():
    def __init__(self, x:int, y:int, height:int):
        # var logiche
        self.x = x
        self.y = y
        self.height = height

        # var visuali
        self.screen = None

    def build(self, screen=None):
        if screen:
            self.screen = screen

    def show(self):
        aaline_thick(self.screen, (0,0,0), (self.x, self.y), (self.x, self.y + self.height), 1)
