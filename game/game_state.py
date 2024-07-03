import random
from game.turn_manager import TurnManager
from game.effect_manager import EffectManager

class GameState:
    def __init__(self, players, deck, num_players):
        self.players = players
        self.deck = deck
        self.discard_pile = []
        self.turn_manager = TurnManager()
        self.effect_manager = EffectManager()
        self.current_player = None
        self.num_players = num_players

    def add_player(self, player):
        self.players.append(player)
        self.turn_manager.add_player(player)

    def start_game(self):
        if not self.deck:
            raise ValueError("The deck is empty. Cannot start the game.")
        
        random.shuffle(self.deck)
        for player in self.players:
            for _ in range(5):
                if self.deck:
                    player.draw_card(self.deck.pop())
                else:
                    print("Warning: Deck is empty. Not all players received 5 cards.")
                    break
        self.current_player = self.turn_manager.next_turn()

    def draw_card(self):
        if not self.deck:
            if self.discard_pile:
                print("Reshuffling discard pile into deck.")
                self.deck = self.discard_pile
                self.discard_pile = []
                random.shuffle(self.deck)
            else:
                raise ValueError("No cards left in the deck or discard pile.")
        
        card = self.deck.pop()
        self.current_player.draw_card(card)
        return card

    def play_card(self, card_index):
        card = self.current_player.hand.pop(card_index)
        self.current_player.stable.append(card)
        self.effect_manager.apply_effect(card.effect, self.current_player)
        return card

    def end_turn(self):
        self.current_player = self.turn_manager.next_turn()
        return self.current_player