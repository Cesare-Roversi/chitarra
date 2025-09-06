import pygame
import cv2
import random as rand
import numpy as np
import os
from classes.Spartito import *
from generatore import Generatore

def cv2_show(s):
    subsurf_array = pygame.surfarray.array3d(s)  # shape: (w, h, 3)
    subsurf_array = np.transpose(subsurf_array, (1, 0, 2))  # swap axes (w,h) -> (h,w)
    subsurf_array = cv2.cvtColor(subsurf_array, cv2.COLOR_RGB2BGR)  # pygame is RGB, cv2 expects BGR

    # Show with cv2
    cv2.imshow("Subsurface", subsurf_array)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

WIDTH = 1920
HEIGHT = 1080

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#*OLD
# list_note = []
# for _ in range(40):
#     tp = [Nota(1,19,0.25), Nota(2,9,0.25)]
#     list_note.append(tp)

# pr:Nota = list_note[0][0]
# pr.dest_arco = list_note[1][0]

# pr:Nota = list_note[0][0]
# pr.dest_slide = list_note[1][0]

# pr:Nota = list_note[3][0]
# pr.bend = 1

# pr:Nota = list_note[2][0]
# pr.bend = 0.3
#*_OLD

#crea cartelle
try:
    os.makedirs(os.path.join("dataset", "images", "train"), exist_ok=True)
    os.makedirs(os.path.join("dataset", "images", "val"), exist_ok=True)
    os.makedirs(os.path.join("dataset", "labels", "train"), exist_ok=True)
    os.makedirs(os.path.join("dataset", "labels", "val"), exist_ok=True)
    print("Cartelle create con successo (o già presenti).")
except OSError as e:
    # Cattura qualsiasi altro errore di sistema che potrebbe verificarsi
    print(f"Errore durante la creazione delle cartelle: {e}")

SAVE = False
SHOW = False
if(SAVE and SHOW):
    exit(104)
    
for i in range(1):
    #*SCREENSHOT SETTINGS
    min_x, max_x = 0, 60 #LONG = 60
    min_y, max_y = 50, 100
    sx_shot = rand.randint(min_x, max_x)
    sy_shot = rand.randint(min_y, max_y)

    width_shot = rand.randint(100, WIDTH - sx_shot)
    height_shot = rand.randint(150, 250)
    width_shot = WIDTH - sx_shot #todo COMMENT - LONG ONLY
    ex_shot = sx_shot+width_shot
    ey_shot = sy_shot+height_shot
    screenshot_rect = pygame.Rect(sx_shot, sy_shot, width_shot, height_shot)
    
    #builds everything
    list_note = Generatore()
    spartito = Spartito_chitarra(list_note=list_note)
    spartito.build(screen, 50, 100, WIDTH - 50)

    #trova la lista di note nello screen    
    list_inside_screenshot = []
    for g in list_note:
        for n in g:
            n:Nota
            sx_n, sy_n, w, h = n.get_bbox()
            ex_n, ey_n = sx_n+w, sy_n+h

            if (sx_n > sx_shot and sx_n < ex_shot) and (sy_n > sy_shot and sy_n < ey_shot) and (ex_n > sx_shot and ex_n < ex_shot) and (ey_n > sy_shot and ey_n < ey_shot):
                list_inside_screenshot.append(n)
                n.set_debug_rect_color((255,0,0,128))
                n.show_debug_rect(False)


    #pygame show
    screen.fill((255,255,255))
    spartito.show(screen)
    pygame.display.flip()
    subsurf = screen.subsurface(screenshot_rect)
    if(SHOW):
        cv2_show(subsurf)

    if(SAVE):
        cartella = "val"
        #label_path = os.path.join("dataset", "labels", cartella, f"{i}.txt")
        label_path = os.path.join("big_long", "labels", f"{i}_bl.txt")
        with open(label_path, "w") as f:
            for n in list_inside_screenshot:
                n:Nota
                f.write(n.get_training_data(sx_shot, sy_shot, width_shot, height_shot))

        #image_path = os.path.join("dataset", "images", cartella, f"{i}.jpg")
        image_path = os.path.join("big_long", "images", f"{i}_bl.jpg")
        pygame.image.save(subsurf, image_path)


running =True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(30)

pygame.quit()
