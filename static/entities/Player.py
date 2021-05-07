import os
import sys
from datetime import datetime

ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/../../"

# Include application directories in the path to allow imports
sys.path.insert(1, ROOT_DIRECTORY + "/static/database/connections/")
sys.path.insert(1, ROOT_DIRECTORY + "/static/entity_interaction/player/")

from PlayerConnection import PlayerConnection
from User import User
import Game # Used instead of from Game import Game to prevent cyclic imports

from Upgrader import *

# Constants related to game balancing
STARTING_HP = 10.0
STARTING_MAX_HP = 10.0
STARTING_HEAL = 2.0
STARTING_ARMOR = 1.0
STARTING_ATTACK = 1.0
STARTING_INCOME = 5.0
STARTING_ENERGY_INCREASE = 1
STARTING_ENERGY_ACCELERATION = 0.05

STARTING_COINS = 0.0
STARTING_ENERGY = 0.0

# Class used to define and interact with players
class Player:

    # Initialize a Player instance, set variables
    def __init__(self, user = None, game = None, id = None):

        self.is_alive = True
        self.user = user
        self.game = game

        self.connection = PlayerConnection(self)
        self.upgrader = Upgrader(self)

        self.id = id
        self.set_attributes()

        self.timestamp = None

        self.is_archived = False

    def set_attributes(self, stats = {}):

        self.id = stats.get("id", self.id)
        self.hp = stats.get("hp", STARTING_HP)
        self.max_hp = stats.get("max_hp", STARTING_MAX_HP)
        self.heal = stats.get("heal", STARTING_HEAL)
        self.armor = stats.get("armor", STARTING_ARMOR)
        self.attack = stats.get("attack", STARTING_ATTACK)
        self.income = stats.get("income", STARTING_INCOME)
        self.coins = stats.get("coins", STARTING_COINS)
        self.energy = stats.get("energy", STARTING_ENERGY)
        self.energy_increase = stats.get("energy_increase", STARTING_ENERGY_INCREASE)
        self.energy_acceleration = stats.get("energy_acceleration", STARTING_ENERGY_ACCELERATION)
        self.is_alive = stats.get("is_alive", True)
        self.is_archived = stats.get("is_archived", False)

    def create(self):
        return self.connection.create_player()

    def write(self, timestamp = False):
        return self.connection.write(timestamp)

    def get_attributes_by_id(self):

        attributes = self.connection.get_stats()

        if attributes == None:
            return False
        else:
            self.set_attributes(attributes)
            return True

    def get_username(self):
        return self.get_user().get_username()

    def get_user_id(self):

        if not self.user == None:
            return self.user.get_id()

        else:
            return self.connection.get_user_id()

    def get_game_id(self):

        if not self.game == None:
            return self.game.get_id()

        else:
            return self.connection.get_game_id()

    def get_user(self):

        if not self.user == None:
            return self.user

        else:
            self.user = User(id = self.get_user_id())
            return self.user

    def get_game(self):

        if not self.game == None:
            return self.game

        else:
            self.game = Game.Game(id = self.get_game_id())
            return self.game

    def get_is_alive(self):
        return self.is_alive

    def get_is_archived(self):
        return self.is_archived

    def get_stats(self):

        stats = self.connection.get_stats()

        self.set_attributes(stats)

        self.timestamp = stats["timestamp"]

    def get_id(self):

        if not self.id == None:
            return self.id

        self.id = self.connection.get_player_id()

        return self.id

    def get_level(self):

        level = 0

        level += self.max_hp / MAX_HP_UPGRADE_AMOUNT
        level += self.heal / HEAL_UPGRADE_AMOUNT
        level += self.armor / ARMOR_UPGRADE_AMOUNT
        level += self.attack / ATTACK_UPGRADE_AMOUNT
        level += self.income / INCOME_UPGRADE_AMOUNT

        level *= UPGRADE_COST

        level += self.coins

        return int(level)

    def deplete_energy(self):

        self.energy = 0
        self.write()

    def increase_skill(self, write = True):

        self.energy_acceleration += (self.energy / self.energy_increase) / 25.0

        if write:
            self.write()

    def attack_player(self, victim):

        self.increase_skill(write = False)

        attack_amount = self.attack * self.energy

        victim.get_stats()

        victim.injure(attack_amount, self)

        self.deplete_energy()



