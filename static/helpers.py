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

# No helper functions are currently used. However, this file is fully functional, and imported by app.py.
