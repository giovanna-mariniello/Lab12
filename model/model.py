import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._listSales = None
        self._listRetailers = None

        self._grafo = nx.Graph()
        self._nodes = []
        self._edges = []
        self.solBest = 0

        self.path = []
        self.path_edge = []

        self.loadSales()
        self.loadRetailers()

    def loadSales(self):
        self._listSales = DAO.getAllSales()

    @property
    def listSales(self):
        return self._listSales

    def loadRetailers(self):
        self._listRetailers = DAO.getAllRetailers()

    @property
    def listRetailers(self):
        return self._listRetailers

    def buildGraph(self, c, a):
        self._grafo.clear()
        self._nodes = []
        self._edges = []
        print('Building graph')

        #nodes = retrailers in country c
        for r in self._listRetailers:
            if r.Country == c:
                self._nodes.append(r)
        self._grafo.add_nodes_from(self._nodes)
        print("Number of nodes: ", len(self._nodes))

        self.idMap = {}
        for n in self._nodes:
            self.idMap[n.Retailer_code] = n

        self._edges = DAO.getSameProduct(c, a, self.idMap)
        print("Number of edges: ", len(self._edges))
        self._grafo.add_weighted_edges_from(self._edges)

    def computeVolume(self):
        self._volume_ret = []
        self._ret_connected = []

        for n in self._grafo.nodes():
            volume=0
            for edge in self._grafo.edges(n, data=True):
                volume += edge[2]['weight']
            if volume > 0:
                self._ret_connected.append((n))
                self._volume_ret.append((n.Retailer_name, volume))
        self.volume_ret_sort=sorted(self._volume_ret, key=lambda x: x[1], reverse=True)
    def computePath(self, N):
        self.path = []
        self.path_edge = []
        self.solBest = 0

        for r in self._ret_connected:
            partial = []
            partial.append(r)
            self.ricorsione(partial, N, [])

    def ricorsione(self, partial, N, partial_edge):
        r_last = partial[-1]
        r_first = partial[0]

        #terminazione
        if len(partial_edge) == (N-1):
            if self._grafo.has_edge(r_last, r_first):
                partial_edge.append((r_last, r_first, self._grafo.get_edge_data(r_last, r_first)['weight']))
                partial.append(r_first)
                weight_path = self.computeWeightPath(partial_edge)
                if weight_path > self.solBest:
                    self.solBest = weight_path + 0.0
                    self.path = partial[:]
                    self.path_edge = partial_edge[:]
                partial.pop()
                partial_edge.pop()
            return

        neighbors = list(self._grafo.neighbors(r_last))
        neighbors = [i for i in neighbors if i not in partial]
        for n in neighbors:
            partial_edge.append((r_last, n, self._grafo.get_edge_data(r_last, n)['weight']))
            partial.append(n)

            self.ricorsione(partial, N, partial_edge)
            partial.pop()
            partial_edge.pop()


    def computeWeightPath(self, mylist):
        weight = 0
        for e in mylist:
            weight += e[2]
        return weight
    def get_nodes(self):
        return self._grafo.nodes()
    def get_edges(self):
        return list(self._grafo.edges(data=True))
    def get_volume_ret(self):
        return list(self._volume_ret)
    def get_num_of_nodes(self):
        return self._grafo.number_of_nodes()
    def get_num_of_edges(self):
        return self._grafo.number_of_edges()