#  Updating Methods



    def injure(self, amount, attacker):

        self.hp -= amount / self.armor

        if self.hp <= 0:
            self.set_dead(attacker)

        self.write()

    def update_stats(self):
        self.get_stats()

        current_timestamp = datetime.now()

        self_timestamp = datetime.fromisoformat(self.timestamp)

        difference =  current_timestamp - self_timestamp

        difference_seconds = difference.seconds

        self.update_coins(difference_seconds)
        self.update_energy(difference_seconds)
        self.update_energy_increase(difference_seconds)
        self.update_health(difference_seconds)

        self.timestamp = current_timestamp.isoformat(sep = ' ', timespec = 'seconds')

        self.write(timestamp = True)

    def update_timestamp_to_now_if_unchanged(self):

        if self.energy_increase == STARTING_ENERGY_INCREASE:

            current_timestamp = datetime.now()

            self.timestamp = current_timestamp.isoformat(sep = ' ', timespec = 'seconds')

            self.write(timestamp = True)

    def update_coins(self, seconds):
        self.coins += self.income * (seconds / 60.0)

    def update_energy(self, seconds):
        self.energy += self.energy_increase * (seconds / 60.0)

    def update_energy_increase(self, seconds):
        self.energy_increase += self.energy_acceleration * (seconds / 60.0)

    def update_health(self, seconds):
        self.hp += self.heal * (seconds / 60.0)

        if self.hp >= self.max_hp:
            self.hp = self.max_hp

    def set_dead(self, attacker):
        self.is_alive = False

        self.on_death(attacker)

    def on_death(self, attacker):

        loot = self.get_loot()

        attacker.coins += loot

        self.set_archived()

        self.write()

        game = self.get_game()

        game.check_is_done()

    def get_loot(self):
        return (0.75 * self.coins) + (0.25 * self.get_level())



# Displaying Methods



    def get_effective_hp(self):
        return round(self.hp, 1)

    def get_display_hp(self):
        return round(self.hp, 1)

    def get_display_max_hp(self):
        return round(self.max_hp, 1)

    def get_display_heal(self):
        return round(self.heal, 1)

    def get_display_armor(self):
        return round(self.armor, 1)

    def get_display_attack(self):
        return round(self.attack, 1)

    def get_display_income(self):
        return int(self.income)

    def get_display_coins(self):
        return int(self.coins)

    def get_display_energy(self):
        return round(self.energy, 2)

    def get_display_data(self):
        stats = {}

        stats['hp'] = self.get_display_hp()
        stats['true_hp'] = self.hp
        stats['max_hp'] = self.get_display_max_hp()
        stats['true_max_hp'] = self.get_display_max_hp()
        stats['heal'] = self.get_display_heal()
        stats['armor'] = self.get_display_armor()
        stats['attack'] = self.get_display_attack()
        stats['income'] = self.get_display_income()
        stats['coins'] = self.get_display_coins()
        stats['energy'] = self.get_display_energy()
        stats['level'] = self.get_level()
        stats['is_alive'] = self.get_is_alive()
        stats['is_archived'] = self.get_is_archived()

        return stats

    def get_broadcasting_data(self):
        stats = {}

        stats['id'] = self.get_id()
        stats['username'] = self.get_username()
        stats['effective_hp'] = self.get_effective_hp()
        stats['level'] = self.get_level()
        stats['is_alive'] = self.get_is_alive()

        return stats

    def upgrade(self, type, amount):

        self.get_stats()

        upgrade = self.upgrader.upgrade(type, amount)

        if upgrade == True:
            self.write()

        return upgrade

    def set_archived(self):
        self.is_archived = True
