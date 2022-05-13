# informatii despre un nod din arborele de parcurgere (nu din graful initial)
import multiprocessing
import queue
import random
import time
from math import sqrt
from random import randint

g = open("output.txt","w")

def este_prim(n):
    prime_flag = 0

    if n > 1:
        for i in range(2, int(sqrt(n)) + 1):
            if n % i == 0:
                prime_flag = 1
                break
        if prime_flag == 0:
            return True
        else:
            return False
    else:
        return False

def nr_prime(l):
    count = 0
    for nr in l:
        if este_prim(nr):
            count += 1
    return count

def nr_pare(l):
    count = 0
    for nr in l:
        if not nr % 2:
            count +=1
    return count

def exista_divizor(l1,l2):
    for x in l1:
        for y in l2:
            if not x % y:
                return True
    return False

# param: o lista de 3 elem reprezentand valorile nodului curent si lista valorilor tuturor nodurilor
# scop: returneaza o lista de elemente reprezentand indecsii vecinilor nodurilor
def calculeazaVecini(val_nod_curent, l_valori):
    vecini = []
    for i in range(len(l_valori)):
        if l_valori[i] != val_nod_curent:
            # cazul a
            counter1 = nr_prime(val_nod_curent)
            counter2 = nr_prime(l_valori[i])
            if counter1 >= counter2:
                vecini.append(i)
                continue

            # cazul b
            if nr_pare(val_nod_curent) == nr_pare(l_valori[i]):
                vecini.append(i)
                continue

            # cazul c
            if max(val_nod_curent) > max(l_valori[i]):
                vecini.append(i)
                continue

            # cazul d
            if exista_divizor(val_nod_curent,l_valori[i]):
                vecini.append(i)
                continue

            # cazul e
            suma = sum(val_nod_curent)
            if suma >= min(l_valori[i]) and suma <= max(l_valori[i]):
                vecini.append(i)
                continue

            # cazul f
            counter1 = 3 - nr_pare(val_nod_curent)
            counter2 = 3 - nr_pare(l_valori[i])
            if counter1 != 0 and counter2 != 0 and counter1 > counter2:
                vecini.append(i)

    return vecini


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
        g.write("->".join(l)+ "\n")
        print("->".join(l))
        return len(l)

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
    def __init__(self, noduri, liste_vecini, start, scopuri, valori):
        self.noduri = noduri
        self.liste_vecini = liste_vecini
        self.nrNoduri = len(liste_vecini)
        self.start = start  # informatia nodului de start
        self.scopuri = scopuri  # lista cu informatiile nodurilor scop
        self.valori = valori #lista cu valorile tuturor nodurilor

    def indiceNod(self, n):
        return self.noduri.index(n)

    # va genera succesorii sub forma de noduri in arborele de parcurgere
    def genereazaSuccesori(self, nodCurent):
        listaSuccesori = []

        for i in range(self.nrNoduri):
            # daca nodul nu are deja lista de vecini, trebuie calculata
            if not self.liste_vecini[nodCurent.id]:
                self.liste_vecini[nodCurent.id] = calculeazaVecini(self.valori[nodCurent.id], self.valori)

            # daca am muchie si nodul i nu se afla in drumul nodului curent (atunci ar fi predecesor)
            if i in self.liste_vecini[nodCurent.id] and not nodCurent.contineInDrum(self.noduri[i]):
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

# Generam aleator N noduri cu 70 <= N <= 100
N = randint(70, 100)
g.write(f"Numarul de noduri nescop este: {N}\n")
print(f"Numarul de noduri nescop este: {N}")


noduri = [str(x) for x in range(0, N+3)] # lista de noduri + 3 pt scopuri

valori = []  # lista de valori ale nodurilor
for x in range(0, N):
    l1, l2, l3 = random.sample(range(1, 101), 3)# Vector aleator de 3 numere cu valori între 1 și 100
    valori.append([l1, l2, l3])  # n = [l1,l2,l3]

m = [[] for _ in range(N)] # lista de vecini

start = str(randint(0, N - 1))
g.write(f"Nodul de start este: {start}\n")
print(f"Nodul de start este: {start}")

