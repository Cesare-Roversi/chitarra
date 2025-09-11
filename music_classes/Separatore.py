from __future__ import annotations
import pygame
import math
from .Helpers import *
pygame.init()


class Separatore():
    def __init__(self):
        # var logiche
        self.x = None
        self.y = None
        self.height = None

        # var visuali
        self.screen = None

    def build(self, x:int, y:int, height:int, screen = None):
        if screen:
            self.screen = screen
        self.x = x
        self.y = y
        self.height = height

    def show(self):
        aaline_thick(self.screen, (0,0,0), (self.x, self.y), (self.x, self.y + self.height), 1)
