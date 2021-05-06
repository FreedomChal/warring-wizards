import sys
import os
import sqlite3
from datetime import datetime
from Connection import Connection

# Note: This constant MUST be changed if the players table is modified.
COLUMNS = ("id", "user_id", "game_id", "hp", "max_hp", "heal", "armor", "attack",
           "income", "coins", "energy", "energy_increase", "energy_acceleration", "timestamp", "is_alive", "is_archived")

def convert_to_dict_player(column_values):

    player_dict = {COLUMNS[i]: column_values[i] for i in range(len(COLUMNS))}

    return player_dict

class PlayerConnection:

    def __init__(self, player = None):
        self.connection = Connection
        self.player = player

    def create_player(self):

        if not self.is_duplicate_player():

            current_timestamp = datetime.now().isoformat(sep = ' ', timespec = 'seconds')

            with self.connection() as cursor:
                cursor.execute('''INSERT INTO players
                    (user_id, game_id, hp, max_hp, heal, armor, attack, income, coins, energy, energy_increase, energy_acceleration, timestamp)
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                    (self.player.get_user_id(), self.player.get_game_id(), self.player.hp, self.player.max_hp, self.player.heal,
                    self.player.armor, self.player.attack, self.player.income, self.player.coins, self.player.energy,
                    self.player.energy_increase, self.player.energy_acceleration, current_timestamp))
                return True

        return False

    def write(self, timestamp = False):

        if self.is_duplicate_player():

            if timestamp:
                return self.write_with_timestamp()
            else:
                return self.write_without_timestamp()

        return False

    def write_with_timestamp(self):

        with self.connection() as cursor:
            cursor.execute('''UPDATE players SET
                hp=?,
                max_hp=?,
                heal=?,
                armor=?,
                attack=?,
                income=?,
                coins=?,
                energy=?,
                energy_increase=?,
                energy_acceleration=?,
                timestamp=?,
                is_alive=?
                WHERE user_id=? AND game_id=?;''',
                (self.player.hp, self.player.max_hp, self.player.heal,
                self.player.armor, self.player.attack, self.player.income, self.player.coins, self.player.energy,
                self.player.energy_increase, self.player.energy_acceleration, self.player.timestamp, self.player.is_alive,
                self.player.get_user_id(), self.player.get_game_id()))

            return True

    def write_without_timestamp(self):

        with self.connection() as cursor:
            cursor.execute('''UPDATE players SET
                hp=?,
                max_hp=?,
                heal=?,
                armor=?,
                attack=?,
                income=?,
                coins=?,
                energy=?,
                energy_increase=?,
                energy_acceleration=?,
                is_alive=?,
                is_archived=?
                WHERE id=?;''',
                (self.player.hp, self.player.max_hp, self.player.heal,
                self.player.armor, self.player.attack, self.player.income, self.player.coins, self.player.energy,
                self.player.energy_increase, self.player.energy_acceleration, int(self.player.is_alive),
                self.player.is_archived, self.player.get_id()))

            return True

    def is_duplicate_player(self):

        with self.connection() as cursor:
            cursor.execute('''SELECT COUNT(*) FROM players WHERE user_id=? AND is_archived=0;''', (self.player.get_user_id(), ))

            row = cursor.fetchone()

            if row[0] != 0:
              return True
            else:
              return False

    def get_player_id(self):
        with self.connection() as cursor:

            cursor.execute('''SELECT id FROM players WHERE user_id=? AND game_id=?;''', (self.player.user.get_id(), self.player.game.get_id()))

            row = cursor.fetchone()

            return row[0]

    def get_player_data_by_user_and_game(self, user, game):
        with self.connection() as cursor:

            cursor.execute('''SELECT * FROM players WHERE user_id=? AND game_id=?;''', (user.get_id(), game.get_id()))

            row = cursor.fetchone()

            return convert_to_dict_player(row)

    def get_user_id(self):
        with self.connection() as cursor:

            cursor.execute('''SELECT user_id FROM players WHERE id=?;''', (self.player.id, ))

            row = cursor.fetchone()

            return row[0]

    def get_game_id(self):
        with self.connection() as cursor:

            cursor.execute('''SELECT game_id FROM players WHERE id=?;''', (self.player.id, ))

            row = cursor.fetchone()

            return row[0]

    def get_stats(self):
        with self.connection() as cursor:
            cursor.execute('''SELECT * FROM players WHERE id=?;''', (self.player.get_id(), ))

            row = cursor.fetchone()

            stats = convert_to_dict_player(row)

            return stats

    def get_all_players(self, game):

        with self.connection() as cursor:
            cursor.execute('''SELECT * FROM players WHERE game_id=?;''', (game.get_id(), ))

            rows = cursor.fetchall()

            players = [convert_to_dict_player(row) for row in rows]

            return players

    def get_living_players(self, game):

        with self.connection() as cursor:

            cursor.execute('''SELECT * FROM players WHERE game_id=? AND is_alive=1;''', (game.get_id(), ))

            rows = cursor.fetchall()

            living_players = [convert_to_dict_player(row) for row in rows]

            return living_players
