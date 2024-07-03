from patterns.mediator import TurnMediator
from patterns.observer import TurnObserver

class TurnManager:
    def __init__(self):
        self.mediator = TurnMediator()
        self.observers = []

    def add_player(self, player):
        self.mediator.add_player(player)

    def add_observer(self, observer):
        self.observers.append(observer)

    def next_turn(self):
        player = self.mediator.next_turn()
        for observer in self.observers:
            observer.update(player)
        return player

    def get_current_player(self):
        return self.mediator.players[self.mediator.current_player_index]