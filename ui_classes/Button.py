# Esempio completo: pygame button class
import pygame

class Button:
    def __init__(self, width, height, delfault_color=(100, 100, 100), pressed_sx_color=(100,0,0), pressed_dx_color=(0,100,0), transparency=255, level=0):
        self.level = level
        self.x, self.y = None, None
        self.width, self.height = width, height
        self.rect = None
        self._color = delfault_color
        self.default_color = delfault_color
        self.pressed_sx_color = pressed_sx_color
        self.pressed_dx_color = pressed_dx_color
        self.transparency = max(0, min(255, transparency))
        self.border_width = 0
        self.border_color = (0,0,0)
        self.screen = None

        # stato interno
        self._pressed_sx = False  # se il click sx è iniziato dentro il pulsante
        self._pressed_dx = False


    def handle_event(self, event):
        """
        Metodo 1 richiesto: chiamare per ogni evento (pygame.event.get()).
        Gestisce MOUSEBUTTONDOWN e MOUSEBUTTONUP.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if event.button == 1:  # sinistro premuto
                    self._color = self.pressed_sx_color
                    self._pressed_sx = True
                    self.on_click_sx()

                elif event.button == 3:  # destro premuto
                    self._color = self.pressed_dx_color
                    self._pressed_dx = True
                    self.on_click_dx()

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # sinistro rilasciato
                # se il click era iniziato dentro e il rilascio avviene dentro, chiamiamo on_release_sx
                if self._pressed_sx and self.rect.collidepoint(event.pos):
                    self.on_release_sx()
                self._pressed_sx = False
                self._color = self.default_color

            if event.button == 3:
                if self._pressed_dx and self.rect.collidepoint(event.pos):
                    self.on_release_dx()
                self._pressed_dx = False
                self._color = self.default_color

    
    def handle_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        # mouse_buttons[0] è True se bottone sinistro tenuto
        mouse_sx, mouse_dx = mouse_buttons[0], mouse_buttons[2]
        if(self._pressed_sx):
            self.on_hold_sx()


    
    def on_click_sx(self):
        print("on_click_sx")

    def on_release_sx(self):
        print("on_release_sx")

    def on_click_dx(self):
        print("on_click_dx")

    def on_release_dx(self):
        print("on_release_dx")

    def on_hold_sx(self):
        print("on_hold_sx")


    def build(self, x, y, screen = None): #determina la posizione che è relativa al padre (cambia spesso) / tutta la merda che è riboldata dal padre
        if(x):
            self.x = x
        if(y):
            self.y = y
        if(screen):
            self.screen = screen
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)



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

    btn = Button(240, 80, delfault_color=(30, 144, 255), transparency=220, level=1)
    btn.build(200, 180)


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
