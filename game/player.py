class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.stable = []

    def draw_card(self, card):
        self.hand.append(card)

    def discard_card(self, card):
        self.hand.remove(card)