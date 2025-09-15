from __future__ import annotations
import pygame
from . import Button
import music_classes
from custom_exceptions import *
print(music_classes.Nota)
'''
build()
tutti i cambiamenti che dipendono dall'aver ribildato il padre
viene cambiato dal padre o 1 volta dal main se non ha padre

non faccio diurettamente col draw() perchè:
1-è stupido ricalcolare se non serve
2-deve poter essere chiamato senza argomenti del cazzo
'''


class ButtonNota(Button):
    def __init__(self, nota, grid_coo:tuple, width = 200, height = 200, delfault_color=(100, 100, 100), pressed_sx_color=(100,0,0), pressed_dx_color=(0,100,0), transparency=255, level=0):
        super().__init__(width,height,delfault_color,pressed_sx_color,pressed_dx_color,transparency,False,level)
        self.grid_coo = grid_coo
        self.nota:music_classes.Nota = nota

    def build(self, nota= None, x= None, y= None, grid_coo= None, screen= None):
        super().build(x,y,screen)
        if(grid_coo):
            self.grid_coo = grid_coo
        if(nota):
            self.nota = nota
        if(self.nota):
            self.nota.build(self.x+self.width/2, self.y+self.height/2, None, screen)

    def show(self):
        super().show()
        if(self.nota):
            self.nota.show()

    def handle_mouse(self):#complete override
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        delta = (0,0)
        if(self._pressed_sx): #questa varaibile è settata da handle event della classe button
            delta = self.on_hold_sx(mouse_pos)

        return delta #posizione iniziale nota - posizione attuale mouse

    
    def on_click_sx(self):
        #print("on_click_sx")
        pass

    def on_release_sx(self):
        #print("on_release_sx")
        # if(not self.check_overlap(self.nota.get_bbox())):
        #     self.nota.build(self.x+self.width/2, self.y+self.height/2) 
        pass

    def on_click_dx(self):
        #print("on_click_dx")
        pass

    def on_release_dx(self):
        #print("on_release_dx")
        pass

    def on_hold_sx(self, mouse_pos):
        if(self.nota):
            self.nota.build(center_x=mouse_pos[0], center_y=mouse_pos[1])

        cx =self.x+self.width/2
        cy =self.y+self.height/2
        delta = (mouse_pos[0]-cx, mouse_pos[1]-cy)
        return delta

    def get_bbox(self):
        return (self.x, self.y, self.width, self.height)

    def get_note_bbox(self):
        if(self.nota):
            return self.nota.get_bbox()
        else:
            raise NotaAssente()

    def check_overlap(self, bbox):
        obj_x, obj_y, obj_w, obj_h = bbox
        obj_x1, obj_y1 = obj_x+obj_w, obj_y+obj_h
        sx, sy, sx1, sy1 = self.x, self.y, self.x+self.width, self.y+self.height

        return not (obj_x1 < sx or obj_x > sx1 or obj_y1 < sy or obj_y > sy1)
    
    def check_click(self, pos):
        cx, cy = pos
        sx, sy, sx1, sy1 = self.x, self.y, self.x+self.width, self.y+self.height
        return (cx >= sx and cx <= sx1 and cy >= sy and cy <= sy1)


    def selected_color(self, v =True):
        if(v):
            self._color = self.pressed_sx_color
        else:
            self._color = self.default_color

    def set_internal_note(self, nota):
        self.nota = nota
        try:
            self.nota.build(self.x+self.width/2, self.y+self.height/2) 
        except:
            pass

    
    def __str__(self):
        return f"coo= {self.grid_coo}, Nota=[ {self.nota} ]"
    