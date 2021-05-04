UPGRADE_COST = 5.0

HP_UPGRADE_AMOUNT = 0.0
MAX_HP_UPGRADE_AMOUNT = 5.0
HEAL_UPGRADE_AMOUNT = 0.2
ARMOR_UPGRADE_AMOUNT = 0.5
ATTACK_UPGRADE_AMOUNT = 0.5
INCOME_UPGRADE_AMOUNT = 1.0

class Upgrader:

    def __init__(self, player):
        self.player = player

    def upgrade(self, type, amount):

        if type == "max_hp":
            return self.upgrade_max_hp(amount)
        elif type == "heal":
            return self.upgrade_heal(amount)
        elif type == "armor":
            return self.upgrade_armor(amount)
        elif type == "attack":
            return self.upgrade_attack(amount)
        elif type == "income":
            return self.upgrade_income(amount)
        else:
            return False

    def upgrade_amount(self, amount):

        try:
            amount = int(amount)
        except:
            return False

        if amount <= 0:
            return False

        amount_in_coins = amount * UPGRADE_COST

        if amount_in_coins > self.player.coins:

            amount = int(self.player.coins / UPGRADE_COST)
            self.player.coins = self.player.coins % UPGRADE_COST

            if amount < 1:
                return False
            else:
                return amount

        else:
            self.player.coins -= amount_in_coins

            return amount

    def upgrade_max_hp(self, amount):

        upgrade_amount_corrected = self.upgrade_amount(amount)

        if upgrade_amount_corrected == False:
            return False

        else:
            self.player.max_hp += upgrade_amount_corrected * MAX_HP_UPGRADE_AMOUNT
            self.player.hp += upgrade_amount_corrected * HP_UPGRADE_AMOUNT

            return True

    def upgrade_heal(self, amount):

        upgrade_amount_corrected = self.upgrade_amount(amount)

        if upgrade_amount_corrected == False:
            return False

        else:
            self.player.heal += upgrade_amount_corrected * HEAL_UPGRADE_AMOUNT

            return True

    def upgrade_armor(self, amount):

        upgrade_amount_corrected = self.upgrade_amount(amount)

        if upgrade_amount_corrected == False:
            return False

        else:
            self.player.armor += upgrade_amount_corrected * ARMOR_UPGRADE_AMOUNT

            return True

    def upgrade_attack(self, amount):

        upgrade_amount_corrected = self.upgrade_amount(amount)

        if upgrade_amount_corrected == False:
            return False

        else:
            self.player.attack += upgrade_amount_corrected * ATTACK_UPGRADE_AMOUNT

            return True

    def upgrade_income(self, amount):

        upgrade_amount_corrected = self.upgrade_amount(amount)

        if upgrade_amount_corrected == False:
            return False

        else:
            self.player.income += upgrade_amount_corrected * INCOME_UPGRADE_AMOUNT

            return True
