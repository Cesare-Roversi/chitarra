import pygame
import math
pygame.init()

def normX(screen):
    width, height = screen.get_size()
    return width/1280

def normY(screen):
    width, height = screen.get_size()
    return height/720

class Debug_rect():
    def build(self, screen, bbox):
        #print(f"bbox: {bbox}")
        self.rect = pygame.Rect(bbox[0], bbox[1], bbox[2], bbox[3])
        #print(f"res {(self.rect.width, self.rect.height)}")

    def show(self, screen):
        # crea una surface temporanea con canale alpha
        s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)

        # disegna il rettangolo blu con alpha 128 (0=trasparente, 255=opaco)
        pygame.draw.rect(s, (0, 0, 255, 128), s.get_rect())

        # blitta sullo schermo nella posizione voluta
        screen.blit(s, self.rect.topleft)




class Nota():
    def __init__(self, corda, tasto, durata = 1, dest_arco =None, dest_slide =None, bend =0):#logico
        self.corda = corda
        self.tasto = tasto
        self.durata = durata
        self.dest_arco = dest_arco
        self.dest_slide = dest_slide
        self.bend = bend

    def build(self, screen, x, y):#visuale
        self.x = x #il centro del testo
        self.y = y #il centro del testo

        self.spartito:Spartito_chitarra = None #la riga dello spartito a cui appartiene

        self.padding = 5
        self.font = pygame.font.SysFont(None, 30)
        self.text_surface = self.font.render(str(self.tasto), True, (0, 0, 0))
        self.rect_behind = self.text_surface.get_rect(center=(x,y))
        self.rect_behind.width += self.padding*normX(screen)
        self.rect_behind.height += self.padding*normY(screen)
        self.rect_behind.center = (x,y)
        self.text_rect = self.text_surface.get_rect(center=(x,y))

    def get_depth(self):
        return self.spartito.depth

    def show(self, screen):
        pygame.draw.rect(screen, (255,255,255), self.rect_behind)
        screen.blit(self.text_surface, self.text_rect)
    
    def get_bbox(self): #* x assoluta, y assoluta, width, height
        # prendi metriche del carattere (lista, una tupla per ogni char)
        metrics = self.font.metrics(str(self.tasto))
        if not metrics or metrics[0] is None:
            # fallback: usa il rect della surface renderizzata
            return self.text_surface.get_rect(topleft=self.text_rect.topleft)

        #! tutto riferito ripetto al punto in alto a sinistra
        min_x_1, max_x_1, min_y_1, max_y_1, advance = metrics[0]
        max_x_2 = 0
        max_y_2 = 0
        if(len(metrics) == 2):
            _, max_x_2, _, max_y_2, _ = metrics[1]

        max_y = max(max_y_1, max_y_2)

        #! in questo modo ottieni il punto in alto a sinistra
        x0 = self.text_rect.left
        y0 = self.text_rect.top + self.font.get_ascent()

        # converti le metriche (relative alla baseline) in coordinate schermo
        left = x0 + min_x_1
        right = x0 + max_x_1 + max_x_2
        top = y0 - max_y    # max_y è distanza verso l'alto dalla baseline
        bottom = y0 - min_y_1 # min_y è distanza verso il basso dalla baseline (spesso negativa)

        # costruisci il rect (interi, larghezza/altezza non negative)
        left_i  = int(round(left))
        top_i   = int(round(top))
        width_i = max(0, int(round(right - left)))
        height_i= max(0, int(round(bottom - top)))

        return (left_i, top_i, width_i, height_i)


class Separatore():
    def build(self, screen, x, y, height):
        self.x = x
        self.y = y
        self.height = height

    def show(self, screen):
        pygame.draw.line(screen, (0,0,0), (self.x, self.y), (self.x, self.y+self.height))


class Linee_spartito():
    def build(self, screen, x, y, distanza_tra_corde, width, depth):
        self.x = x
        self.y = y
        self.distanza_tra_corde = distanza_tra_corde
        self.width = width
        self.depth = depth

    def show(self, screen):
        for i in range(6):
            pygame.draw.line(screen, (0,0,0), (self.x, self.y+self.distanza_tra_corde*i), (self.width, self.y+self.distanza_tra_corde*i))


class Arco():
    def build(self, screen, nota1:"Nota", nota2:"Nota"):
        self.nota1 = nota1
        self.nota2 = nota2
        self.sx = nota1.x
        self.sy = nota1.get_bbox()[1] -3
        self.ex = nota2.x
        self.ey = nota2.get_bbox()[1] -3
        #print(nota1.get_bbox())

        if(nota1.get_depth() == nota2.get_depth()):
            height = 20
            self.rect = pygame.Rect(self.sx, self.sy-height/2, self.ex-self.sx, height)  # x, y, width, height
            self.start_angle = 0   # pi radians (left side)
            self.end_angle = 3.14      # 0 radians (right side)
        else:
            pass
            #todo NON ho voglia
        #print(f"self.sx: {self.sx} self.sy: {self.sy} + self.ex: {self.ex} + self.ey: {self.ey}")
    
    def show(self, screen):
        if(self.nota1.get_depth() == self.nota2.get_depth()): #todo rimuovere quando fixi ^
            pygame.draw.arc(screen, (0,0,0), self.rect, self.start_angle, self.end_angle, 2)


