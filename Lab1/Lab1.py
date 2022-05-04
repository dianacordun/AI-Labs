import os
import random


class Elev:
    i = 0
    d_activitati = {}

    def __init__(self, nume=None, sanatate=90, inteligenta=20, oboseala=0, buna_dispozitie=100, lista_activitati=[]):
        if nume == None:
            self.nume = self.necunoscut_i
        else:
            self.nume = nume

        self.sanatate = sanatate
        self.inteligenta = inteligenta
        self.oboseala = oboseala
        self.buna_dispozitie = buna_dispozitie
        self.lista_activitati = lista_activitati

    @classmethod
    def necunoscut_i(cls):
        cls.i += 1
        return "Necunoscut_" + f"{cls.i}"

    def incepe_activitate(self, activitate):
        self.activitate_curenta = activitate
        self.timp_executat_activ = 0

    def desfasoara_activitate(self):
        self.incepe_activitate(self.lista_activitati[0])

    def trece_ora(self, ora_curenta):
        d = self.activitate_curenta.durata
        if self.timp_executat_activ == d:
            return False

        # Executa inca o ora din activitatea curenta
        self.timp_executat_activ += 1

        fs = self.activitate_curenta.factor_sanatate / d
        fi = self.activitate_curenta.factor_inteligenta / d
        fo = self.activitate_curenta.factor_oboseala / d
        fd = self.activitate_curenta.factor_dispozitie / d

        # Activitatile din acest interval scad sanatatea cu 1 per ora
        if ora_curenta >= 6 and ora_curenta <= 22 and self.activitate_curenta.nume != "dormit":
            if self.sanatate >= d:
                self.sanatate -= d

        # Daca oboseala a ajuns la 100, orice aport va fi la jumatate
        aport = 1
        if self.oboseala + fo >= 100:
            self.oboseala = 100
            aport = 0.5
        else:
            if self.oboseala + fo < 0:
                self.oboseala = 0
            else:
                self.oboseala += fo

        if (self.sanatate + fs) * aport > 100:
            self.sanatate = 100
        else:
            if (self.sanatate + fs) * aport < 0:
                self.sanatate = 0
            else:
                self.sanatate = (self.sanatate + fs) * aport

        if (self.inteligenta + fi) * aport > 100:
            self.inteligenta = 100
        else:
            if (self.inteligenta + fi) * aport < 0:
                self.inteligenta = 0
            else:
                self.inteligenta = (self.inteligenta + fi) * aport

        if (self.buna_dispozitie + fd) * aport > 100:
            self.buna_dispozitie = 100
        else:
            if (self.buna_dispozitie + fd) * aport < 0:
                self.buna_dispozitie = 0
            else:
                self.buna_dispozitie = (self.buna_dispozitie + fd) * aport

        # Elevul a terminat activitatea curenta
        if self.timp_executat_activ == d:
            self.lista_activitati.pop(0)
            self.desfasoara_activitate()
        return True

    def testeaza_final(self):
        if self.sanatate == 0:
            return True, "Elevul este bolnav"
        if self.buna_dispozitie == 0:
            return True, "Elevul este depresiv"
        if self.inteligenta == 100:
            print(f"Elevul {self.nume} a absolvit scoala!")
            return True, "Elevul a terminat scoala"
        return False

    def afiseaza_raport(self):
        raport = {}

        for a in self.lista_activitati:
            activ = Elev.d_activitati[a]
            if a not in raport.keys():
                raport[a] = activ.durata
            else:
                raport[a] += activ.durata
        print("Raportul elevului:")
        for act, ore in raport.items():
            print(act, ore)
        return raport

    def salveaza_raport(self, cale_folder):
        raport = self.afiseaza_raport()
        nume_fisier = self.nume+".txt"
        nume_complet = os.path.join(cale_folder, nume_fisier)
        with open(nume_complet, 'w') as g:
            g.write("Raportul elevului:")
            for act, ore in raport.items():
                g.write(f"{act} : {ore} ore")

        stare, cauza = self.testeaza_final()
        if stare:
            g.write(cauza)

    def __repr__(self):
        sir = "Prop clasa:\n"
        for (k, v) in self.__class__.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        sir = "Prop instanta:\n"
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)

    def __str__(self):
        sir = self.nume.capitalize()
        sir += " " + str(self.activitate_curenta.nume) + " "
        sir += f"{self.timp_executat_activ}/{self.activitate_curenta.durata}"
        sir += f" (snt: {self.sanatate}, intel: {self.inteligenta}, obos: {self.oboseala}, dispoz: {self.buna_dispozitie})\n"
        return sir

