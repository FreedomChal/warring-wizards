import os
import sys
from datetime import datetime, timezone

ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/../../"

# Include application directories in the path to allow imports
sys.path.insert(1, ROOT_DIRECTORY + "/static/database/connections/")

from GameConnection import GameConnection
from PlayerConnection import PlayerConnection
from User import User
import Player # Used instead of from Player import Player to prevent cyclic imports

DEFAULT_GAME_WAIT_TIME = 300 # The default length of time players have to join the game, measured in seconds.

MIN_GAME_WAIT_TIME = 60 # The minimum length of time players have to join the game, measured in seconds.
MAX_GAME_WAIT_TIME = 1500 # The maximum length of time players have to join the game, measured in seconds.

class Game:

    def __init__(self, id = None, game_creator = None, available_slots = 0, timestamp = None, wait_time = DEFAULT_GAME_WAIT_TIME):

        self.connection = GameConnection(self)

        self.game_creator = game_creator
        self.id = id
        self.can_join = available_slots > 0
        self.available_slots = available_slots
        self.timestamp = timestamp
        self.wait_time = self.format_wait_time(wait_time)

        self.is_archived = None

    def format_wait_time(self, wait_time):
        if wait_time < MIN_GAME_WAIT_TIME:
            return MIN_GAME_WAIT_TIME
        elif wait_time > MAX_GAME_WAIT_TIME:
            return MAX_GAME_WAIT_TIME
        else:
            return wait_time

    def close_joining(self):
        self.can_join = False
        self.connection.set_unjoinable()

    def create(self):

        is_valid_new_game = self.connection.create_game()

        return is_valid_new_game

    def delete(self):

        self.connection.delete_game_and_players()

    def get_attributes(self):

        attributes_dict = self.connection.get_attributes()

        self.set_attributes(attributes_dict)

    def set_attributes(self, attributes_dict):
        self.id = attributes_dict.get("id", self.id)
        self.timestamp = attributes_dict.get("timestamp", self.timestamp)
        self.can_join = attributes_dict.get("can_join", self.can_join)
        self.available_slots = attributes_dict.get("available_slots", self.available_slots)
        self.is_archived = attributes_dict.get("is_archived", self.is_archived)
        self.wait_time = attributes_dict.get("wait_time", self.wait_time)

    def get_id(self):

        if not self.id == None:
            return self.id

        self.id = self.connection.get_game_id()

        return self.id

    def get_creator_id(self):
        return self.game_creator.get_id()

    def get_timestamp(self):

        timestamp = self.connection.get_timestamp()
        self.timestamp = timestamp

        return timestamp

    def get_has_started(self):

        if self.connection.get_is_joinable() == False:
            return True

        current_timestamp = datetime.now(timezone.utc)

        self_timestamp = self.get_timestamp()

        print(self_timestamp, current_timestamp)

        difference = current_timestamp - self_timestamp

        difference_seconds = difference.seconds

        if difference_seconds >= self.wait_time:
            self.close_joining()

            return True
        else:
            return False

    def get_available_game_slots(self):

        self.available_slots = self.connection.get_available_game_slots()

        return self.available_slots

    def take_game_slot(self):
        self.connection.take_game_slot()

        self.get_available_game_slots()

    def attempt_to_join(self, user):

        if self.get_available_game_slots() > 0 and self.get_has_started() == False:

            new_player = Player.Player(game = self, user = user)

            if new_player.create():
                self.take_game_slot()

            return True

        return False

    def check_is_done(self):

        living_players = PlayerConnection().get_living_players(self)

        if len(living_players) == 1:
            self.set_done()
            winner = Player.Player(id = living_players[0]["id"])
            winner.get_stats()
            winner.set_archived()
            winner.write()

    def set_done(self):
        self.connection.set_archived()
