import rfoo


class Annuaire(rfoo.BaseHandler):
    def __init__(self, handler, conn):
        self._handler = handler
        self._conn = conn
        self._buffer = ''
        self._counter = 0
        self._server = rfoo.Server(self._handler)
        self._methods = {}
        self.repertoire = {}

    def ajouterEntree(self, nom, number):
        self.repertoire[nom] = number

    def trouverNumero(self, nom):
        return self.repertoire.get(nom)

    def nbNumeros(self):
        return len(self.repertoire)

    def getAll(self):
        return self.repertoire

    def supprimerEntree(self, nom):
        del self.repertoire[nom]
        return 'entree supprimé avec succès'

    def supprimerTout(self):
        self.repertoire = {}
        return 'repertoire supprimé avec succès'


if __name__ == '__main__':
    port = 52525
    rfoo.InetServer(Annuaire).start(host='', port=port)  # "Start server - depratcated."""
