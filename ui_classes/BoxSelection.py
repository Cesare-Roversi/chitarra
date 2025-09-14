import pygame

class BoxSelection:
    def __init__(self, color=(255, 0, 0, 100)):
        self.color = color
        self.is_active = False
        self.screen = None
        self.top_x = None
        self.top_y = None
        self.width = None
        self.height = None

    def build(self, is_active = False, st_coo = None, end_coo = None, screen = None):
        self.is_active = is_active
        if(self.is_active):
            if(screen):
                self.screen = screen
            st_x, st_y = st_coo
            end_x, end_y =  end_coo
            self.top_x = min(st_x, end_x)
            bottom_x = max(st_x, end_x)
            self.top_y = min(st_y, end_y)
            bottom_y = max(st_y, end_y)
            self.width, self.height = bottom_x-self.top_x, bottom_y-self.top_y
            self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self.surface.fill(self.color)  # RGBA
            self.rect = self.surface.get_rect(topleft=(self.top_x, self.top_y))

    def show(self):
        if(self.is_active):
            self.screen.blit(self.surface, self.rect)

    def get_bbox(self):
        return (self.top_x, self.top_y, self.width, self.height)
    

