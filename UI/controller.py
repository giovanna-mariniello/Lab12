import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        for n in self._model.listSales:
            if n.Date.year not in self._listYear:
                self._listYear.append(n.Date.year)

        for n in self._model.listRetailers:
            if n.Country not in self._listCountry:
                self._listCountry.append(n.Country)

        for a in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(a))

        for c in self._listCountry:
            self._view.ddcountry.options.append(ft.dropdown.Option(c))

        self._view.update_page()

    def handle_graph(self, e):
        a = self._view.ddyear.value
        c = self._view.ddcountry.value

        if a is None:
            self._view.create_alert("Inserire l'anno")
            return

        if c is None:
            self._view.create_alert("Inserire la nazione")
            return

        self._model.buildGraph(c, a)

        self._view.txt_result.controls.append(ft.Text(
            f"Numero di vertici: {self._model.get_num_of_nodes()} Numero di archi: {self._model.get_num_of_edges()}"))

        self._view.update_page()


    def handle_volume(self, e):
        self._model.computeVolume()

        for ii in self._model.volume_ret_sort:
            self._view.txtOut2.controls.append(ft.Text(
                f"{ii[0]} --> {ii[1]}"))

        self._view.update_page()

    def handle_path(self, e):
        N = int(self._view.txtN.value)
        if N < 2:
            self._view.create_alert("Lunghezza percorso non valida (minore di 2)!")
            return
        self._model.computePath(N)

        self._view.txtOut3.controls.append(ft.Text(
            f"Peso cammino massimo: {str(self._model.solBest)}"))

        for ii in self._model.path_edge:
            self._view.txtOut3.controls.append(ft.Text(
                f"{ii[0].Retailer_name} --> {ii[1].Retailer_name}: {str(ii[2])}"))

        self._view.update_page()