class Slide():
    def build(self, screen, nota1:"Nota", nota2:"Nota"):
        self.nota1 = nota1
        self.nota2 = nota2
        left_1, top_1, width_1, height_1 = nota1.get_bbox()
        left_2, top_2, width_2, height_2 = nota2.get_bbox()
        self.sx = left_1+width_1+3
        self.sy = top_1 +3
        self.ex = left_2-3
        self.ey = top_2+height_2 -3

        #todo NON ho voglia

    def show(self, screen):
        if(self.nota1.get_depth() == self.nota2.get_depth()): #todo rimuovere quando fixi ^
            pygame.draw.line(screen, (0,0,0), (self.sx, self.sy), (self.ex, self.ey), 2)


class Bend():
    def build(self, screen, nota, intensity =1):
        left_1, top_1, width_1, height_1 = nota.get_bbox()
        self.sx = left_1+width_1+3
        self.sy = top_1+3
        height = 140*intensity*normY(screen)
        width = 10
        self.rect = pygame.Rect(self.sx-width_1/2, self.sy-height, width, height)  # x, y, width, height
        self.start_angle = 3.14   # pi radians (left side)
        self.end_angle = 0     # 0 radians (right side)

        self.testo_x = self.sx + width #il centro del testo
        self.testo_y = self.sy - height/4 #il centro del testo
        self.font = pygame.font.SysFont(None, 15)
        self.text_surface = self.font.render(self.get_fraction(intensity), True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(center=(self.testo_x, self.testo_y))

    def get_fraction(self, i):
        if(i == 1):
            return "full"
        if(i == 0.75):
            return "3/4"
        if(i >= 0.6 and i <0.7):
            return "2/3"
        if(i == 0.5):
            return "1/2"
        if(i >= 0.3 and i <= 0.4):
            return "1/3"
        if(i == 0.25):
            return "1/4"
        if(i == 0.2):
            return "1/5"
        return "???"

    def show(self, screen):
        pygame.draw.arc(screen, (0,0,0), self.rect, math.pi*1.5, 0, 1)
        screen.blit(self.text_surface, self.text_rect)





class Spartito_chitarra():
    def __init__(self, tempo = 1, list_note = []):
        self.list_note:list[list] = list_note
        self.tempo = tempo

    def build(self, screen, x, y, width):
        #parametri visuali
        screen_width, screen_height = screen.get_size()
        distanza_tra_corde = 20*normY(screen)
        distanza_tra_note = 20*normX(screen)
        distanza_separatore = 40*normX(screen)
        distanza_tra_spartiti = 100*normY(screen)
        self.x = x #angolo in alto a sx spartito
        self.y = y #
        self.width = width

        #variabili
        self.list_figli = []
        
        count_depth_spartiti = 0 
        x_relativa = x
        y_relativa = y
        linee = Linee_spartito()
        linee.build(screen, x, y, distanza_tra_corde, width, count_depth_spartiti)
        self.list_figli.append(linee)
        count_durata_note = 0
        for note_contemporanee in self.list_note:

            note_contemporanee:Nota
            count_durata_note += note_contemporanee[0].durata
            if(count_durata_note > self.tempo):
                #print(f"x_relativa: {x_relativa}")
                count_durata_note = 0
                sep = Separatore() 
                x_relativa += distanza_separatore
                sep.build(screen, x_relativa, y_relativa, distanza_tra_corde*5)
                self.list_figli.append(sep)
                x_relativa += distanza_separatore

            if(x_relativa > self.width-50):
                x_relativa = x
                y_relativa += distanza_tra_corde*5 +distanza_tra_spartiti
                linee = Linee_spartito()
                count_depth_spartiti +=1
                linee.build(screen, x_relativa, y_relativa, distanza_tra_corde, width, count_depth_spartiti)
                self.list_figli.append(linee)

            x_relativa += distanza_tra_note
            for nota in note_contemporanee: #add Note objects
                y_nota = y_relativa + distanza_tra_corde*(nota.corda-1)
                nota.build(screen, x_relativa, y_nota)
                nota.spartito = linee
                self.list_figli.append(nota)
            x_relativa += distanza_tra_note

        #*archi, slide, bend
        for note in self.list_note:
            for nota in note:
                nota:Nota
                bbox = nota.get_bbox()
                d = Debug_rect() #debug
                d.build(screen, bbox)
                self.list_figli.append(d)
                if(nota.dest_arco != None):
                    arco = Arco()
                    arco.build(screen, nota, nota.dest_arco)
                    self.list_figli.append(arco)

                if(nota.dest_slide != None):
                    slide = Slide()
                    slide.build(screen, nota, nota.dest_slide)
                    self.list_figli.append(slide)

                if(nota.bend != 0):
                    bend = Bend()
                    bend.build(screen, nota, nota.bend)
                    self.list_figli.append(bend)



    def show(self, screen):
        for f in self.list_figli:
            f.show(screen)




            


