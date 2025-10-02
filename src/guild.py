from data import guildas
import hero
import mapa

class Guild:
    def __init__(self, nome):
        self.nome = nome
        self.medalhas = []
        self.herois = []

    def __repr__(self):
        return (f"Guilda: {self.nome} \n"
                f"Heróis: {self.herois}\n"
                f"Medalhas: {len(self.medalhas)}")


# vermelha = Guild(guildas[0])
# seth = hero.Hero("Seth", vermelha.nome)
# johan = hero.Hero("Johan", vermelha.nome)
# vapor = hero.Hero("Vapor", vermelha.nome)
# medalha1 = "PVP"
# medalha2 = "PVE"
#
# vermelha.herois = [seth, johan, vapor]
# vermelha.medalhas =[medalha1, medalha1, medalha2]
# print(vermelha)
