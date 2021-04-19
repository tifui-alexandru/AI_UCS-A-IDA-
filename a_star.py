import argparse

class Lacat:
    # clasa pentru un lacat -> nodul grafului din problema noastra
    def __init__(self, incuietori):
        self.incuiecori = incuietori

    def __str__(self):
        return ['inc(' + x[0] + ', ' + str(x[1]) + ')' for x in self.incuiecori]

    def aplica_cheie(self, cheie):
    # returneaza un lacat nou
        if len(cheie) != len(self.incuiecori):
            print("Numar diferit de zone si incuietori")
            exit(1)

        new_incuietori = []
        for i in range(len(cheie)):
            stare = self.incuiecori[i][0]
            nr_incuieri = self.incuiecori[i][1]

            if cheie[i] == 'd':
                if self.incuiecori[i][0] == 'i':
                    if self.incuiecori[i][1] == 0:
                        stare = 'd'
                        nr_incuieri = 0
                    else:
                        nr_incuieri -= 1
            elif cheie[i] == 'i':
                stare = 'i'
                nr_incuieri += 1

            new_incuietori.append((stare, nr_incuieri))

        return Lacat(new_incuietori)

class NodParcurgere:
    # informatii despre un nod din arborele parcurgerii
    def __init__(self, info, parinte, cost, euristica):
        self.info = info
        self.parinte = parinte
        self.cost = cost
        self.euristica = euristica
        self.total = self.cost + self.euristica

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

    def calculeaza_euristica(self, node):
        # calculeaza euristica pentru un nod din graf
        return 0

class Alg:
    # clasa care rezolva problema
    def __init__():
        self.parser = argparse.ArgumentParser()
        parser.add_argument('input_file')
        parser.add_argument('output_file')
        parser.add_argument('nr_solutii')
        parser.add_argument('timeout')

    def read_data(self):
        # citim din fisierul dat ca parametru si instantiem clasa graf
        file_name = self.parser.parse_args().input_file

        fin = open(file_name, "r")
        lista_chei = fin.read().strip().split()
        fin.close()

        start = [('i', 1)] * len(lista_chei[0])
        scop = [('d', 0)] * len(lista_chei[0])

        self.gr = Graf(start, scop, lista_chei)


    def afiseaza_drum(self, drum):
        # afisam drumul in fisierul de output dat ca parametru
        file_name = self.parser.parse_args().output_file

        fout = open(file_name, "w")
        fout.write("Initial: " + drum[0] + "\n\n")

        for idx in len(drum):
            fout.write(str(idx) + ") \t\t incuietori: " + drum[idx] + "\n")

        fout.write("\nScop: " + drum[-1])

    def a_star(self):
        q = [NodParcurgere(self.gr.start, None, 0, self.gr.calculeaza_h(gr.start))]

        while len(q) > 0:
            curr_node = q.pop(0)

            if self.gr.scop == curr_node:
                afiseaza_drum(self, curr_node.obtine_drum())

            succesori = self.gr.genereaza_succesori(curr_node)
            for lacat in succesori:
                next_node = NodParcurgere(lacat, curr_node, curr_node.cost + 1, self.gr.calculeaza_h(lacat))

                for pos in range(len(q)):
                    if q[pos].total >= next_node.total:
                        q.insert(pos, next_node)
                        break
                else:
                    q.append(next_node)

if __name__ == '__main__':
    A = Alg()
    A.read_data()
    A.a_star()
