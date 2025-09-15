import pygame
from ui_classes import *
from music_classes import Nota
from custom_exceptions import *
from DebugTools import *

pygame.init()
screen = pygame.display.set_mode((1500, 1000))
clock = pygame.time.Clock()

nota0 = Nota(0,0,1)
nota1 = Nota(1,1,1)
nota3 = Nota(0,2,1)
nota4 = Nota(1,3,1)
notes = [[nota0, nota1], [nota3, nota4]]


spartito_chitarra = SparitoChitarra(4,4)
spartito_chitarra.build(50, 50, notes, screen)

spartito_chitarra.print_grid()


def handler_spartito(event, keys, btns:set[ButtonNota], selected_btns:set[ButtonNota], box_select_start_coo:tuple[float,float], box_select_active:bool, box_selection:BoxSelection):
    #key list
    CTRL = keys & pygame.KMOD_CTRL

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left mouse down
        print("MOUSE DOWN")
        clicked_btn = None
        pressed_a_button = False
        for ix, dest in enumerate(btns):
            if dest.check_click(event.pos):
                clicked_btn = dest
                pressed_a_button = True   
        if(pressed_a_button and not CTRL):#*add or remove single button
            if clicked_btn in selected_btns:
                selected_btns.remove(clicked_btn)
                clicked_btn.selected_color(False)
            else:
                clicked_btn.selected_color()
                selected_btns.add(clicked_btn)
        elif(not pressed_a_button):
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
        if(box_select_active):#* you are selecting with box_selection
            box_select_end_coo = event.pos
            box_select_active = False
            for btn in btns:
                if(btn.check_overlap(box_selection.get_bbox())):
                    selected_btns.add(btn)
                    btn.selected_color(True)
        else:#* you are dragging
            found_valid_destination = False
            for any_btn in btns:
                if(found_valid_destination):
                    break
                for sel_btn in selected_btns:
                    any_btn:ButtonNota
                    sel_btn:ButtonNota
                    try:
                        if(sel_btn != any_btn and any_btn.check_overlap(sel_btn.get_note_bbox())):
                            print("diebymyhand")
                            #n.set_internal_note(s.steal_internal_note())
                            found_valid_destination = True
                            deltaX = any_btn.grid_coo[0]-sel_btn.grid_coo[0]
                            deltaY = any_btn.grid_coo[1]-sel_btn.grid_coo[1]
                            for sel_btn in selected_btns:
                                spartito_chitarra.set_pos_in_grid(sel_btn, deltaX, deltaY)
                    except NotaAssente:
                        pass
            #clear after dragging
            if(found_valid_destination):#evita il problema di quando riclicchi su un selezionato x deselezionarlo
                for s in selected_btns:
                    s.selected_color(False)
                selected_btns.clear()

    return (box_select_start_coo, box_select_active)


#handler vars
btns = spartito_chitarra.get_btns_set()
selected_btns = set()
box_select_start_coo:tuple[float,float] = None
box_selection = BoxSelection()
box_select_active = False

running = True
while running:
    #internal notes mouse handler
    spartito_chitarra.handle_mouse()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #internal notes event handler
        spartito_chitarra.handle_event(event)
        keys = pygame.key.get_mods()
        box_select_start_coo, box_select_active = handler_spartito(event, keys, btns, selected_btns, box_select_start_coo, box_select_active, box_selection) #premere un bottone è un evento? boh


    #show
    screen.fill((255, 255, 255))
    spartito_chitarra.show()
    box_selection.build(box_select_active, box_select_start_coo, pygame.mouse.get_pos(), screen)
    box_selection.show()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()


btns = set()
selected_btns = set()

