import os
import sys
from flask import render_template

ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/../"
sys.path.insert(1, ROOT_DIRECTORY + "/static/entities/")
sys.path.insert(1, ROOT_DIRECTORY + "/static/database/connections/")

from Player import Player
from Game import Game
from User import User

from GameConnection import GameConnection
from PlayerConnection import PlayerConnection
from UserConnection import UserConnection

def get_all_players(game):

    return PlayerConnection().get_all_players(game)

def get_player_objects(game):

    all_player_dicts = get_all_players(game)

    players = [Player(id = player["id"], user = User(id = player["user_id"]), game = Game(id = player["game_id"])) for player in all_player_dicts]

    _ = [players[i].set_attributes(all_player_dicts[i]) for i in range(len(players))]

    return players

def get_all_games(joinable = False):
    return GameConnection().get_all_games(joinable = joinable)

def get_game_objects(joinable = False):
    all_games = get_all_games(joinable = joinable)

    display_games = [Game(id = game["id"], game_creator = User(id = game["user_id"]), available_slots = game["available_slots"]) for game in all_games]

    return display_games
