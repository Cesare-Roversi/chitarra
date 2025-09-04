import random
from spartito import Nota

def find_next(lista_note, ix, corda):
    LIMIT = 3
    count = 0
    for g_ix in range(ix+1, len(lista_note)):
        if(count >= LIMIT):
            break
        for n in lista_note[g_ix]:
            n:Nota
            if(n.corda == corda):
                return n 
        count +=1
    return None

def Generatore():
    LEN = 80 #gruppi verticali
    N_FRET = 30

    lista_note = []
    for g_ix in range(LEN):
        gruppo = []
        for corda in range (1, 7):
            r = random.uniform(0, 1)
            if(r <= 0.25):
                fret = random.randint(0, 30)  # 0 e 30 inclusi
                nota = Nota(corda, fret, 0.25)
                gruppo.append(nota)

        if(len(gruppo) != 0):
            lista_note.append(gruppo)

    #* archi, bend, slide
    for gruppo_ix in range(len(lista_note)):
        gruppo = lista_note[gruppo_ix]
        for nota in gruppo:
            nota:Nota
            r_arco = random.uniform(0, 1)
            if(r_arco <= 0.5):
                next_nota = find_next(lista_note, gruppo_ix, nota.corda)
                #print(f"next_nota: {next_nota}")
                nota.dest_arco = next_nota

            r_slide = random.uniform(0, 1)
            if(r_slide <= 0.5):
                next_nota = find_next(lista_note, gruppo_ix, nota.corda)
                #print(f"next_nota: {next_nota}")
                nota.dest_slide = next_nota

            r_bend = random.uniform(0, 1)
            if(r_bend < 0.2):
                ch = [0.3, 0.5, 0.6, 1]
                nota.bend = random.choice(ch)


    return lista_note