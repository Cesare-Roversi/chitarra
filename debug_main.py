import pygame
from ui_classes.ButtonNota import *
from music_classes import Nota

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

nota = Nota(0,0,1)
btn = ButtonNota(nota, (0,0), 100, 100, delfault_color=(30, 144, 255), transparency=220, level=1)
btn.build(None, 300, 300, (0,0), screen)

nota1 = Nota(0,1,1)
btn1 = ButtonNota(nota1, (0,0), 100, 100, delfault_color=(30, 144, 255), transparency=220, level=1)
btn1.build(None, 100, 100, (0,0), screen)

print(nota1.get_bbox())

def handler_spartito(event, keys, clicked_btn, btns, selected_btns):
    #key list
    CTRL = keys & pygame.KMOD_CTRL

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left mouse down
        print("MOUSE DOWN")
        found = False
        for ix, dest in enumerate(btns):
            if dest.check_click(event.pos):
                clicked_btn = dest
                found = True   
        if(found and not CTRL):
            if clicked_btn in selected_btns:
                selected_btns.remove(clicked_btn)
                clicked_btn.selected_color(False)
            else:
                clicked_btn.selected_color()
                selected_btns.add(clicked_btn)
        elif(not found):
            for s in selected_btns:
                s.selected_color(False)
            clicked_btn = None
            selected_btns.clear()


    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # left mouse up
        print("MOUSE UP")

        print(f"selected_notes: {selected_btns}")
        found = False
        for n in btns:
            if(found):
                break
            for s in selected_btns:
                n:ButtonNota
                s:ButtonNota
                print(f"nota: {s.get_note_bbox()}")
                if(s != n and n.check_inside(s.get_note_bbox())):
                    print("diebymyhand")
                    #n.set_internal_note(s.steal_internal_note())
                    found = True
                    deltaX = n.grid_coo[0]-s.grid_coo[0]
                    deltaY = n.grid_coo[1]-s.grid_coo[1]
                    for s in selected_btns:
                        new_posX = s.grid_coo[0]+deltaX
                        new_posY = s.grid_coo[1]+deltaY
                        #btns_grid[new_posX][new_posY].set_iternal_note(s.steal_internal_note())


    return clicked_btn

btns = set()
btns.update([btn, btn1])

selected_btns = set()
clicked_btn = None
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #internal notes handler
        for b in btns :
            b.handle_event(event)
        keys = pygame.key.get_mods()
        clicked_btn = handler_spartito(event, keys, clicked_btn, btns, selected_btns) #premere un bottone è un evento? boh

    #internal notes mouse
    for b in btns :
        b.handle_mouse()

    #show
    screen.fill((30, 30, 30))
    for b in btns:
        b.show()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()


btns = set()
selected_btns = set()
clicked_btn = None
