import random
from data import herois

class Hero:
    def __init__(self, nome, guilda):
        # encontra o dicionário correspondente pelo nome
        dados = next((h for h in herois if h["Herói"] == nome), None)
        if not dados:
            raise ValueError(f"Herói '{nome}' não encontrado na base de dados.")

        self.nome = nome
        self.guilda = guilda
        self.defesa = dados["Def"]
        self.vida = dados["Vida"]
        self.total = dados["Total"]
        self.habilidade = dados["Habilidade"]
        self.efeito = dados["Efeito"]
        self.death_tokens = 0

    def __repr__(self):
        return (f"Hero -\n"
                f"Nome: {self.nome}\n"
                f"Guilda: {self.guilda}\n"
                f"DEF: {self.defesa}\n"
                f"VIDA: {self.vida}\n"
                f"TOKENS: {self.death_tokens}\n")



# heroes = []
# for h in herois:
#     hero = Hero(
#         nome=h["Herói"],
#         guilda="Guilda Azul",
#     )
#     heroes.append(hero)
#
# print(f"random choice from all heroes: {random.choice(heroes)}")
