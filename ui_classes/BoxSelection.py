import pygame

class BoxSelection:
    def __init__(self, color=(255, 0, 0, 100)):
        self.color = color
        self.screen = None
        self.x = None
        self.y = None
        self.width = None
        self.height = None

    def build(self, st_coo, end_coo, screen = None):
        if(screen):
            self.screen = screen
        self.x, self.y = st_coo
        end_x, end_y =  end_coo
        self.width, self.height = end_x-self.x, end_y-self.y
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface.fill(self.color)  # RGBA
        self.rect = self.surface.get_rect(topleft=(self.x, self.y))

    def show(self):
        self.screen.blit(self.surface, self.rect)
