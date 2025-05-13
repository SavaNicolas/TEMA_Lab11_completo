import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._productsAll = DAO.getAllProducts()  # lista con tutte le nazioni, per avere l'id map
        # creo grafo
        self._grafo = nx.Graph()
        # mappa di oggetti
        self.idMapProducts = {}
        for p in self._productsAll:
            self.idMapProducts[p.Product_number] = p

    def buildGraph(self,colore,anno):
        self._products = DAO.getProducts_colore(colore) #nazioni prese in base all'anno indicato
        # aggiungiamo i nodi(li ho nelle fermate)
        self._grafo.add_nodes_from(self._products)
        # aggiungo archi
        self.addEdges(colore,anno)

    def addEdges(self,colore,anno):
        allEdges=DAO.addEdges(self.idMapProducts,colore,anno) #lista di archi
        for edge in allEdges:
            if self._grafo.has_node(edge.nodo1) and self._grafo.has_node(edge.nodo2):
                self._grafo.add_edge(edge.nodo1, edge.nodo2, weight= edge.peso) #nodo 1 e nodo 2


    def getNumNodi(self):
        return len(self._grafo.nodes())

    def getNumArchi(self):
        return len(self._grafo.edges())
