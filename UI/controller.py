import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        all_nazioni = self._model.get_all_nazioni()
        for nazione in all_nazioni:
            self._listCountry.append(nazione)
            self._view.ddcountry.options.append(ft.dropdown.Option(nazione))

        all_anni = self._model.get_all_anni()
        for anno in all_anni:
            self._listYear.append(anno)
            self._view.ddyear.options.append(ft.dropdown.Option(anno))

        self._view.update_page()


    def handle_graph(self, e):
        self._view.txt_result.controls.clear()

        anno = self._view.ddyear.value

        if anno is None:
            self._view.create_alert("Per favore seleziona un anno")
            return

        nazione = self._view.ddcountry.value

        if nazione is None:
            self._view.create_alert("Per favore seleziona una nazione")
            return

        self._model.build_grafo(nazione, anno)

        num_nodi, num_archi = self._model.get_dettagli_grafo()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato!"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {num_nodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {num_archi}"))

        self._view.update_page()






    def handle_volume(self, e):
        self._view.txtOut2.controls.clear()
        tuple_r_v = self._model.volumi_retailers()
        #tuple_r_v.sort(key=lambda x:x[1], reverse=True)

        for tupla in tuple_r_v:
            retailer = tupla[0]
            volume = tupla[1]
            self._view.txtOut2.controls.append(ft.Text(f"{retailer} --> {volume}"))

        self._view.update_page()


    def handle_path(self, e):
        pass
