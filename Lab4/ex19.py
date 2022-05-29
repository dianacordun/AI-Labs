"""
Dati enter dupa fiecare solutie afisata.

Presupunem ca avem costul de mutare al unui bloc egal cu indicele in alfabet, cu indicii incepănd de la 1 (care se calculează prin 1+ diferenta dintre valoarea codului ascii al literei blocului de mutat si codul ascii al literei "a" ) . Astfel A* are trebui sa prefere drumurile in care se muta intai blocurile cu infomatie mai mica lexicografic pentru a ajunge la una dintre starile scop
"""

import copy
from math import gcd
from sympy import isprime


# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    def __init__(self, info, parinte, cost=0, h=0):
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost  # consider cost=1 pentru o mutare
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        for nod in l:
            print(str(nod))
        if afisCost:
            print("Cost: ", self.g)
        if afisCost:
            print("Lungime: ", len(l))
        return len(l)

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:
            if (infoNodNou == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte

        return False

    def __repr__(self):
        sir = ""
        sir += str(self.info)
        return (sir)

    # euristica banală: daca nu e stare scop, returnez 1, altfel 0

    def __str__(self):
        sir = ""
        maxInalt = max([len(stiva) for stiva in self.info])
        for inalt in range(maxInalt, 0, -1):
            for stiva in self.info:
                if len(stiva) < inalt:
                    sir += "  "
                else:
                    sir += str(stiva[inalt - 1]) + " "
            sir += "\n"
        sir += "-" * (2 * len(self.info) - 1)
        return sir


class Graph:  # graful problemei
    def __init__(self, nume_fisier):

        def obtineStive(sir):
            stiveSiruri = sir.strip().split("\n")  # ["a","c b","d"]
            listaStive = [sirStiva.strip().split() if sirStiva != "#" else [] for sirStiva in stiveSiruri]
            #  In aceasta varianta blocurile au valori numerice.
            listaStive = [[int(x) for x in stiva] for stiva in listaStive]

            return listaStive

        f = open(nume_fisier, 'r')

        continutFisier = f.read()  # citesc tot continutul fisierului
        siruriStari = continutFisier.split("stari_finale")
        self.start = obtineStive(siruriStari[0])  # [["a"], ["c","b"],["d"]]

    # O stare este scop daca toate stivele au ca valori doar blocuri cu
    # cmmdc != 1 (cmmdc(blocurile de pe stiva) > 1)
    def testeaza_scop(self, nodCurent):
        for stiva in nodCurent.info:
            # gcd = cmmdc
            if gcd(*stiva) == 1:
                return False
        return True

    # va genera succesorii sub forma de noduri in arborele de parcurgere
    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
        listaSuccesori = []
        stive_c = nodCurent.info  # stivele din nodul curent
        nr_stive = len(stive_c)
        for idx in range(nr_stive):  # idx= indicele stivei de pe care iau bloc

            if len(stive_c[idx]) == 0:
                continue
            copie_interm = copy.deepcopy(stive_c)
            bloc = copie_interm[idx].pop()  # iau varful stivei
            for j in range(nr_stive):  # j = indicele stivei pe care pun blocul
                if idx == j:  # nu punem blocul de unde l-am luat
                    continue
                stive_n = copy.deepcopy(copie_interm)  # lista noua de stive
                stive_n[j].append(bloc)  # pun blocul
                costMutareBloc = bloc
                if not nodCurent.contineInDrum(stive_n):
                    nod_nou = NodParcurgere(stive_n, nodCurent, cost=nodCurent.g + costMutareBloc,
                                            h=self.calculeaza_h(stive_n, tip_euristica))
                    listaSuccesori.append(nod_nou)

        return listaSuccesori

    # euristica banala
    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
        if tip_euristica == "euristica banala":
            flag = 0
            for stiva in infoNod:
                if gcd(*stiva) == 1:
                    flag = 1 # daca nu indeplineste conditia
            if flag:
                return 1 # se pune costul minim pe o mutare
            return 0
        # !
        elif tip_euristica == "euristica admisibila 4":
            euristici = []
            h = 0
            # euristica = cate elemente au gcd 1 dintr-o stiva
            for stiva in infoNod:
                for iElem, Elem in enumerate(stiva):
                    for otherElem in stiva[iElem:]:
                        if gcd(Elem, otherElem) == 1:
                            h += otherElem
            euristici.append(h)
            return min(euristici)

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)


def breadth_first(gr, nrSolutiiCautate):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None)]

    while len(c) > 0:
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            print("Solutie:")
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            print("\n----------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        c.extend(lSuccesori)


def a_star(gr, nrSolutiiCautate, tip_euristica):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]

    while len(c) > 0:
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            print("Solutie: ")
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            print("\n----------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # diferenta fata de UCS e ca ordonez dupa f
                if c[i].f >= s.f:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)

# de modificat pt n
def exista_solutie(stive):
    # toate stivele trebuie sa aiba minim un element
    if all(len(stiva) <= 1 for stiva in stive):
        return True

    # 1 nu trebuie sa fie element pe nicio stiva
    for stiva in stive:
        for el in stiva:
            if el == 1:
                return False

    l_prime = []
    for stiva in stive:
        for elem in stiva:
            if isprime(elem):
                l_prime.append(elem)
                if len(l_prime) > 3: # nr de nr prime = max nr de stive
                    return False
    if len(l_prime) == 3:
        # daca avem 3 nr prime, atunci trebuie ca fiecare
        # alt element sa se imparta la minim unul dintre ele
        for stiva in stive:
            for elem in stiva:
                # daca nu se imparte la niciunul
             if all(elem % nr for nr in l_prime):
                return False
    elif len(l_prime) == 2:
        # daca avem 2 nr prime, atunci fiecare nr trb fie sa
        # se imparta la un nr prim, fie toate cele care nu se "incadreaza"
        # sa aiba cmmdc != 1
        l_stiva3 = []
        for stiva in stive:
            for elem in stiva:
            # daca nu se imparte la niciunul
             if all(elem % nr for nr in l_prime):
                l_stiva3.append(elem)
        for el in l_stiva3: #elementele care nu se pot afla pe stive cu nr prime
            if gcd(*el) == 1:
                return False
    elif len(l_prime) == 1:
        pass
        # daca avem 1 nr prim, atunci fie se imparte la nr respectiv, fie
        # avem o lista de numere ce trebuie impartita in 2 cu cmmdc != 1
    else: # len(l_prime) == 0
        pass



gr = Graph("input_nou.txt")

# Rezolvat cu breadth first
"""
print("Solutii obtinute cu breadth first:")
breadth_first(gr, nrSolutiiCautate=3)
"""

# print("\n\n##################\nSolutii obtinute cu A*:")
a_star(gr, nrSolutiiCautate=3, tip_euristica="euristica admisibila 4")
