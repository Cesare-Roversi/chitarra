from music_classes import *
from ui_classes import *

class LineeSpartitoChitarra():
    def __init__(self):
        self.depth = 0
        self.screen = None

    def build(self, x, y, distanza_tra_corde, width, screen):
        if(x):
            self.x = x
        if(y):
            self.y = y
        if(distanza_tra_corde):
            self.distanza_tra_corde = distanza_tra_corde
        if(width):
            self.width = width
        if(screen):
            self.screen = screen

    def show(self):
        for i in range(6):
            aaline_thick(self.screen, (0,0,0), (self.x, self.y+self.distanza_tra_corde*i), (self.width, self.y+self.distanza_tra_corde*i), 1)


class LineeSpartitoClassico():
    def __init__(self):
        self.depth = 0
        self.screen = None

    def build(self, x, y, distanza_tra_corde, width, screen):
        if(x):
            self.x = x
        if(y):
            self.y = y
        if(distanza_tra_corde):
            self.distanza_tra_corde = distanza_tra_corde
        if(width):
            self.width = width
        if(screen):
            self.screen = screen

    def show(self):
        for i in range(15):
            color = (0,0,0)
            if(i <5):
                color = (0,0,0)
            elif(i >=5 and i <10):
                color = (0,0,0)
            else:
                color = (255,0,0) 

            aaline_thick(self.screen, color, (self.x, self.y+self.distanza_tra_corde*i), (self.width, self.y+self.distanza_tra_corde*i), 1)
        


class SparitoChitarra():
    def __init__(self, number_of_beats, beat_value):
        #logica
        self.number_of_beats = number_of_beats
        self.beat_value = beat_value

        #visuale
        self.level =0
        self.x = None
        self.y = None
        self.tempo = 1
        self.width = 1000
        self.distanza_tra_corde = 20 #MID = 10
        self.distanza_tra_note = 15 #MID = 15
        self.distanza_separatore = 30 #MID = 30
        self.distanza_tra_spartiti = 100
        self.screen = None
        #*Spartito Chitarra
        self.grid_chitarra:list[list[ButtonNota]] = []
        self.separatori_chiatarra:list[Separatore] = []
        self.linee_spartito_chitarra:list[LineeSpartitoChitarra] = []
        #*Spartito Classico
        self.grid_classico:list[list[ButtonNota]] = []
        self.separatori_classico:list[Separatore] = []
        self.linee_spartito_classico:list[LineeSpartitoClassico] = []

        

    def build(self, x= None, y= None, list_groups:list[list[Nota]] = None, screen = None):
        if(x):
            self.x = x
        if(y):
            self.y = y
        if(screen):
            self.screen = screen

        if(list_groups):

            for grid_x in range(len(list_groups)):
                #*Riempio la griglia dello spartito chitarra
                self.grid_chitarra.append([])
                for grid_y in range(6):
                    self.grid_chitarra[grid_x].append(ButtonNota(None, (grid_x,grid_y), 20, 20, delfault_color=(100,100,0)))
            
                for n in list_groups[grid_x]:
                    grid_y = n.corda
                    self.grid_chitarra[grid_x][grid_y].set_internal_note(n)

                #*Riempio la griglia dello spartito Classico
                self.grid_classico.append([])
                for grid_y in range(15):
                    self.grid_chitarra[grid_x].append(ButtonNota(None, (grid_x,grid_y), 20, 20, delfault_color=(100,100,0)))

        #visuale
        self.linee_spartito_chitarra.append(LineeSpartitoChitarra())
        self.linee_spartito_chitarra[0].build(self.x, self.y, self.distanza_tra_corde*normY(self.screen), self.width, self.screen)
        
        nx = self.x
        ny = self.y
        limit = self.number_of_beats*self.beat_value
        counter = 0
        for grid_x in range(len(self.grid_chitarra)):
            for grid_y in range(6):
                if(counter >= limit):
                    counter = 0
                    nx += self.distanza_separatore
                    if(nx > self.x+self.width):
                        nx = self.x
                        ny = self.y+6*normY(self.screen)+self.distanza_tra_spartiti*normY(self.screen)
                        s = Separatore()
                        s.build(nx, ny, self.distanza_tra_corde*5, screen)
                        self.separatori_chiatarra.append(s)

                ny = self.y+grid_y*self.distanza_tra_corde*normY(self.screen)
                if(nx > self.x+self.width):
                    nx = self.x
                    ny = self.y+6*normY(self.screen)+self.distanza_tra_spartiti*normY(self.screen)
                
                self.grid_chitarra[grid_x][grid_y].build(None, nx, ny, (grid_x, grid_y), screen=self.screen)

            #tra una colonna e l'altra
            nx += self.x+self.distanza_tra_note*normX(self.screen)

    
    def show(self):
        for l in self.linee_spartito_chitarra:
            l.show()
        for s in self.separatori_chiatarra:
            s.show()
        for x in range(len(self.grid_chitarra)):
            for y in range(6):
                #print(f"screen: {self.grid[x][y].screen}")
                self.grid_chitarra[x][y].show()


    def handle_mouse(self):
        for g in self.grid_chitarra:
            for b in g:
                b.handle_mouse()


    def handle_event(self, event):
        for g in self.grid_chitarra:
            for b in g:
                b.handle_event(event)


    def get_btns_set(self):
        ris:set[ButtonNota] = set()
        for g in self.grid_chitarra:
            for b in g:
                ris.add(b)
        return ris
    
    def print_grid(self):
        print("---GRID DEBUG")
        for x in range(len(self.grid_chitarra)):
            for y in range(len(self.grid_chitarra[x])):
                print(self.grid_chitarra[x][y])
        print("---")

    def set_pos_in_grid(self, btn:ButtonNota, delta_x:int, delta_y:int):
        Ox, Oy = btn.grid_coo
        Nx = Ox+delta_x
        Ny = Oy+delta_y
        if(Ny <= 6 and Nx <= 1): #!NO è UN ERRORE
            #TODO manca controllo Nx espansione
            new_btn:ButtonNota = self.grid_chitarra[Nx][Ny]
            new_btn.build(nota=btn.nota)
            print(f"new_btn: {new_btn}")

        btn.nota = None


