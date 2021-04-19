import argparse
import time

class Lacat:
    # clasa pentru un lacat -> nodul grafului din problema noastra
    def __init__(self, incuietori, ultima_cheie):
        self.incuietori = incuietori
        self.ultima_cheie = ultima_cheie

    def __eq__(self, other):
        return self.incuietori == other.incuietori

    def __str__(self):
        temp = ['inc(' + x[0] + ', ' + str(x[1]) + ')' for x in self.incuietori]
        return "[" + ", ".join(str(i) for i in temp) + "]"

    def aplica_cheie(self, cheie):
    # returneaza un lacat nou
        if len(cheie) != len(self.incuietori):
            print("Numar diferit de zone si incuietori")
            exit(1)

        new_incuietori = []
        for i in range(len(cheie)):
            stare = self.incuietori[i][0]
            nr_incuieri = self.incuietori[i][1]

            if cheie[i] == 'd':
                if self.incuietori[i][0] == 'i':
                    if self.incuietori[i][1] == 1:
                        stare = 'd'
                        nr_incuieri = 0
                    else:
                        nr_incuieri -= 1
            elif cheie[i] == 'i':
                stare = 'i'
                nr_incuieri += 1

            new_incuietori.append((stare, nr_incuieri))

        return Lacat(new_incuietori, cheie)

class NodParcurgere:
    # informatii despre un nod din arborele parcurgerii
    def __init__(self, info, parinte, cost, euristica):
        self.info = info
        self.parinte = parinte
        self.cost = cost
        self.euristica = euristica
        self.total = cost + euristica

    def obtine_drum(self):
        ans = []
        node = self

        while node is not None:
            ans.insert(0, node.info)
            node = node.parinte

        return ans

    def contine_in_drum(self, info_nod_nou):
        node = self

        while node is not None:
            if node.info == info_nod_nou:
                return True
            node = node.parinte

        return False


class Graf:
    # clasa graf pentru problema noastra
    def __init__(self, start, scop, lista_chei):
        self.start = start
        self.scop = scop
        self.lista_chei = lista_chei

    def genereaza_succesori(self, nod_curent):
        # aplicam cheile la nodul curent pentru a obtine noduri noi
        return [nod_curent.aplica_cheie(k) for k in self.lista_chei]

    def __calculeaza_euristica1(self, lacat):
        # euristica banala
        return 0

    def __calculeaza_euristica2(self, lacat):
        # admisibila
        # minimul de chei necesar pentru a descuia o incuietoare
        ans = lacat.incuietori[0][1]
        for inc in lacat.incuietori:
            if inc[1] < ans:
                ans = inc[1]
        return ans

    def __calculeaza_euristica3(self, lacat):
        # admisibila
        # maximul de chei necesar pentru a descuia o incuietoare
        ans = lacat.incuietori[0][1]
        for inc in lacat.incuietori:
            if inc[1] > ans:
                ans = inc[1]
        return ans

    def __calculeaza_euristica4(self, lacat):
        # inadmisibila
        # suma numarului de chei necesare pentru a descuia fiecare incuietoare in parte
        ans = 0
        for inc in lacat.incuietori:
            ans += inc[1]
        return ans

    def calculeaza_euristica(self, lacat, no_euristica):
        # functie care calculeaza o eutistica pentru un nod
        if no_euristica == 1:
            return self.__calculeaza_euristica1(lacat)
        elif no_euristica == 2:
            return self.__calculeaza_euristica2(lacat)
        elif no_euristica == 3:
            return self.__calculeaza_euristica3(lacat)
        else:
            return self.__calculeaza_euristica4(lacat)

class Alg:
    # clasa care rezolva problema
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('input_file')
        parser.add_argument('output_file')
        parser.add_argument('nr_solutii')
        parser.add_argument('timeout')
        parser.add_argument('tip_euristica')
        self.fin = open(parser.parse_args().input_file, "r")
        self.fout = open(parser.parse_args().output_file, "w")
        self.nsol = int(parser.parse_args().nr_solutii)
        self.timeout = float(parser.parse_args().timeout)
        self.no_nodes = 0
        self.tip_euristica = int(parser.parse_args().tip_euristica)

    def __del__(self):
        self.fin.close()
        self.fout.close()

    def read_data(self):
        # citim din fisierul dat ca parametru si instantiem clasa graf
        lista_chei = self.fin.read().strip().split()

        start = [('i', 1)] * len(lista_chei[0])
        scop = [('d', 0)] * len(lista_chei[0])

        self.gr = Graf(Lacat(start, []), Lacat(scop, []), lista_chei)

    def __get_time(self):
        # functie care intoarce durata de la inceperea algoritmului
        return time.time() - self.start_time


    def afiseaza_drum(self, drum, sol_crt):
        # afisam drumul in fisierul de output dat ca parametru
        self.fout.write("Solutia cu numarul " + str(sol_crt) + "\n")
        self.fout.write("Numarul de chei folosite este " + str(len(drum) - 1) + "\n")
        self.fout.write("Cautarea a durat " + str(self.__get_time()) + " secunde\n")
        self.fout.write("Am generat in total " + str(self.no_nodes) + " noduri\n\n")

        self.fout.write("Initial: " + str(drum[0]) + "\n\n")

        for idx in range(len(drum) - 1):
            self.fout.write(str(idx) + ")\t\tIncuietori: " + str(drum[idx]) + "\n")
            self.fout.write("\t\tAm folosit cheia: " + str(drum[idx + 1].ultima_cheie))
            self.fout.write("\n\t\tPentru a ajunge la: " + str(drum[idx + 1]) + "\n")

        self.fout.write("\n\nScop: " + str(drum[-1]) + "\n\n\n")

    def __timeout(self):
        # functie care imi spune daca am luat timeout
        now = time.time()
        return self.start_time + self.timeout < now

    def afiseaza_timeout(self, sol_crt):
        self.fout.write("Am luat timeout cautand solutia cu numarul " + str(sol_crt) +" :(\n")

    def __dead_state(self):
        # functie care verifica daca problema are solutii
        # daca pentru o incuietoare nu exista chei care sa o deschida, atunci problema nu are solutii
        for i in range(len(self.gr.start.incuietori)):
            for cheie in self.gr.lista_chei:
                if cheie[i] == 'd':
                    break
            else:
                return True
        return False

    def construieste_drum(self, curr_node, limita):
        if self.gr.scop == curr_node.info:
            return (True, 0)

        if curr_node.total > limita:
            return (False, curr_node.total)

        minn = float('inf')

        for lacat in self.gr.genereaza_succesori(curr_node.info):
            next_node = NodParcurgere(lacat, curr_node, curr_node.cost + 1, self.gr.calculeaza_euristica(lacat, self.tip_euristica))
            (ajuns, lim) = self.construieste_drum(next_node, limita)
            if ajuns:
                return (True, 0)
            minn = min(minn, lim)

        return (False, minn)

    def ida_star(self):
        nivel = self.gr.calculeaza_euristica(self.gr.start, self.tip_euristica)
        nod_start = NodParcurgere(self.gr.start, None, 0, self.gr.calculeaza_euristica(self.gr.start, self.tip_euristica))
        sol_crt = 0

        while True:
            (ajuns, lim) = self.construieste_drum(nod_start, nivel)
            if ajuns:
                self.afiseaza_drum(curr_node.obtine_drum(), sol_crt + 1)
                sol_crt += 1
                if self.nsol == sol_crt:
                    break
            if lim == float('inf'):
                # nu axista solutii
                break
            nivel = lim

if __name__ == '__main__':
    A = Alg()
    A.read_data()
    A.ida_star()
