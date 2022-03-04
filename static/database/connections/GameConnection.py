import sys
import os
import psycopg2
from datetime import datetime
from Connection import Connection, convert_to_dict

# Note: This constant MUST be changed if the games table is modified.
COLUMNS = ("id", "timestamp", "user_id", "can_join", "available_slots", "is_archived", "wait_time")

def convert_to_dict_game(column_values):

    game_dict = convert_to_dict(column_values, COLUMNS)

    return game_dict

class GameConnection:

    def __init__(self, game = None):
        self.connection = Connection
        self.game = game

    def create_game(self):

        if self.is_duplicate_game():
            return False

        user_id = self.game.game_creator.get_id()

        current_timestamp = datetime.now().isoformat(sep = ' ', timespec = 'seconds')

        with self.connection() as cursor:
            cursor.execute('''INSERT INTO games (user_id, can_join, available_slots, timestamp, wait_time) VALUES(%s, %s, %s, %s, %s);''', (self.game.game_creator.id, 1, self.game.available_slots, current_timestamp, self.game.wait_time))

        return True

    def delete_game_and_players(self):
        with self.connection() as cursor:
            cursor.execute('''DELETE FROM players WHERE game_id=%s;''', (self.game.get_id(), ))
            cursor.execute('''DELETE FROM games WHERE id=%s;''', (self.game.get_id(), ))

        return True

    def is_duplicate_game(self):

        with self.connection() as cursor:
            user_id = self.game.game_creator.get_id()

            cursor.execute('''SELECT COUNT(*) FROM games WHERE user_id=%s AND is_archived=0;''', (user_id, ))

            row = cursor.fetchone()

            if row[0] != 0:
              return True
            else:
              return False

    def get_attributes(self):

        if self.game.id:
            with self.connection() as cursor:
                cursor.execute('''SELECT * FROM games WHERE id=%s;''', (self.game.get_id(), ))

                row = cursor.fetchone()

                return row[0]
        else:
            with self.connection() as cursor:
                cursor.execute('''SELECT * FROM games WHERE user_id=%s;''', (self.game.get_creator_id(), ))

                row = cursor.fetchone()

                return row[0]

    def get_game_id(self):

        user_id = self.game.get_creator_id()

        with self.connection() as cursor:
            cursor.execute('''SELECT id FROM games WHERE user_id=%s;''', (user_id, ))

            row = cursor.fetchone()

            return row[0]

    def get_timestamp(self):

        id = self.game.get_id()

        with self.connection() as cursor:
            cursor.execute('''SELECT timestamp FROM games WHERE id=%s;''', (id, ))

            row = cursor.fetchone()

            return row[0]

    def get_available_game_slots(self):

        with self.connection() as cursor:
            cursor.execute('''SELECT available_slots FROM games WHERE id=%s;''', (self.game.id, ))

            row = cursor.fetchone()

            return row[0]

    def take_game_slot(self):

        with self.connection() as cursor:
            cursor.execute('''UPDATE games SET available_slots = available_slots - 1 WHERE id = %s;''', (self.game.id, ))

        if self.get_available_game_slots() <= 0:
            self.update_is_joinable()

    def update_is_joinable(self):
        with self.connection() as cursor:
            cursor.execute('''UPDATE games SET can_join = 0 WHERE available_slots <= 0;''')

    def get_is_joinable(self):

        with self.connection() as cursor:

            cursor.execute('''SELECT can_join FROM games WHERE id=%s;''', (self.game.id, ))

            row = cursor.fetchone()

            return row[0]

    def set_unjoinable(self):
        with self.connection() as cursor:
            cursor.execute('''UPDATE games SET can_join = 0 WHERE id=%s;''', (self.game.id, ))

    def set_archived(self):
        with self.connection() as cursor:
            cursor.execute('''UPDATE games SET is_archived = 1 WHERE id=%s;''', (self.game.id, ))

    def get_all_games(self, joinable = False):

        self.update_is_joinable()

        with self.connection() as cursor:
            if joinable:
                cursor.execute('''SELECT * FROM games WHERE can_join=1;''')
            else:
                cursor.execute('''SELECT * FROM games;''')

            rows = cursor.fetchall()

            games = [convert_to_dict_game(row) for row in rows]

            return games

    def get_previous_games(self, user_id):

        with self.connection() as cursor:

            cursor.execute('''SELECT games.id, players.is_alive, games.timestamp FROM games JOIN players ON players.game_id=games.id WHERE players.user_id=%s AND players.is_archived=1;''', (user_id, ))

            rows = cursor.fetchall()

            games = [convert_to_dict(row, ["game_id", "is_alive", "timestamp"]) for row in rows]

            return games

    def get_game_by_host(self, host):

        with self.connection() as cursor:

            cursor.execute('''SELECT * FROM games WHERE user_id=%s AND is_archived=0;''', (host.get_id(), ))

            row = cursor.fetchone()

            if row:
                game = convert_to_dict_game(row)

                return game
            else:
                return None
