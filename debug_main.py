import pygame
from ui_classes.ButtonNota import *

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