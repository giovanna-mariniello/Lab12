import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap_retailers = {}

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

        for r in self._nodi:
            lista_archi_incidenti = list(self._grafo.edges(r))
            #print("Lista archi incidenti", lista_archi_incidenti)
            somma = 0
            for arco in lista_archi_incidenti:
                somma += self._grafo[arco[0]][arco[1]]["weight"]
            lista_tuple.append((r, somma))
        #print(lista_tuple)

        lista_tuple.sort(key=lambda x:x[1], reverse=True)
        return lista_tuple