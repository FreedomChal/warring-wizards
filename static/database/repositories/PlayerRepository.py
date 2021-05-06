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
