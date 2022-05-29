import cProfile
import queue
import random
from collections import deque
import numpy
"""
ncalls: numărul de apeluri
tottime: timpul total (agregat) în care a fost executată funcția curentă
percall: Raportul dintre timpul total și numărul de apeluri (cât a durat în medie o executare a acelei funcții\
cumtime: Timpul cumulat al executării funcției, împreună cu funcțiile apelate de către ea
percall: Se referă la al doilea percall din raport. Reprezintă raportul dintre timpul cumulat (cumtime) și numărul de apeluri (ncalls)
filename_lineno(function): Punctual din program, care a fost evaluat ( de exemplu un număr de linie din program sau un apel de funcție).

"""

"""
Observatie pentru cei absenti la laborator: trebuie sa dati enter după fiecare afișare a cozii/stivei până vă apare o soluție. Afișarea era ca să vedem progresul algoritmului. Puteți să o dezactivați comentând print-ul cu coada/stiva și input()

De asemenea, apelurile algoritmilor sunt la final. Este doar unul dintre ele decomentat. Voi trebuie sa comentati/decomentati apelurile în funcție de ce vă interesează sa rulați.
"""


# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    def __init__(self, id, info, parinte):
        self.id = id  # este indicele din vectorul de noduri (si din matricea de adiacenta)
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere

    def obtineDrum(self):
        l = [self.info]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte.info)
            nod = nod.parinte
        return l

    def afisDrum(self):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        print("->".join(l))
        return len(l)

    def testeazaDrum(self): #testeaza daca un drum este solutie(are exact 3 consoane)
        nr_consoane = 0
        nod = self
        if nod.info not in "aeiou": # este consoana
            nr_consoane += 1

        while nod.parinte is not None:
            if nod.parinte.info not in "aeiou":  # este consoana
                nr_consoane += 1
            nod = nod.parinte

        if nr_consoane == 3:
            return True
        else:
            return False

    def contineInDrum(self, infoNodNou):
        # return infoNodNou in self.obtineDrum()
        nodDrum = self
        while nodDrum is not None:
            if (infoNodNou == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte

        return False

    def __repr__(self):
        sir = ""
        sir += self.info + "("
        sir += "id = {}, ".format(self.id)
        sir += "drum="
        drum = self.obtineDrum()
        sir += ("->").join(drum)
        sir += ")"
        return (sir)


class Graph:  # graful problemei
    def __init__(self, noduri, matrice, start, scopuri):
        self.noduri = noduri
        self.matrice = matrice
        self.nrNoduri = len(matrice)
        self.start = start  # informatia nodului de start
        self.scopuri = scopuri  # lista cu informatiile nodurilor scop

    def indiceNod(self, n):
        return self.noduri.index(n)

    # va genera succesorii sub forma de noduri in arborele de parcurgere
    def genereazaSuccesori(self, nodCurent):
        listaSuccesori = []
        for i in range(self.nrNoduri):
            # daca am muchie si nodul i nu se afla in drumul nodului curent (atunci ar fi predecesor)
            if self.matrice[nodCurent.id][i] == 1 and not nodCurent.contineInDrum(self.noduri[i]):
                nodNou = NodParcurgere(i, self.noduri[i], nodCurent)
                listaSuccesori.append(nodNou)
        return listaSuccesori

    def testeaza_scop(self, nodCurent):
        return nodCurent.info in self.scopuri

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)


##############################################################################################
#                                 Initializare problema                                      #
##############################################################################################

# pozitia i din vectorul de noduri da si numarul liniei/coloanei corespunzatoare din matricea de adiacenta
noduri = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]

m = [
    [0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
]

start = "a"
scopuri = ["f", "j"]
gr = Graph(noduri, m, start, scopuri)


#### algoritm BF
# presupunem ca vrem mai multe solutii (un numar fix) prin urmare vom folosi o variabilă numită nrSolutiiCautate
# daca vrem doar o solutie, renuntam la variabila nrSolutiiCautate
# si doar oprim algoritmul la afisarea primei solutii



def breadth_first(gr, nrSolutiiCautate=1):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.noduri.index(gr.start), gr.start, None)]
# un nod are id(index-ul nodului de start), info, parinte

    while len(c) > 0:
        print("Coada actuala: " + str(c))
        nodCurent = c.pop(0)
        lSuccesori = gr.genereazaSuccesori(nodCurent)

        for n in lSuccesori:
            if gr.testeaza_scop(n):
                print("Solutie:")
                n.afisDrum()
                print("\n----------------\n")
                nrSolutiiCautate -= 1
                if nrSolutiiCautate == 0:
                    return
        c.extend(lSuccesori)