# Pe lângă cele N noduri se vor genera și 3 noduri scop
scopuri = noduri[-3:]
valori.append([4, 2, 3])
valori.append([2, 3, 5])
valori.append([8, 2, 4])

gr = Graph(noduri, m, start, scopuri, valori)

###################################################################################
def breadth_first(gr, nrSolutiiCautate=1):

    c = queue.Queue()
    c.put(NodParcurgere(gr.noduri.index(gr.start), gr.start, None))
    vizitati = [False for _ in range(len(noduri))]

    while not c.empty():
        nodCurent = c.get()
        lSuccesori = gr.genereazaSuccesori(nodCurent)

        # drumul de lungime minimă
        # se adaugă un nod în coadă doar dacă nu a mai fost deja vizitat.
        for n in lSuccesori:
            if not vizitati[n.id]:
                vizitati[n.id] = True
                c.put(n)

            if gr.testeaza_scop(n):
                g.write("Solutie:\n")
                print("Solutie:")
                n.afisDrum()
                g.write("\n----------------\n\n")
                print("\n----------------\n")
                nrSolutiiCautate -= 1
                if nrSolutiiCautate == 0:
                    return

def depth_first(gr, nrSolutiiCautate=1):
    # vom simula o stiva prin relatia de parinte a nodului curent
    df(NodParcurgere(gr.noduri.index(gr.start), gr.start, None), nrSolutiiCautate)


def df(nodCurent, nrSolutiiCautate):
    if nrSolutiiCautate <= 0:  # testul acesta s-ar valida doar daca in apelul initial avem df(start,if nrSolutiiCautate=0)
        return nrSolutiiCautate
    g.write("Stiva actuala: " + "->".join(nodCurent.obtineDrum()) + "\n")
    #print("Stiva actuala: " + "->".join(nodCurent.obtineDrum()))
    if gr.testeaza_scop(nodCurent):
        g.write("Solutie:\n")
        print("Solutie: ", end="")
        nodCurent.afisDrum()
        g.write("\n----------------\n\n")
        print("\n----------------\n")
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return nrSolutiiCautate
    lSuccesori = gr.genereazaSuccesori(nodCurent)
    for sc in lSuccesori:
        if nrSolutiiCautate != 0:
            nrSolutiiCautate = df(sc, nrSolutiiCautate)

    return nrSolutiiCautate



def dfi(nodCurent, adancime, nrSolutiiCautate):
    g.write("Stiva actuala: " + "->".join(nodCurent.obtineDrum()) + "\n")
    print("Stiva actuala: " + "->".join(nodCurent.obtineDrum()))
    if adancime == 1 and gr.testeaza_scop(nodCurent):
        g.write("Solutie:\n")
        print("Solutie: ", end="")
        nodCurent.afisDrum()
        g.write("\n----------------\n\n")
        print("\n----------------\n")
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return nrSolutiiCautate
    if adancime > 1:
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for sc in lSuccesori:
            if nrSolutiiCautate != 0:
                nrSolutiiCautate = dfi(sc, adancime - 1, nrSolutiiCautate)
    return nrSolutiiCautate


def depth_first_iterativ(gr, nrSolutiiCautate=1):
    for i in range(1, gr.nrNoduri + 1):
        if nrSolutiiCautate == 0:
            return
        g.write(f"**************\nAdancime maxima: {i} \n")
        #print("**************\nAdancime maxima: ", i)
        nrSolutiiCautate = dfi(NodParcurgere(gr.noduri.index(gr.start), gr.start, None), i, nrSolutiiCautate)


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=breadth_first, name="BF", args=(gr,5))
    p1.start()
    p2 = multiprocessing.Process(target=depth_first, name="DF", args=(gr, 5))
    p2.start()
    p3 = multiprocessing.Process(target=depth_first_iterativ, name="DFI", args=(gr, 5))
    p3.start()

    # Asteapta 3 minute
    time.sleep(180)

    # Termina toate procesele
    p1.terminate()
    p2.terminate()
    p3.terminate()

    # Asteapta ca toate thread-urile sa se termine
    p1.join()
    p2.join()
    p3.join()

    g.close()

"""
Un nod scop care sigur ar avea solutie ar fi [2,3,5]
Fiind toate prime => exista arc de la acest nod la oricare alt nod
"""

