import bottle
import os
import random

import utils
from move import Move
from copy import deepcopy
from coord import UP, DOWN, LEFT, RIGHT
from game import Game


@bottle.route('/static/<path:path>')
def static(path):
    """Static files."""
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    """Start the game."""
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'sneksnek'
    }


def unsafe_moves(game):
    """Return banned moves to neighbour positions (walls and other snakes)."""
    banned_moves = []
    head = game.me.head()

    neighbours = [
        {'d': head.up(), 'm': Move(UP, 0)},
        {'d': head.down(), 'm': Move(DOWN, 0)},
        {'d': head.left(), 'm': Move(LEFT, 0)},
        {'d': head.right(), 'm': Move(RIGHT, 0)}
    ]

    # If neighbour move is unsafe, add to banned moves
    for n in neighbours:
        if game.is_unsafe(n['d']):
            banned_moves.append(n['m'])

    return banned_moves


def food(game):
    """Return good moves towards food goodness is width * height - distance_to_food."""
    if len(game.foods) <= 0:
        return []

    moves = []

    # Get a list of distances to all foods
    food_distances = map(lambda c: game.me.head().distance(c), game.foods)

    for idx, d in enumerate(food_distances):
        # Find possible moves towards the foods
        #   i.e. if food is to the top right, possible moves are up and right
        mt = game.me.moves_to(game.foods[idx])
        for m in mt:
            # Add possible move to possible moves with inverse distance as
            moves.append(Move(m, 1 / d))

    return moves


def remove_critical(moves, banned_moves):
    """Remove all critical moves from possible move."""
    return filter(lambda d: d not in banned_moves, moves)


def choose_best_move(moves):
    """Choose the best move based on goodness."""
    moves.sort()
    moves.reverse()
    if len(moves) <= 0:
        return None
    return moves[0]


@bottle.post('/move')
def move():
    """Make a move."""
    print('\n--- MAKING MOVE')

    data = bottle.request.json

    # Create game state
    game = Game(data)

    # Possible directions we can move
    directions = [
        Move(UP, 0.01),
        Move(DOWN, 0.01),
        Move(LEFT, 0.01),
        Move(RIGHT, 0.01)
    ]

    # Critcal positions
    not_safe = unsafe_moves(game)
    critcal = utils.flatten([not_safe])

    # Good positions
    food_moves = food(game)
    good = utils.flatten([food_moves, directions])

    print('\n--- critcal')
    for c in critcal:
        print(str(c))

    print('\n--- good')
    for c in good:
        print(str(c))

    # Remove critical moves from good moves
    available = remove_critical(good, critcal)

    # Choose best move based on goodness
    move = choose_best_move(available)

    print('\n--- available')
    for c in available:
        print(str(c))

    print('\n--- move')

    # We lost :(
    if move is None:
        move = random.choice(directions)
        print('No best move')
    else:
        print(move)

    return {
        'move': move.direction,
        'taunt': 'sneksnek'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))