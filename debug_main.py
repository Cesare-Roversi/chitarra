import pygame
from ui_classes import *
from music_classes import Nota
from custom_exceptions import *

pygame.init()
screen = pygame.display.set_mode((1500, 1000))
clock = pygame.time.Clock()

nota = Nota(0,0,1)
nota1 = Nota(0,1,1)
notes = [[nota], [nota1]]


spartito_chitarra = SparitoChitarra(4,4)
spartito_chitarra.build(50, 50, notes, screen)


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
            for sel_btn in selected_btns:
                sel_btn.selected_color(False)
            clicked_btn = None
            selected_btns.clear()


    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # left mouse up
        print("MOUSE UP")

        print(f"selected_notes: {selected_btns}")
        found = False
        for any_btn in btns:
            if(found):
                break
            for sel_btn in selected_btns:
                any_btn:ButtonNota
                sel_btn:ButtonNota
                try:
                    if(sel_btn != any_btn and any_btn.check_inside(sel_btn.get_note_bbox())):
                        print("diebymyhand")
                        #n.set_internal_note(s.steal_internal_note())
                        found = True
                        deltaX = any_btn.grid_coo[0]-sel_btn.grid_coo[0]
                        deltaY = any_btn.grid_coo[1]-sel_btn.grid_coo[1]
                        for sel_btn in selected_btns:
                            spartito_chitarra.set_pos_in_grid(sel_btn, deltaX, deltaY)
                except NotaAssente:
                    pass


    return clicked_btn

btns = spartito_chitarra.get_btns_set()

selected_btns = set()
clicked_btn = None
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #internal notes event handler
        spartito_chitarra.handle_event(event)
        keys = pygame.key.get_mods()
        clicked_btn = handler_spartito(event, keys, clicked_btn, btns, selected_btns) #premere un bottone è un evento? boh

    #internal notes mouse handler
    spartito_chitarra.handle_mouse()

    #show
    screen.fill((255, 255, 255))
    spartito_chitarra.show()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()


btns = set()
selected_btns = set()
clicked_btn = None
