import pygame
from ui_classes import *
from music_classes import Nota
from custom_exceptions import *
from DebugTools import *

pygame.init()
screen = pygame.display.set_mode((1500, 1000))
clock = pygame.time.Clock()

nota = Nota(0,0,1)
nota1 = Nota(0,1,1)
notes = [[nota], [nota1]]


spartito_chitarra = SparitoChitarra(4,4)
spartito_chitarra.build(50, 50, notes, screen)


def handler_spartito(event, keys, btns:set[ButtonNota], selected_btns:set[ButtonNota], box_select_start_coo:tuple[float,float], box_select_active:bool):
    #key list
    CTRL = keys & pygame.KMOD_CTRL

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left mouse down
        print("MOUSE DOWN")
        clicked_btn = None
        found = False
        for ix, dest in enumerate(btns):
            if dest.check_click(event.pos):
                clicked_btn = dest
                found = True   
        if(found and not CTRL):#*add or remove single button
            if clicked_btn in selected_btns:
                selected_btns.remove(clicked_btn)
                clicked_btn.selected_color(False)
            else:
                clicked_btn.selected_color()
                selected_btns.add(clicked_btn)
        elif(not found):
            if(not CTRL):#*clear selected[]
                for sel_btn in selected_btns:
                    sel_btn.selected_color(False)
            #*box_selection
            box_select_start_coo = event.pos
            box_select_active = True
            clicked_btn = None
            selected_btns.clear()


    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # left mouse up
        print("MOUSE UP")

        print(f"selected_notes: {selected_btns}")
        if(box_select_active):#* you are selecting
            box_select_end_coo = event.pos
            W = box_select_end_coo[0]-box_select_start_coo[0]
            H = box_select_end_coo[1]-box_select_start_coo[1]
            bbox = (box_select_start_coo[0], box_select_start_coo[1], W, H)
            box_select_active = False
            for btn in btns:
                if(btn.check_overlap(bbox)):
                    selected_btns.add(btn)
                    btn.selected_color(True)
        else:#* you are dragging
            found = False
            for any_btn in btns:
                if(found):
                    break
                for sel_btn in selected_btns:
                    any_btn:ButtonNota
                    sel_btn:ButtonNota
                    try:
                        if(sel_btn != any_btn and any_btn.check_overlap(sel_btn.get_note_bbox())):
                            print("diebymyhand")
                            #n.set_internal_note(s.steal_internal_note())
                            found = True
                            deltaX = any_btn.grid_coo[0]-sel_btn.grid_coo[0]
                            deltaY = any_btn.grid_coo[1]-sel_btn.grid_coo[1]
                            for sel_btn in selected_btns:
                                spartito_chitarra.set_pos_in_grid(sel_btn, deltaX, deltaY)
                            break
                    except NotaAssente:
                        pass

    return (box_select_start_coo, box_select_active)


#handler vars
btns = spartito_chitarra.get_btns_set()
selected_btns = set()
box_select_start_coo:tuple[float,float] = None
box_selection = BoxSelection()
box_select_active = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #internal notes event handler
        spartito_chitarra.handle_event(event)
        keys = pygame.key.get_mods()
        box_select_start_coo, box_select_active = handler_spartito(event, keys, btns, selected_btns, box_select_start_coo, box_select_active) #premere un bottone è un evento? boh

    #internal notes mouse handler
    spartito_chitarra.handle_mouse()

    #show
    screen.fill((255, 255, 255))
    spartito_chitarra.show()
    if(box_select_active):
        printv("pos", pygame.mouse.get_pos(), "box", box_select_start_coo)
        box_selection.build(box_select_start_coo, pygame.mouse.get_pos(), screen)
        box_selection.show()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()


btns = set()
selected_btns = set()

