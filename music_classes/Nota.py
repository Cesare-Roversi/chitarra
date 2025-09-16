from __future__ import annotations
import pygame
import os
import math
try:
    from .Helpers import *
except:
    pass


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
    '''
    Dato che la nota classica e la nota chitarra sono strettamente legate nello spartito
    ho deciso di non usare ereditarientà ma composizione
    '''
    def __init__(self, corda, tasto, durata = 1, dest_arco =None, dest_slide =None, bend =0):
        #var logiche
        self.corda = corda
        self.tasto = tasto
        self.durata = durata
        self.dest_arco = dest_arco
        self.dest_slide = dest_slide
        self.bend = bend
        self.tono, self.ottava = self.converti_nota(corda, tasto)

        #var visuali
        self.visuale_chitarra = NotaVisualeChitarra(self)
        self.visuale_classica = NotaVisualeClassica(self)

    #?LOGIC ONLY
    def converti_nota(self, corda, tasto):
        scala_cromatica = ["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"]
        intonazione = {1: "E", 2: "B", 3: "G", 4: "D", 5: "A", 6: "E"}
        ottava_iniziale = {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 2}
        nota_iniziale = intonazione[corda]
        cr_ix = scala_cromatica.index(nota_iniziale)
        tono_ix = (cr_ix+tasto)%12
        tono = scala_cromatica[tono_ix]
        salto_di_un_ottava = math.floor((cr_ix+tasto)/12)
        ottava = ottava_iniziale[corda]+salto_di_un_ottava
        return (tono, ottava)
    
    #?LOGIC ONLY
    def build_visuale_chitarra(self, center_x = None, center_y = None, font_size = None, screen = None):
        self.visuale_chitarra.build(center_x, center_y, font_size, screen)

    def show_visuale_chitarra(self):
        self.visuale_chitarra.show()

    def build_visuale_classica(self, center_x = None, center_y = None, size = None, screen = None):
        self.visuale_classica.build(center_x = None, center_y = None, size = None, screen = None)

    def build_visuale_classica(self):
        self.build_visuale_classica.show()
    
    #?DEBUG ONLY
    def get_bbox_visuale_chitarra(self):
        return self.visuale_chitarra.get_bbox()
    
    def get_bbox_visuale_classica(self):
        return self.visuale_classica.get_bbox()

    def __str__(self):
        return f"Nota=[ tasto={self.tasto}, corda={self.corda}, durata={self.durata} ]"
    def __repr__(self):
        return self.__str__()
    
    #?DEBUG ONLY => visuale_chitarra
    def show_debug_rect(self, show = True):
        self.visuale_chitarra.show_debug_rect(show)

    #?DEBUG ONLY => visuale_classica
    def show_circlebbx(self):
        self.visuale_classica.show_circlebbx()
    

