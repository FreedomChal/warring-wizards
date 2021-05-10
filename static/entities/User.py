import os
import sys

ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/../../"

# Include application directories in the path to allow imports
sys.path.insert(1, ROOT_DIRECTORY + "/static/database/connections/")

from UserConnection import UserConnection

class User:

    def __init__(self, username = None, password = None, id = None, is_authenticated = False):

        self.connection = UserConnection(self)

        self.username = username
        self.password = password
        self.id = id

        # Properties required by Flask-Login
        self.is_authenticated = is_authenticated
        self.is_active = True
        self.is_anonymous = False

        self.is_administrator = None
        self.can_create_games = None

    def set_attributes(self, attributes):

        self.id = attributes.get("id", self.id)
        self.username = attributes.get("username", self.username)
        self.is_administrator = attributes.get("is_administrator", self.is_administrator)
        self.can_create_games = attributes.get("can_create_games", self.can_create_games)

    def get_attributes_by_id(self):

        attributes = self.connection.get_attributes_by_id()

        if attributes == None:
            return False
        else:
            self.set_attributes(attributes)
            return True

    def create(self):

        is_valid_new_user = self.connection.create_user()

        return is_valid_new_user

    def authenticate(self):

        self.is_authenticated = self.connection.verify_password()

        return self.is_authenticated

    def get_id(self):

        if self.id:
            return self.id

        self.id = self.connection.get_user_id()

        return self.id

    def get_username(self):

        if self.username:
            return self.username

        self.username = self.connection.get_user_username()

        return self.username

    def get_can_create_games(self):

        if not self.can_create_games == None:
            return self.can_create_games

        self.can_create_games = self.connection.get_can_create_games()

        return self.can_create_games
