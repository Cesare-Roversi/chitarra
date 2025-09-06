from __future__ import annotations
import pygame
from . import Button
import music_classes
print(music_classes.Nota)
'''
build()
tutti i cambiamenti che dipendono dall'aver ribildato il padre
viene cambiato dal padre o 1 volta dal main se non ha padre

non faccio diurettamente col draw() perchè:
1-è stupido ricalcolare se non serve
2-deve poter essere chiamato senza argomenti del cazzo
'''


class ButtonNota(Button.Button):
    def __init__(self, nota, grid_coo:tuple, width = 200, height = 200, delfault_color=(100, 100, 100), pressed_sx_color=(100,0,0), pressed_dx_color=(0,100,0), transparency=255, level=0):
        super().__init__(width,height,delfault_color,pressed_sx_color,pressed_dx_color,transparency,level)
        self.grid_coo = grid_coo
        self.nota:music_classes.Nota = nota

    def build(self, x= None, y= None, grid_coo= None, screen= None):
        if(x):
            x = self.x
        if(y):
            y = self.y
        if(grid_coo):
            grid_coo = self.grid_coo
        if(screen):
            self.screen


    def handle_mouse(self):#complete override
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        # mouse_buttons[0] è True se bottone sinistro tenuto
        mouse_sx, mouse_dx = mouse_buttons[0], mouse_buttons[2]
        if(self._pressed_sx):
            self.on_hold_sx(mouse_pos)

    
    def on_click_sx(self):
        print("on_click_sx")

    def on_release_sx(self):
        print("on_release_sx")

    def on_click_dx(self):
        print("on_click_dx")

    def on_release_dx(self):
        print("on_release_dx")

    def on_hold_sx(self, mouse_pos):
        #self.nota.
        print("on_hold_sx")


    def draw(self, screen):
        tmp = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        r, g, b = self._color
        tmp.fill((r, g, b, self.transparency))
        screen.blit(tmp, (self.x, self.y))
        if self.border_width > 0:
            pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)



# --- Esempio di utilizzo in un loop pygame ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    btn = ButtonNota(200, 180, 240, 80, delfault_color=(30, 144, 255), transparency=220, level=1)


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            btn.handle_event(event)  # metodo per gestire gli eventi mouse (down/up)

        btn.handle_mouse()
        screen.fill((30, 30, 30))
        btn.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