class Activitate:

    def __init__(self, nume, factor_sanatate, factor_inteligenta, factor_oboseala, factor_dispozitie, durata):
        self.nume = nume
        self.factor_sanatate = factor_sanatate
        self.factor_inteligenta = factor_inteligenta
        self.factor_oboseala = factor_oboseala
        self.factor_dispozitie = factor_dispozitie
        self.durata = durata

    def __repr__(self):
        sir = "Prop clasa:\n"
        for (k, v) in self.__class__.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        sir = "Prop instanta:\n"
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir


# Functii ajutatoare pentru citirea elevilor

# Genereaza o lista de activitati, daca aleator = True activitatile se vor afla intr-o ordine random
def genereazaListaActivitati(l, aleator=False):
    activitati = []
    i = 0
    while i < len(l):
        # Adaug activitatea de numarul mentionat de ori consecutiv
        for j in range(int(l[i + 1])):
            activitati.append(l[i])
        i += 2
    if aleator == True:
        random.shuffle(activitati)
    return activitati


# Genereaza o lista de na activitati aleatoare
def genereazaListaAleatoareActivitati(na):
    act = list(Elev.d_activitati.keys())
    activitati = []
    for i in range(na):
        poz = random.randint(0, len(act) - 1)  # Genereaza o activitate random din lista
        activitati.append(act[poz])
    return activitati

def porneste_simulare(l_elevi):
    # Simularea la ora 9
    ora = 10
    print(f"Ora {ora}:00\n")

    for e in l_elevi:
        if len(e.lista_activitati) > 0:
            activ = Elev.d_activitati[e.lista_activitati[0]]
            e.incepe_activitate(activ)
            e.trece_ora(ora)
            print(e.__str__())
    while True:
        comanda = input("comanda = ").split()
        if len(comanda) == 2 and comanda[0] == "detaliat" and comanda[1].isnumeric():
            nr_ore = int(comanda[1])
            for i in range(nr_ore):
                if ora == 23:
                    ora = 0
                else:
                    ora += 1
                print(f"Ora {ora}:00\n")
                for e in l_elevi:
                    if len(e.lista_activitati) > 0:
                        activ = Elev.d_activitati[e.lista_activitati[0]]
                        e.incepe_activitate(activ)
                        e.trece_ora(ora)
                        print(e.__str__())

        elif comanda[0] == "gata":
            for e in l_elevi:
                print(e.__str__())
                e.afiseaza_raport()
                print("Simulare terminata fortat")
                return
        elif comanda[0] == "continua":
            if len(comanda) == 2:
                if comanda[1].isnumeric():
                    n = int(comanda[1])
                    # Starea elevilor dupa n ore

                    for i in range(n):
                        if ora == 23:
                            ora = 0
                        else:
                            ora += 1
                        for e in l_elevi:
                            if len(e.lista_activitati) > 0:
                                activ = Elev.d_activitati[e.lista_activitati[0]]
                                e.incepe_activitate(activ)
                                e.trece_ora(ora)
                    for e in l_elevi:
                        print(e.__str__())
                elif comanda[1] == "final_elev":
                    # Se continua pana cand iese un elev din simulare
                    iesire = False
                    while not iesire:
                        if ora == 23:
                            ora = 0
                        else:
                            ora += 1
                        print(f"Ora {ora}:00\n")
                        for e in l_elevi:
                            if len(e.lista_activitati) > 0:
                                activ = Elev.d_activitati[e.lista_activitati[0]]
                                e.incepe_activitate(activ)
                                e.trece_ora(ora)
                                print(e.__str__())
                            else:
                                if e.testeaza_final():
                                    final, motiv = e.testeaza_final()
                                    print(motiv)
                                    iesire = True
                    return

                else:
                    print("Comanda gresita")
            else:
                nr_elevi = len(l_elevi)
                nr_finale = 0
                while nr_finale != nr_elevi:
                    if ora == 23:
                        ora = 0
                    else:
                        ora += 1

                    for e in l_elevi:
                        if len(e.lista_activitati) > 0:
                            activ = Elev.d_activitati[e.lista_activitati[0]]
                            e.incepe_activitate(activ)
                            e.trece_ora(ora)

                    if e.testeaza_final():
                        nr_finale +=1

                for e in l_elevi:
                    final, motiv = e.testeaza_final()
                    print(motiv)
                    e.afiseaza_raport()
                return "natural"
        else:
            print("Comanda gresita")