def depth_first(gr, nrSolutiiCautate=1):
    # vom simula o stiva prin relatia de parinte a nodului curent
    df(NodParcurgere(gr.noduri.index(gr.start), gr.start, None), nrSolutiiCautate)

"""
Rezolvare 3
"""
def df(nodCurent, nrSolutiiCautate):
    if nrSolutiiCautate <= 0:  # testul acesta s-ar valida doar daca in apelul initial avem df(start,if nrSolutiiCautate=0)
        return nrSolutiiCautate
    print("Stiva actuala: " + "->".join(nodCurent.obtineDrum()))
    if gr.testeaza_scop(nodCurent):
        print("Solutie: ", end="")
        nodCurent.afisDrum()
        print("\n----------------\n")
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return nrSolutiiCautate
    #print(f"Se expandeaza {nodCurent.info}")
    lSuccesori = gr.genereazaSuccesori(nodCurent)
    for sc in lSuccesori:
        if nrSolutiiCautate != 0:
            print(f"Se expandeaza {nodCurent.info}")
            nrSolutiiCautate = df(sc, nrSolutiiCautate)

    print("Se intoarce ->")
    return nrSolutiiCautate


# df(a)->df(b)->df(c)->df(f)
#############################################


def dfi(nodCurent, adancime, nrSolutiiCautate):
    print("Stiva actuala: " + "->".join(nodCurent.obtineDrum()))
    input()
    if adancime == 1 and gr.testeaza_scop(nodCurent):
        print("Solutie: ", end="")
        nodCurent.afisDrum()
        print("\n----------------\n")
        input()
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return nrSolutiiCautate
    if adancime > 1:
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for sc in lSuccesori:
            if nrSolutiiCautate != 0:
                #ex 5
                if nodCurent.info in expandari:
                    expandari[nodCurent.info] += 1
                else:
                    expandari[nodCurent.info] = 1

                nrSolutiiCautate = dfi(sc, adancime - 1, nrSolutiiCautate)

    return nrSolutiiCautate


def depth_first_iterativ(gr, nrSolutiiCautate=1):
    for i in range(1, gr.nrNoduri + 1):
        if nrSolutiiCautate == 0:
            return
        print("**************\nAdancime maxima: ", i)
        nrSolutiiCautate = dfi(NodParcurgere(gr.noduri.index(gr.start), gr.start, None), i, nrSolutiiCautate)



"""
Rezolvare 2
"""
def breadth_first_queue(gr):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = queue.Queue()
    c.put(NodParcurgere(gr.noduri.index(gr.start),gr.start,None))

    while not c.empty():
        nodCurent = c.get()
        lSuccesori = gr.genereazaSuccesori(nodCurent)

        for n in lSuccesori:
            c.put(n) #punem succesorul in coada
            if gr.testeaza_scop(n):
                print("Solutie:")
                n.afisDrum()
                print("\n----------------\n")

"""
Rezolvare 6
# drum solutie = drum cu 3 consoane
"""
def bf_consoane(gr):
    c = queue.Queue()
    c.put(NodParcurgere(gr.noduri.index(gr.start),gr.start,None))

    while not c.empty():
        nodCurent = c.get()
        lSuccesori = gr.genereazaSuccesori(nodCurent)

        for n in lSuccesori:
            c.put(n) #punem succesorul in coada

            if n.testeazaDrum():
                print("Solutie:")
                n.afisDrum()
                print("\n----------------\n")

"""
Rezolvare 7
"""
def bf_optimizat(gr):
    c = queue.Queue()
    c.put(NodParcurgere(gr.noduri.index(gr.start), gr.start, None))

    vizitati = [False for _ in range(len(noduri))]

    while not c.empty():
        nodCurent = c.get()
        lSuccesori = gr.genereazaSuccesori(nodCurent)

        # drumul de lungime minimă
        # se adaugă un nod în coadă doar dacă nu a mai fost deja vizitat.
        for n in lSuccesori:
            if vizitati[n.id] == False:
                vizitati[n.id] = True
                c.put(n)

            if gr.testeaza_scop(n):
                print("Solutie:")
                n.afisDrum()
                print("\n----------------\n")
                return





