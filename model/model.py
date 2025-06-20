import copy

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
        #puliamo il grafo
        self._grafo.clear()
        self._products = DAO.getProducts_colore(colore) #nazioni prese in base all'anno indicato
        # aggiungiamo i nodi(li ho nelle fermate)
        self._grafo.add_nodes_from(self._products)
        # aggiungo archi
        self.addEdges(anno)

    def addEdges(self,anno):
        for u in self._products:#prendo nodo1
            for v in self._products:#prendo nodo2
                if u != v:#se son diversi controllo con la query
                    idU= u.Product_number
                    idV= v.Product_number
                    edges= DAO.addEdges(idU,idV,self.idMapProducts,anno) #mi restituisce una lista di archi: [arco1,arco2,...]
                    #che collegano prodotti diversi venduti lo stesso giorno dallo stesso retailer
                    #se due retailer vendono lo stesso giorno lo stesso prodotto, vale come 1(fatto con la group by)
                    #se non ci sono archi passo oltre:
                    if not edges:
                        continue
                    #se ci sono:
                    #arco ha sempre stessi nodi u,v --> quindi è inutile iterare
                    if self._grafo.has_edge(edges[0].nodo1, edges[0].nodo2):#controllo se esiste già l'arco
                        continue
                    else:
                        self._grafo.add_edge(edges[0].nodo1, edges[0].nodo2, weight=len(edges))

    def getNumNodi(self):
        return len(self._grafo.nodes())

    def getNumArchi(self):
        return len(self._grafo.edges())

    def getMaggiori(self):
        archi= list(self._grafo.edges(data=True))
        #ordino in base al peso
        archi.sort(key=lambda x: x[2]["weight"],reverse=True)

        #archi lista di tuple ordinate in base al peso #[(u,v,{"weight":3,...}
        risultato=[archi[0],archi[1],archi[2]]
        return risultato

    def getDuplicati(self,archi):
        #archi = lista di tuple
        nodi=[] #lista di id
        risultato=set() #per non avere duplicati
        for i in archi:
            nodi.append(i[0].Product_number)
            nodi.append(i[1].Product_number)

        for j in nodi:
            if nodi.count(j)>1:
                risultato.add(j)
        return risultato


    ########################################################parte 2
    def getNodi(self):
        nodes= list(self._grafo.nodes())
        return nodes

    def handle_search(self, nodoSorgente):
        self.percorso_migliore = []  # Memorizza il percorso più lungo trovato
        self._ricorsione([nodoSorgente], nodoSorgente)
        # Restituisce il numero massimo di archi (nodi - 1)
        return len(self.percorso_migliore) - 1

    def _ricorsione(self, parziale, nodoSorgente):
        # Prendo i vicini del nodo corrente
        neighbors = list(self._grafo.neighbors(nodoSorgente))

        # Condizione terminale: nessun vicino o nessun vicino ammissibile
        listaAmmissibili = self.viciniAmmissibili(neighbors, parziale)
        if len(neighbors) == 0 or len(listaAmmissibili) == 0:
            # Controllo se il percorso corrente è il più lungo trovato finora
            if len(parziale) > len(self.percorso_migliore):
                self.percorso_migliore = copy.deepcopy(parziale)

            return

        # Caso ricorsivo: esploro i vicini ammissibili
        for n in listaAmmissibili:
            # Aggiungo il vicino al percorso parziale
            parziale.append(n)
            # Procedo ricorsivamente
            self._ricorsione(parziale, n)
            # Backtracking: rimuovo il nodo appena aggiunto
            parziale.pop()

    def viciniAmmissibili(self, neighbors, parziale):
        """Restituisce una lista di vicini ammissibili"""
        nodiAmmissibili = []
        for n in neighbors:
            if self.possoAggiungere(n, parziale):
                nodiAmmissibili.append(n)
        return nodiAmmissibili

    def possoAggiungere(self, nodo, parziale):
        """Verifica se è possibile aggiungere un nodo al percorso"""
        # Se il percorso ha meno di 2 nodi, posso aggiungere il nuovo nodo
        if len(parziale) < 2:
            return True

        # Ottengo il peso dell'ultimo arco aggiunto e del nuovo arco
        ultimo_peso = self._grafo[parziale[-2]][parziale[-1]]["weight"]
        nuovo_peso = self._grafo[parziale[-1]][nodo]["weight"]

        # Controllo se il nuovo arco rispetta il criterio del peso crescente
        if nuovo_peso >= ultimo_peso:
            # Controllo anche che l'arco non sia già presente nel percorso
            for i in range(len(parziale)-1): #se abbiamo già attraversato quella strada
                if (parziale[i], parziale[i + 1]) == (parziale[-1], nodo):
                    return False
            return True
        return False














