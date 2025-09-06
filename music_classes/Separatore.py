from __future__ import annotations
import pygame
import math
from .Helpers import *
pygame.init()

class Separatore():
    def build(self, screen, x, y, height):
        self.x = x
        self.y = y
        self.height = height

    def show(self, screen):
        aaline_thick(screen, (0,0,0), (self.x, self.y), (self.x, self.y+self.height), 1)