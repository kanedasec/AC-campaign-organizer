import data
from guild import Guild
from hero import Hero
from mapa import Mapa,Medalha
from deathCurses import deckPreparer,curseApplier
from data import herois,death_curses,guildas

while True:
    mapa = Mapa(input("Qual mapa é esse?\n"))

    guilds = []
    for n in range(1):
        while True:
            guild_input = input("Qual é a sua guilda? [Vermelha, Azul, Laranja, Verde]\n")
            guild_input = guild_input.strip().capitalize()  # normalize case maybe

            if guild_input in data.guildas:
                g = Guild(guild_input)
                guilds.append(g)
                break  # exit the while loop, go to next n in the for-loop
            else:
                print(f"'{guild_input}' não é uma opção válida. Tente novamente.")

        for heroi in range(3):
            while True:
                hero_input = input("Qual é o seu primeiro Heroi?\n")
                hero_input = hero_input.strip().capitalize()
                hero_exist = next((h for h in herois if h["Herói"] == hero_input), None)
                if hero_exist:
                    h = Hero(hero_input, guild_input)
                    g.herois.append(h)
                    break
                else:
                    print(f"'{hero_input}' não é uma opção válida. Tente novamente.")

    for guild in guilds:
        quantas_medalha = int(input(f"A Guilda {guild.nome} ganhou quantas medalha?\n"))
        if quantas_medalha > 0:
            for n in range(quantas_medalha):
                guild.medalhas.append(Medalha(input(f"Medalha {n+1}: Qual tipo? [PVE/PVP]\n"), mapa))

    active_heroes = [hero for guild in guilds for hero in guild.herois]
    for hero in active_heroes:
        hero.death_tokens = int(input(f"Quantos death tokens o heroi: {hero.nome} tem?\n"))

    sorted_heroes = sorted(active_heroes, key=lambda h: h.death_tokens, reverse=True)

    for hero in sorted_heroes:
        print(hero, sorted_heroes.index(hero))
        if sorted_heroes.index(hero) == 0:
            curse_deck = deckPreparer()
            hero_curse = curseApplier(hero.death_tokens, curse_deck)
        else:
            curse_deck.remove(hero_curse)
            hero_curse = curseApplier(hero.death_tokens, curse_deck)