#breadth_first(gr, nrSolutiiCautate=4)
#cProfile.run("breadth_first(gr, nrSolutiiCautate=4)")
"""
Pentru 1:
Metoda ineficienta: 904 function calls in 4.937 seconds
Metoda eficienta: 478 function calls in 3.356 seconds
"""

"""
Rezolvare 4
"""
# generare graf aleator
def generare_graf():
    n = int(input('Introduceti numarul de noduri: '))
    noduri_nou = [str(x) for x in range(0, n)] # lista de noduri
    mat_random = numpy.random.randint(2, size=(n, n)) # matricea de adiacenta
    nr_muchii = 0

    for i in range(0, n):
        mat_random[i][i] = 0
        for j in range(0, n):
            if mat_random[i][j] == 1:
                nr_muchii += 1

    print(nr_muchii)
    print(mat_random)

    # generare nr random de scopuri
    s = '0'
    nr_scopuri = int(input('Introduceti numarul de scopuri: '))
    scopuri_random = random.sample([str(aux) for aux in range(1, n)], nr_scopuri)
    print(scopuri_random)

    graf = Graph(noduri_nou, mat_random, s, scopuri_random)

    print('DFS cu lista pe post de stiva: ')
    dfs_lista(NodParcurgere(graf.noduri.index(graf.start), graf.start, None), graf)

    print('DFS cu deque: ')
    dfs_deque(NodParcurgere(graf.noduri.index(graf.start), graf.start, None), graf)

    print('DFS cu LIFO Queue: ')
    dfs_lifoqueue(NodParcurgere(graf.noduri.index(graf.start), graf.start, None), graf)


def dfs_lista(nodCurent, graf):

    vizitat = [False for _ in range(graf.nrNoduri)]
    stiva = []
    stiva.append(nodCurent)

    while len(stiva) > 0:
        nodCurent = stiva[-1] # scot ultimul nod in lista
        stiva.pop()

        if not vizitat[int(nodCurent.info)]:
            vizitat[int(nodCurent.info)] = True
            if graf.testeaza_scop(nodCurent):
                print(f"Am gasit nodul: {nodCurent}")

        l_succesori = graf.genereazaSuccesori(nodCurent)

        for nod in l_succesori:
            if not vizitat[int(nod.info)]: # este adaugat in stiva doar daca e nevizitat
                stiva.append(nod)
    print()
    return


def dfs_deque(nodCurent, graf):

    vizitat = [False for _ in range(graf.nrNoduri)]
    deq = deque([])
    deq.append(nodCurent)

    while len(deq) > 0:
        nodCurent = deq[0]
        deq.popleft()

        if not vizitat[int(nodCurent.info)]:
            vizitat[int(nodCurent.info)] = True
            if graf.testeaza_scop(nodCurent):
                print(f"Am gasit nodul: {nodCurent}")

        l_succesori = graf.genereazaSuccesori(nodCurent)

        for nod in l_succesori:
            if not vizitat[int(nod.info)]:
                deq.append(nod)

    print()
    return

# vizitat = False cand il scot de pe stiva
def dfs_lifoqueue(nodCurent, graf):

    vizitat = [False for _ in range(graf.nrNoduri)]
    lifo = queue.LifoQueue()
    lifo.put(nodCurent)

    while not lifo.empty():
        nodCurent = lifo.get()

        if not vizitat[int(nodCurent.info)]:
            vizitat[int(nodCurent.info)] = True
            if graf.testeaza_scop(nodCurent):
                print(f"Am gasit nodul: {nodCurent}")

        l_succesori = graf.genereazaSuccesori(nodCurent)

        for nod in l_succesori:
            if not vizitat[int(nod.info)]:
                lifo.put(nod)
    print()
    return


####################################################
#breadth_first_queue(gr)

####################################################
#depth_first(gr, nrSolutiiCautate=5)
#cProfile.run("depth_first(gr, nrSolutiiCautate=5)")

##################################################
#generare_graf()

##################################################
expandari = {}
#depth_first_iterativ(gr, nrSolutiiCautate=4)
#print(expandari)

##################################
#bf_consoane(gr)
bf_optimizat(gr)
