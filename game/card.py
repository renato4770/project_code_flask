from patterns.prototype import Card
from patterns.state import AnimalState

class GameCard(Card):
    def __init__(self, name, type, effect, state: AnimalState):
        super().__init__(name, type, effect)
        self.state = state

    def get_animal_type(self):
        return self.state.get_animal_type()