if __name__ == "__main__":
    # Citirea activitatilor
    f = open("input_activitati.txt", "r")
    l_citire = f.readlines()[1:]
    l_activitati = []
    for linie in l_citire:
        a = linie.split()
        l_activitati.append(Activitate(a[0], float(a[1]), float(a[2]), float(a[3]), float(a[4]), int(a[5])))

    for a in l_activitati:
        Elev.d_activitati[a.nume] = a
        # print(repr(a))

    print(Elev.d_activitati.keys())

    # Citirea elevilor
    h = open("input_elevi.txt", "r")
    n = h.readline().split()
    n_elevi = int(n[0])
    na_implicit = int(n[1])

    # Din moment ce am mai putin de n_elevi, citesc pana mi se termina fisierul
    l_elevi = []
    for linie in h:
        l_elev = linie.strip().split(maxsplit=5)
        nume = l_elev[0]
        sanatate = int(l_elev[1])
        inteligenta = int(l_elev[2])
        oboseala = int(l_elev[3])
        dispozitie = int(l_elev[4])

        l_act_elev = []
        #print(l_elev)
        if l_elev[5][0:6] == 'random':
            # Cele 3 cazuri cu random
            if len(l_elev[5]) > 6 and l_elev[5][6] == '(':
                if l_elev[5][7].isdigit():
                    # Cazul in care trebuie alocate nr dat de activitati random
                    for j in range(7, len(l_elev[5])):
                        if l_elev[5][j] == ')':
                            break
                    number = int(l_elev[5][7:j])
                    lista_activitati = genereazaListaAleatoareActivitati(number)
                else:
                    # Cazul in care activitatile date trebuie alocate intr-o ordine random
                    lista_activitati = genereazaListaActivitati(l_elev[5][7:].rstrip(')').split(), True)
            else:
                # Cazul in care trebuie alocate na_implicit activitati random
                lista_activitati = genereazaListaAleatoareActivitati(na_implicit)
        else:
            # Cazul in care activitatile sunt mentionate in ordine
            lista_activitati = genereazaListaActivitati(l_elev[5].split())
        elev = Elev(nume, sanatate, inteligenta, oboseala, dispozitie, lista_activitati)
        l_elevi.append(elev)

    # Pentru elevii neprecizati in fisier se aloca na_implicit activitati aleatoare
    ne = len(l_elevi)
    for i in range(n_elevi - ne):
        lista_activitati = genereazaListaAleatoareActivitati(na_implicit)
        elev = Elev(lista_activitati)
        l_elevi.append(elev)

    if porneste_simulare(l_elevi) == "natural":
        if input("Salvati raportul? (da/nu)") == "da":
            os.mkdir("raport")
            for e in l_elevi:
                e.salveaza_raport("raport")

    f.close()
    h.close()

