import pygame
from ui_classes.ButtonNota import *
from music_classes import Nota

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

nota = Nota(0,0,1)
btn = ButtonNota(nota, (0,0), 240, 80, delfault_color=(30, 144, 255), transparency=220, level=1)
btn.build(None, 300, 300, (0,0), screen)

nota1 = Nota(0,1,1)
btn1 = ButtonNota(nota1, (0,0), 240, 80, delfault_color=(30, 144, 255), transparency=220, level=1)
btn1.build(None, 100, 100, (0,0), screen)

print(nota1.get_bbox())

def handler_spartito(event, keys, clicked_note, btns, selected_btns):
    #key list
    CTRL = keys & pygame.KMOD_CTRL

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left mouse down
        print("MOUSE DOWN")
        found = False
        for ix, dest in enumerate(btns):
            if dest.check_click(event.pos):  # assumiamo che esista
                clicked_note = dest
                found = True
                
        if(not found):
            for s in selected_btns:
                s.selected_color(False)
            clicked_note = None
            selected_btns.clear()


    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # left mouse up
        print("MOUSE UP")
        if clicked_note and clicked_note.check_click(event.pos):
            if clicked_note in selected_btns:
                selected_btns.remove(clicked_note)
                clicked_note.selected_color(False)
            else:
                clicked_note.selected_color()
                selected_btns.add(clicked_note)
            print(f"selected_notes: {selected_btns}")

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
                    #n.set_internal_note(s.steal_internal_note())
                    found = True
                    deltaX = n.grid_coo[0]-s.grid_coo[0]
                    deltaY = n.grid_coo[1]-s.grid_coo[1]
                    for s in selected_notes:
                        new_posX = s.grid_coo[0]+deltaX
                        new_posY = s.grid_coo[1]+deltaY
                        #btns_grid[new_posX][new_posY].set_iternal_note(s.steal_internal_note())


    return clicked_note

notes = set()
notes.update([btn, btn1])

selected_notes = set()
clicked_note = None
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #internal notes handler
        for b in notes :
            b.handle_event(event)
        keys = pygame.key.get_mods()
        clicked_note = handler_spartito(event, keys, clicked_note, notes, selected_notes) #premere un bottone è un evento? boh

    #internal notes mouse
    for b in notes :
        b.handle_mouse()

    #show
    screen.fill((30, 30, 30))
    for b in notes:
        b.show()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()


notes = set()
selected_notes = set()
clicked_note = None
