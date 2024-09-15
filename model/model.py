import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap_retailers = {}
        self._bestPath = []
        self._bestScore = 0

    def get_all_nazioni(self):
        self._all_nazioni = DAO.get_all_nazioni()
        return self._all_nazioni

    def get_all_anni(self):
        self._all_anni = DAO.get_all_anni()
        return self._all_anni

    def build_grafo(self, nazione, anno):

        self._grafo.clear()

        self._nodi = DAO.get_retailers_nazione(nazione)
        for nodo in self._nodi:
            self._idMap_retailers[nodo.Retailer_code] = nodo

        self._grafo.add_nodes_from(self._nodi)

        self._archi = DAO.get_archi(nazione, anno, self._idMap_retailers)
        for arco in self._archi:
            self._grafo.add_edge(arco[0], arco[1], weight=arco[2])

    def get_dettagli_grafo(self):
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def volumi_retailers(self):

        lista_tuple = []
        self.retailers_connessi = []

        for r in self._nodi:
            lista_archi_incidenti = list(self._grafo.edges(r))
            #print("Lista archi incidenti", lista_archi_incidenti)
            somma = 0
            for arco in lista_archi_incidenti:
                somma += self._grafo[arco[0]][arco[1]]["weight"]
            lista_tuple.append((r, somma))
            if somma > 0:
                self.retailers_connessi.append(r)
        #print(lista_tuple)

        lista_tuple.sort(key=lambda x:x[1], reverse=True)
        return lista_tuple

    def get_cammino_ottimo(self, N):

        self._bestPath = []
        self._bestScore = 0

        for n in self.retailers_connessi:
            parziale = [n]
            self._ricorsione(parziale, N)

        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, N):

        if len(parziale) == N:
            if self._grafo.has_edge(parziale[-1], parziale[0]):
                parziale.append(parziale[0])
                if self.get_peso_cammino(parziale) > self._bestScore:
                    self._bestPath = copy.deepcopy(parziale)
                    self._bestScore = self.get_peso_cammino(parziale)
                parziale.pop()

            return

        vicini = self._grafo.neighbors(parziale[-1])
        vicini = [v for v in vicini if v not in parziale]
        for v in vicini:
            parziale.append(v)
            self._ricorsione(parziale, N)
            parziale.pop()


    def get_peso_cammino(self, lista_nodi):
        peso = 0

        for i in range(0, len(lista_nodi)-1):
            if self._grafo.has_edge(lista_nodi[i], lista_nodi[i+1]):
                peso += self._grafo[lista_nodi[i]][lista_nodi[i+1]]["weight"]

        return peso

    def get_peso_arco(self, u, v):
        return self._grafo[u][v]["weight"]

