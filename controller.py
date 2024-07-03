import flet as ft

from UI.view import View
from database.meteo_dao import MeteoDao
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        val = self._view.dd_mese.value

        self._view.lst_result.controls.clear()

        if val is None:
            self._view.create_alert("Inserire un mese")
            return

        self._view.lst_result.controls.append(ft.Text("L'umidità media nel mese selezionato è:"))
        risultati = self._model.media(val)

        for r in risultati:
            self._view.lst_result.controls.append(ft.Text(r[0] + ": " + str(r[1])))

        self._view.update_page()




    def handle_sequenza(self, e):
        val = self._view.dd_mese.value

        self._view.lst_result.controls.clear()

        if val is None:
            self._view.create_alert("Inserire un mese")
            return

        sequ_iniziale = MeteoDao.get_ricorsione(val)
        self._model.solve_ricorsione(sequ_iniziale)

        sequenza = self._model.sequenza
        costo = self._model.costo_ottimo

        self._view.lst_result.controls.append(ft.Text(f"La sequenza selezionata ha un costo di {costo}"))

        for s in sequenza:
            self._view.lst_result.controls.append(ft.Text(f"({s.localita}, {s.data}) Umidità = {s.umidita}"))

        self._view.update_page()



    def read_mese(self, e):
        self._mese = int(e.control.value)

