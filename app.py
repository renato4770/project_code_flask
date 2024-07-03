from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from game.game_state import GameState
from game.player import Player
from patterns.builder import DeckBuilder
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

games = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<game_id>/<player_name>')
def game_room(game_id, player_name):
    session['game_id'] = game_id
    session['player_name'] = player_name
    return render_template('game.html', game_id=game_id, player_name=player_name)

@socketio.on('create_game')
def handle_create_game(data):
    num_players = data['num_players']
    player_name = data['player_name']
    game_id = str(uuid.uuid4())[:8]
    deck = DeckBuilder().build()
    games[game_id] = GameState([], deck, int(num_players))
    join_room(game_id)
    player = Player(player_name)
    games[game_id].add_player(player)
    emit('game_created', {'game_id': game_id, 'player_name': player_name})

@socketio.on('join_game')
def handle_join_game(data):
    game_id = data['game_id']
    player_name = data['player_name']
    if game_id in games:
        game = games[game_id]
        if len(game.players) < game.num_players:
            join_room(game_id)
            player = Player(player_name)
            game.add_player(player)
            emit('player_joined', {'message': f'{player_name} joined the game'}, room=game_id)
            if len(game.players) == game.num_players:
                try:
                    game.start_game()
                    emit('game_started', {'message': 'Game has started', 'current_player': game.current_player.name}, room=game_id)
                except ValueError as e:
                    emit('error', {'message': str(e)}, room=game_id)
            update_game_state(game_id)
        else:
            emit('error', {'message': 'Game is full'})
    else:
        emit('error', {'message': 'Game does not exist'})

@socketio.on('draw_card')
def handle_draw_card(data):
    game_id = data['game_id']
    player_name = data['player_name']
    game = games[game_id]
    if game.current_player and game.current_player.name == player_name:
        card = game.draw_card()
        emit('card_drawn', {'message': f'{player_name} drew a card: {card.name}'}, room=game_id)
        update_game_state(game_id)
    else:
        emit('error', {'message': 'Not your turn or game not started'})

@socketio.on('play_card')
def handle_play_card(data):
    game_id = data['game_id']
    player_name = data['player_name']
    card_index = data['card_index']
    game = games[game_id]
    if game.current_player and game.current_player.name == player_name:
        card = game.play_card(int(card_index))
        emit('card_played', {'message': f'{player_name} played {card.name}'}, room=game_id)
        update_game_state(game_id)
    else:
        emit('error', {'message': 'Not your turn or game not started'})

@socketio.on('end_turn')
def handle_end_turn(data):
    game_id = data['game_id']
    player_name = data['player_name']
    game = games[game_id]
    if game.current_player and game.current_player.name == player_name:
        next_player = game.end_turn()
        emit('turn_ended', {'message': f'{player_name} ended their turn. It\'s now {next_player.name}\'s turn'}, room=game_id)
        update_game_state(game_id)
    else:
        emit('error', {'message': 'Not your turn or game not started'})

def update_game_state(game_id):
    game = games[game_id]
    game_state = {
        'current_player': game.current_player.name if game.current_player else None,
        'players': [{'name': p.name, 'hand': [c.name for c in p.hand], 'stable': [c.name for c in p.stable]} for p in game.players],
        'deck_size': len(game.deck)
    }
    emit('game_state_update', game_state, room=game_id)

if __name__ == '__main__':
    socketio.run(app, debug=True)