from __future__ import annotations
import pygame
import math
from .Helpers import *
pygame.init()


class Bend():
    def __init__(self, nota:"Nota", intensity:float=1):
        # var logiche
        self.nota = nota
        self.intensity = intensity

        # var visuali
        self.sx = None
        self.sy = None
        self.rect = None
        self.start_angle = None
        self.end_angle = None
        self.testo_x = None
        self.testo_y = None
        self.font_size = 15
        self.screen = None

    def build(self, screen=None):
        if screen:
            self.screen = screen

        left_1, top_1, width_1, height_1 = self.nota.get_bbox()
        self.sx = left_1 + width_1 + 3
        self.sy = top_1 + 3

        height = 140 * self.intensity * normY(self.screen)
        width = 10
        self.rect = pygame.Rect(self.sx - width_1/2, self.sy - height, width, height)

        self.start_angle = math.pi      # pi radians (left side)
        self.end_angle = 0              # 0 radians (right side)

        self.testo_x = self.sx + width
        self.testo_y = self.sy - height/4

        font = pygame.font.SysFont(None, self.font_size)
        text = self.get_fraction(self.intensity)
        self.text_surface = font.render(text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(center=(self.testo_x, self.testo_y))

    def get_fraction(self, i:float) -> str:
        if i == 1:
            return "full"
        if i == 0.75:
            return "3/4"
        if 0.6 <= i < 0.7:
            return "2/3"
        if i == 0.5:
            return "1/2"
        if 0.3 <= i <= 0.4:
            return "1/3"
        if i == 0.25:
            return "1/4"
        if i == 0.2:
            return "1/5"
        return "???"

    def show(self):
        aarc(self.screen, (0,0,0), self.rect, math.pi*1.5, 0, 1)
        self.screen.blit(self.text_surface, self.text_rect)
