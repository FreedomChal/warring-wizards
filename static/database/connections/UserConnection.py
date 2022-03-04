import sys
import os
import bcrypt
import psycopg2
from Connection import Connection, convert_to_dict

# Note: This constant MUST be changed if the players table is modified.
COLUMNS = ("id", "username", "password_hash", "is_administrator", "can_create_games")

def convert_to_dict_user(column_values):

    user_dict = convert_to_dict(column_values, COLUMNS)

    return user_dict

class UserConnection:

    def __init__(self, user = None):
        self.connection = Connection
        self.user = user

    def create_user(self):

        if self.is_duplicate_user(self.user.username):
            return False

        password_hash = self.hash_password(self.user.password)

        with self.connection() as cursor:
            cursor.execute('''INSERT INTO users (username, password_hash) VALUES(%s, %s);''', (self.user.username, password_hash))

        return True

    def is_duplicate_user(self, username):

        with self.connection() as cursor:
            cursor.execute('''SELECT COUNT(*) FROM users WHERE username=%s;''', (username, ))

            row = cursor.fetchone()

            if row[0] != 0:
              return True
            else:
              return False

    def get_attributes_by_id(self):

        with self.connection() as cursor:
            cursor.execute('''SELECT * FROM users WHERE id=%s;''', (self.user.get_id(), ))

            row = cursor.fetchone()

            if not row:
                return None
            else:
                return convert_to_dict_user(row)

    def hash_password(self, password):

        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        return (password_hash.decode('utf-8'))

    def verify_password(self):
        with self.connection() as cursor:
            cursor.execute('''SELECT * FROM users WHERE username=%s;''', (self.user.username, ))

            rows = cursor.fetchall()

            if len(rows) != 1:
                return False

            user_info_dict = convert_to_dict_user(rows[0])

            correct_password_hash = user_info_dict["password_hash"]

            if (bcrypt.checkpw(self.user.password.encode('utf-8'), correct_password_hash.encode('utf-8'))):

                self.user.set_attributes(user_info_dict)

                return True
            else:
                return False

    def get_user_id(self):
        with self.connection() as cursor:
            cursor.execute('''SELECT id FROM users WHERE username=%s;''', (self.user.username, ))

            row = cursor.fetchone()

            return row[0]

    def get_user_username(self):
        with self.connection() as cursor:
            cursor.execute('''SELECT username FROM users WHERE id=%s;''', (self.user.id, ))

            row = cursor.fetchone()

            return row[0]

    def get_can_create_games(self):
        with self.connection() as cursor:
            cursor.execute('''SELECT can_create_games FROM users WHERE id=%s;''', (self.user.id, ))

            row = cursor.fetchone()

            return row[0]

    def get_is_administrator(self):
        with self.connection() as cursor:
            cursor.execute('''SELECT is_administrator FROM users WHERE id=%s;''', (self.user.id, ))

            row = cursor.fetchone()

            return row[0]
