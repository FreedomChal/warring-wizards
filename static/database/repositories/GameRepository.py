import os
import sys

ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/../../../"

# Include application directories in the path to allow imports
sys.path.insert(1, ROOT_DIRECTORY + "/static/database/connections/")
sys.path.insert(1, ROOT_DIRECTORY + "/static/entities/")

from GameConnection import GameConnection
from Game import Game
from User import User

def get_previous_games(user):
    return GameConnection().get_previous_games(user.get_id())

def get_game_objects(joinable = False):
    all_games = GameConnection().get_all_games(joinable = joinable)

    display_games = [Game(id = game["id"], game_creator = User(id = game["user_id"]), available_slots = game["available_slots"]) for game in all_games]

    return display_games

def get_game_by_host(host):

    hosted_game_attributes = GameConnection().get_game_by_host(host)

    if not hosted_game_attributes:
        return None
    else:
        hosted_game = Game()
        hosted_game.set_attributes(hosted_game_attributes)

        return hosted_game
