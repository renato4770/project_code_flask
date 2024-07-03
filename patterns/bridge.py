from abc import ABC, abstractmethod

class Effect(ABC):
    @abstractmethod
    def apply(self, player):
        pass

class DrawCardEffect(Effect):
    def apply(self, player):
        player.draw_card()

class DiscardCardEffect(Effect):
    def apply(self, player):
        player.discard_card()