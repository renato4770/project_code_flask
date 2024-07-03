from abc import ABC, abstractmethod

class CardPrototype(ABC):
    @abstractmethod
    def clone(self):
        pass

class Card(CardPrototype):
    def __init__(self, name, type, effect):
        self.name = name
        self.type = type
        self.effect = effect

    def clone(self):
        return Card(self.name, self.type, self.effect)