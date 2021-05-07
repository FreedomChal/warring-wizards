import os
import sys

ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/../../../"

# Include application directories in the path to allow imports
sys.path.insert(1, ROOT_DIRECTORY + "/static/database/connections/")
sys.path.insert(1, ROOT_DIRECTORY + "/static/entities/")

from PlayerConnection import PlayerConnection
from Player import Player
from Game import Game
from User import User

def get_player_objects(game):

    all_player_dicts = PlayerConnection().get_all_players(game)

    players = [Player(id = player["id"], user = User(id = player["user_id"]), game = Game(id = player["game_id"])) for player in all_player_dicts]

    _ = [players[i].set_attributes(all_player_dicts[i]) for i in range(len(players))]

    return players

def get_player_by_user_and_game(user, game):

    player_data = PlayerConnection().get_player_data_by_user_and_game(user = user, game = game)

    player = Player()
    player.set_attributes(player_data)
    player.user = user
    player.game = game

    return player

def get_player_by_id(id):
    player = Player(id = id)

    if player.get_attributes_by_id():
        return player
    else:
        return None
