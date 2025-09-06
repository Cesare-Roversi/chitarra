from __future__ import annotations
import pygame
import math
from .Helpers import *
pygame.init()


class Bend():
    def build(self, screen, nota, intensity =1):
        left_1, top_1, width_1, height_1 = nota.get_bbox()
        self.sx = left_1+width_1+3
        self.sy = top_1+3
        height = 140*intensity*normY(screen)
        width = 10
        self.rect = pygame.Rect(self.sx-width_1/2, self.sy-height, width, height)  # x, y, width, height
        self.start_angle = 3.14   # pi radians (left side)
        self.end_angle = 0     # 0 radians (right side)

        self.testo_x = self.sx + width #il centro del testo
        self.testo_y = self.sy - height/4 #il centro del testo
        self.font = pygame.font.SysFont(None, 15)
        self.text_surface = self.font.render(self.get_fraction(intensity), True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(center=(self.testo_x, self.testo_y))

    def get_fraction(self, i):
        if(i == 1):
            return "full"
        if(i == 0.75):
            return "3/4"
        if(i >= 0.6 and i <0.7):
            return "2/3"
        if(i == 0.5):
            return "1/2"
        if(i >= 0.3 and i <= 0.4):
            return "1/3"
        if(i == 0.25):
            return "1/4"
        if(i == 0.2):
            return "1/5"
        return "???"

    def show(self, screen):
        aarc(screen, (0,0,0), self.rect, math.pi*1.5, 0, 1)
        screen.blit(self.text_surface, self.text_rect)