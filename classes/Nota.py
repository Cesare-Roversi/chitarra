from __future__ import annotations
import pygame
import math
from .Helpers import *
pygame.init()

class Debug_rect():
    def build(self, screen, bbox):
        self.rect = pygame.Rect(bbox[0], bbox[1], bbox[2], bbox[3])
        self.color = (0, 0, 255, 128)
        self.is_show = True

    def show(self, screen):
        if(self.is_show):
            # crea una surface temporanea con canale alpha
            s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            # disegna il rettangolo blu con alpha 128 (0=trasparente, 255=opaco)
            pygame.draw.rect(s, self.color, s.get_rect())
            # blitta sullo schermo nella posizione voluta
            screen.blit(s, self.rect.topleft)

class Nota():
    def __init__(self, corda, tasto, durata = 1, dest_arco =None, dest_slide =None, bend =0):#logico
        self.corda = corda
        self.tasto = tasto
        self.durata = durata
        self.dest_arco = dest_arco
        self.dest_slide = dest_slide
        self.bend = bend

    def build(self, screen, x, y, font_size = 30):#visuale
        self.screen = screen

        self.center_x = x #il centro del testo
        self.center_y = y #il centro del testo

        self.spartito:"Spartito_chitarra" = None #la riga dello spartito a cui appartiene
        self.padding = 5
        self.font = pygame.font.SysFont(None, font_size)
        self.text_surface = self.font.render(str(self.tasto), True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(center=(x,y))
        
        left_i, top_i, width_i, height_i = self.get_bbox()
        width_i += self.padding*normX(screen)
        self.rect_behind = pygame.Rect(left_i, top_i, width_i, height_i)
        self.rect_behind.center = (self.center_x, self.center_y)
        # self.rect_behind = self.text_surface.get_rect(center=(x,y))
        # self.rect_behind.width += self.padding*normX(screen)
        # self.rect_behind.height += self.padding*normY(screen)
        # self.rect_behind.center = (x,y)

        #debug rect
        bbox = self.get_bbox()
        self.debug_rect = Debug_rect() #debug
        self.debug_rect.build(screen, bbox)

    def show(self, screen):
        pygame.draw.rect(screen, (255,255,255), self.rect_behind)
        screen.blit(self.text_surface, self.text_rect)
        self.debug_rect.show(screen)

    def get_depth(self):
        return self.spartito.depth
    
    def set_debug_rect_color(self, color):
        self.debug_rect.color = color
        self.debug_rect.is_show = True
    
    def show_debug_rect(self, show = True):
        self.debug_rect.is_show = show
    
    def get_bbox(self): #* x assoluta, y assoluta, width, height
        # prendi metriche del carattere (lista, una tupla per ogni char)
        metrics = self.font.metrics(str(self.tasto))
        if not metrics or metrics[0] is None:
            # fallback: usa il rect della surface renderizzata
            return self.text_surface.get_rect(topleft=self.text_rect.topleft)

        #! tutto riferito ripetto al punto in alto a sinistra
        min_x_1, max_x_1, min_y_1, max_y_1, advance = metrics[0]
        max_x_2 = 0
        max_y_2 = 0
        if(len(metrics) == 2):
            _, max_x_2, _, max_y_2, _ = metrics[1]

        max_y = max(max_y_1, max_y_2)

        #! in questo modo ottieni il punto in alto a sinistra
        x0 = self.text_rect.left
        y0 = self.text_rect.top + self.font.get_ascent()

        # converti le metriche (relative alla baseline) in coordinate schermo
        left = x0 + min_x_1
        right = x0 + max_x_1 + max_x_2 + 1
        top = y0 - max_y    # max_y è distanza verso l'alto dalla baseline
        bottom = y0 - min_y_1 # min_y è distanza verso il basso dalla baseline (spesso negativa)

        # costruisci il rect (interi, larghezza/altezza non negative)
        left_i  = int(round(left))
        top_i   = int(round(top))
        width_i = max(0, int(round(right - left)))
        height_i= max(0, int(round(bottom - top)))

        return (left_i, top_i, width_i, height_i)
    
    def get_training_data(self, left_shot, top_shot, width_shot, height_shot):
        abs_left_bbox, abs_top_bbox, width_bbox, height_bbox = self.get_bbox()
        left_bbox = abs_left_bbox - left_shot
        top_bbox = abs_top_bbox - top_shot

        x_center_norm = (left_bbox + width_bbox/2) / width_shot
        y_center_norm = (top_bbox + height_bbox/2) / height_shot

        bbox_width_norm = width_bbox / width_shot
        bbox_height_norm = height_bbox / height_shot

        return f"{self.tasto} {x_center_norm:.6f} {y_center_norm:.6f} {bbox_width_norm:.6f} {bbox_height_norm:.6f}\n"