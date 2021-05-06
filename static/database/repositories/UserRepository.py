import os
import sys

ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/../../../"

# Include application directories in the path to allow imports
sys.path.insert(1, ROOT_DIRECTORY + "/static/database/connections/")
sys.path.insert(1, ROOT_DIRECTORY + "/static/entities/")

from UserConnection import UserConnection
from User import User

def get_user_by_id(id, is_authenticated = False):
    user = User(id = id, is_authenticated = is_authenticated)

    if user.get_attributes_by_id():
        return user
    else:
        return None
