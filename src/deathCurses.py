import random
from data import death_curses

# Importar as maldições
cards = death_curses

def deckPreparer():
    curse_deck = [card for card in cards for _ in range(card["Qtd"])]
    random.shuffle(curse_deck)
    print(len(curse_deck))
    return curse_deck

def curseApplier(death_tokens, curse_deck):
    if death_tokens <= 2:
        possible_deck = [card for card in curse_deck if card["Tier"] <= death_tokens]
    else:
        possible_deck = [card for card in curse_deck]
    picked_cards = [random.choice(possible_deck) for token in range(death_tokens)]
    print("possible deck: ", len(possible_deck), " cards")
    print("picked curses: ", len(picked_cards), " cards:", picked_cards, "\n")
    final_curse = max(picked_cards, key=lambda c: c["Valor"])
    print(f"Maldição final: \n"
          f"Valor: {final_curse["Valor"]}\n"
          f"Nome: {final_curse["Nome"]}\n"
          f"Efeito: { final_curse["Efeito"]}\n")

    return final_curse




