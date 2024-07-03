import copy

from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        self.sequenza = []
        self.costo_ottimo = 10000000000000

    def solve_ricorsione(self, situazioni_rimanenti):
        self.sequenza = []
        self.costo_ottimo = 10000000000000
        self.ricorsione([], situazioni_rimanenti)
        return self.sequenza

    def ricorsione(self, parziale, situazioni_rimanenti):

        if len(parziale) == 15:
            costo = self.calcola_costo(parziale)
            if costo <= self.costo_ottimo:
                self.sequenza = copy.deepcopy(parziale)
                self.costo_ottimo = costo

        else:
            giorni_dopo = self.situazioni_giorno_dopo(parziale, situazioni_rimanenti)
            for giorno in giorni_dopo:
                parziale.append(giorno)

                if self.ammissibile(parziale):
                    self.ricorsione(parziale, situazioni_rimanenti)
                parziale.pop()

    def situazioni_giorno_dopo(self, parziale, situazioni_rimanenti):
        domani = len(parziale) + 1
        situazioni_domani = []
        for s in situazioni_rimanenti:   # situazioni[(day-1)*3:day*3] --> equivale al ciclo (è comunque da aggungere l'if)
            if s.data.day == domani:
                situazioni_domani.append(s)
        return situazioni_domani

    def calcola_costo(self, parziale):
        costo = 0
        for s in parziale:
            costo += s.umidita

        cambiamenti = 0
        for i in range(len(parziale) - 1):
            if parziale[i].localita != parziale[i + 1].localita:
                cambiamenti += 1

        costo_cambiamenti = 100 * cambiamenti
        costo += costo_cambiamenti
        return costo


    @staticmethod
    def ammissibile(parziale):
        volte = 1
        ultima = parziale[-1]

        if len(parziale) == 1:
            return True

        # controllo che non sia stato già 6 giorni nella città selezionata
        for sit in parziale[:len(parziale) - 1]:
            if sit.localita == ultima.localita:
                volte += 1

        if volte > 6:
            return False

        # controllo che non mi sposti dalla città selezionata prima che siano passati almeno 3 giorni
        nuovo_nome = ""

        for i in range(len(parziale)):
            if nuovo_nome == parziale[i].localita:
                volte += 1
            else:
                volte = 1
                nuovo_nome = parziale[i].localita

        if volte >= 3:
            return True

        else:
            if parziale[len(parziale)-2].localita == ultima.localita:
                return True
            elif parziale[len(parziale)-2].localita == parziale[len(parziale)-3].localita == parziale[len(parziale)-4].localita and volte == 1:
                return True
            else:
                return False


        # altro modo per gestire il vincolo 2:

        # 1. se parziale ha meno di 3 elementi, questi dveono essere necessariamente tutti uguali

        # if len(parziale) <= 2 and len(parziale) > 0:
        #       if ultima.localita != parziale[0].localita:
        #           return False

        # 2. se ci sono più di 3 situazioni in parziale, bisogna controllare se ci si può spostare o meno:
        #    lo si può fare se guardando le ultime tre situazioni di parziale, queste sono tutte uguali,
        #    altrimenti, se ce n'è almeno una diversa, l'ultima e la penultima devono essere uguali

        # elif len(parziale) > 2:
        #       sequenza_finale = parziale[-3:]
        #       prima_fermata = sequenza_finale[0].localita
        #       counter = 0
        #       for fermata in sequenza_finale:
        #           counter += 1
        #       if counter < 3 and ultima.localita != sequenza_finale[-1].localita:
        #           return False

        # 3. tutti i vincoli sono soddisfatti (anche il caso inziale con lunghezza = 0)
        # return True


    def media(self, val):
        risultati = MeteoDao.get_media(val)
        return risultati