#!---------------------------------------------------------------------------------------------------------------------------------
class NotaVisualeChitarra():
    def __init__(self, nota_logica):
        self.nota_logica:Nota = nota_logica
        self.font_size = 30
        self.screen = None
        self.center_x = None #il centro del testo
        self.center_y = None #il centro del testo
        self.padding = 5
        self.rect_behind = None
        self.debug_rect = Debug_rect()

    #?VISUAL ONLY
    def build(self, center_x = None, center_y = None, font_size = None, screen = None):#visuale
        if(center_x):
            self.center_x = center_x #il centro del testo
        if(center_y):
            self.center_y = center_y #il centro del testo
        if(font_size):
            self.font_size = font_size
        if(screen):
            self.screen = screen

        self.spartito:"Spartito_chitarra" = None #la riga dello spartito a cui appartiene
        self.font = pygame.font.SysFont(None, self.font_size)
        self.text_surface = self.font.render(str(self.nota_logica.tasto), True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(center=(center_x,center_y))
        
        left_i, top_i, width_i, height_i = self.get_bbox()
        width_i += self.padding*normX(self.screen)
        self.rect_behind = pygame.Rect(left_i, top_i, width_i, height_i)
        self.rect_behind.center = (self.center_x, self.center_y)

        #debug rect
        bbox = self.get_bbox()
        self.debug_rect.build(self.screen, bbox)

    def show(self):
        pygame.draw.rect(self.screen, (255,255,255), self.rect_behind)
        self.screen.blit(self.text_surface, self.text_rect)
        self.debug_rect.show(self.screen)

    def get_bbox(self): #* x assoluta, y assoluta, width, height
        # prendi metriche del carattere (lista, una tupla per ogni char)
        metrics = self.font.metrics(str(self.nota_logica.tasto))
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
    
    def show_debug_rect(self, show = True):
        self.debug_rect.is_show = show
    
    def get_training_data(self, left_shot, top_shot, width_shot, height_shot):
        abs_left_bbox, abs_top_bbox, width_bbox, height_bbox = self.get_bbox()
        left_bbox = abs_left_bbox - left_shot
        top_bbox = abs_top_bbox - top_shot

        x_center_norm = (left_bbox + width_bbox/2) / width_shot
        y_center_norm = (top_bbox + height_bbox/2) / height_shot

        bbox_width_norm = width_bbox / width_shot
        bbox_height_norm = height_bbox / height_shot

        return f"{self.nota_logica.tasto} {x_center_norm:.6f} {y_center_norm:.6f} {bbox_width_norm:.6f} {bbox_height_norm:.6f}\n"



#!----------------------------------------------------------------------------------------------------------------------------------
class NotaVisualeClassica():
    def __init__(self, nota_logica):
        self.nota_logica:Nota = nota_logica
        self.screen = None
        self.center_x = None #il centro del testo
        self.center_y = None #il centro del testo
        self.padding = 5
        self.size = 50
        self.img = None

    #?SOLO VISUAL
    def build(self, center_x = None, center_y = None, size = None, screen = None):#visuale
        if(center_x):
            self.center_x = center_x #il centro del testo
        if(center_y):
            self.center_y = center_y #il centro del testo
        if(size):
            self.size = size
        if(screen):
            self.screen = screen

        if(self.nota_logica.durata == 1):
            tipo = "1th.png"
        elif(self.nota_logica.durata == 1/2):
            tipo = "2th.png"
        elif(self.nota_logica.durata == 1/4):
            tipo = "4th.png"
        elif(self.nota_logica.durata == 1/8):
            tipo = "8th.png"
        elif(self.nota_logica.durata == 1/16):
            tipo = "16th.png"
        elif(self.nota_logica.durata == 1/32):
            tipo = "32th.png"
        elif(self.nota_logica.durata == 1/64):
            tipo = "64th.png"
        path = os.path.join("notes_notation", tipo)
        self.img = pygame.transform.scale((pygame.image.load("path").convert_alpha()), (self.size,self.size))

    def show(self):
        pygame.draw.rect(self.screen, (255,255,255), self.rect_behind)
        self.screen.blit(self.img, (self.center_x-(self.size/2), self.center_y-(self.size/2)))
        self.show_bbox()


    #?SOLO DEBUG
    def get_bbox(self):
        hw = self.size * 0.15  # metà larghezza
        hh = self.size * 0.10 # metà altezza
        sx = -hw  # distanza orizzontale dal centro
        sy = -hh  # distanza verticale dal centro
        width = 2 * hw
        height = 2 * hh
        return (sx+self.center_x, sy+self.center_y, width, height)
    
    def show_circlebbx(self):
        x,y,W,H = self.get_bbox()
        rect_surf = pygame.Surface((W,H), pygame.SRCALPHA)
        rect_surf.fill((0,0,255, 128))
        self.screen.blit(rect_surf, (x,y))

    


if __name__ == "__main__":
    nota = Nota(4, 5)
    print(nota.tono)
    print(nota.ottava)
