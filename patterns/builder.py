from game.card import GameCard
from patterns.state import UnicornState, PandaState
from patterns.bridge import DrawCardEffect, DiscardCardEffect

class DeckBuilder:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def build(self):
        # Asegurarse de que haya suficientes cartas en el mazo
        while len(self.cards) < 20:  # Ajusta este número según sea necesario
            self.add_card(GameCard("Baby Unicorn", "Unicorn", DrawCardEffect(), UnicornState()))
            self.add_card(GameCard("Magical Panda", "Panda", DiscardCardEffect(), PandaState()))
        return self.cards