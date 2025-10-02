class Mapa:
    def __init__(self, nome):
        self.nome = nome
        self.guilda_vencedora = ""
        self.total_medalhas = ""


class Medalha:
    def __init__(self, tipo, mapa):
        self.tipo = tipo
        self.mapa = mapa
