import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

    def fillDD(self):
        colors= DAO.getAllColors()
        for color in colors:
            self._view._ddcolor.options.append(ft.dropdown.Option(text=color))


    def handle_graph(self, e):
        self._view.txtOut.controls.clear()
        # prendo anno dall'input
        anno = self._view._ddyear.value
        # controlli
        if anno is None:
            self._view.txtOut.controls.clear()
            self._view.txtOut.controls.append(ft.Text("seleziona un valore"))
            self._view.update_page()
            return

        # converto in intero
        try:
            anno = int(anno)
        except ValueError:
            self._view.txtOut.controls.clear()
            self._view.txtOut.controls.append(ft.Text("data non valida"))
            self._view.update_page()
            return

        #prendo colore
        colore = self._view._ddcolor.value
        # controlli
        if colore is None:
            self._view.txtOut.controls.clear()
            self._view.txtOut.controls.append(ft.Text("seleziona un colore"))
            self._view.update_page()
            return

        # creo grafo
        self._model.buildGraph(colore,anno)

        # posso abilitare bottoni
        self._view._ddnode .disabled = False
        self._view.btn_search.disabled = False

        # stampo txt result
        self._view.txtOut.controls.append(ft.Text("grafo correttamente creato"))
        self._view.txtOut.controls.append(
            ft.Text(f"il grafo ha {self._model.getNumNodi()} nodi e {self._model.getNumArchi()} archi"))
        self._view.update_page()

        #stampo txt result 2
        archi=self._model.getMaggiori()
        duplicati = self._model.getDuplicati(archi)
        for i in archi:
            self._view.txtOut.controls.append(ft.Text(f"arco da {i[0].Product_number} a {i[1].Product_number} ha peso= {i[2]["weight"]}"))

        self._view.txtOut.controls.append(ft.Text(f"prodotti duplicati:"))
        self._view.update_page()

        if duplicati!=[]:
            for i in duplicati:
                self._view.txtOut.controls.append(ft.Text(f"-{i}"))
                self._view.update_page()
        else:
            self._view.txtOut.controls.append(ft.Text(f"non ci sono duplicati"))


        self._view.update_page()

    def fillDDProduct(self):
        pass


    def handle_search(self, e):
        pass
