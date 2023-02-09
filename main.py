# importing required libraries
import sys
import os
import logging
import random
import numpy as np
import pandas as pd

# other import settings
pd.set_option('display.max_columns', None)  # disabling truncation of columns in dataframes

# Import stats datasets
class_stats = pd.read_csv(os.path.join("CSV", "Class_Stats.csv"), header=0, encoding='latin-1')
enemy_stats = pd.read_csv(os.path.join("CSV", "Enemy_Stats.csv"), header=0, encoding='latin-1')


# Player Character Class
class PlayerChar:
    def __init__(self, name, class_num: int):
        # draw stats from stats csv based on index
        self.name = name

        # class num: 0 - Wizard, 1 - Knight, 2 - Archer
        self.class_type = class_stats.iat[class_num, 0]

        # modifier stats
        # access them from csv
        mHP = class_stats.iat[class_num, 1]
        mattack = class_stats.iat[class_num, 2]
        mdefense = class_stats.iat[class_num, 3]
        mspeed = class_stats.iat[class_num, 4]

        # roll basic stats using modifiers
        self.max_HP = random.randint(40, 50) + mHP
        self.curr_HP = self.max_HP
        self.attack = random.randint(10, 15) + mattack
        self.defense = random.randint(10, 15) + mdefense
        self.speed = random.randint(10, 15) + mspeed

        # move and damage
        self.move_name = class_stats.iat[class_num, 5]
        self.move_dmg = class_stats.iat[class_num, 6]

        # potion counts
        self.max_potionCount = class_stats.iat[class_num, 7]
        self.curr_potionCount = self.max_potionCount

        # stats dictionary
        stats_keys = ["Name", "Class", "Max HP", "Current HP", "Attack", "Defense", "Speed", "Move Name", "Move Damage",
                      "Potion Count"]
        stats_values = [self.name, self.class_type, self.max_HP, self.curr_HP, self.attack, self.defense, self.speed,
                        self.move_name, self.move_dmg, self.curr_potionCount]
        self.stats = pd.DataFrame(data=[stats_values], columns=stats_keys)

    def PrintStats(self):
        print("The stats for " + self.name + " are: \n", self.stats)


class Enemy:
    def __init__(self, enemy_num: int):
        # draw stats from stats csv based on index
        # enemy num: 0 - Sphinx, 1 - Mimir, 2 - Athena
        self.enemy_num = enemy_num
        self.name = enemy_stats.iat[enemy_num, 0]

        # read stats from csv
        self.max_HP = enemy_stats.iat[enemy_num, 1]
        self.curr_HP = self.max_HP
        self.attack = enemy_stats.iat[enemy_num, 2]
        self.defense = enemy_stats.iat[enemy_num, 3]
        self.speed = enemy_stats.iat[enemy_num, 4]

        # moves and damage
        self.move1_name = enemy_stats.iat[enemy_num, 5]
        self.move1_dmg = enemy_stats.iat[enemy_num, 6]
        self.move2_name = enemy_stats.iat[enemy_num, 7]
        self.move2_dmg = enemy_stats.iat[enemy_num, 8]

        # stats dictionary
        stats_keys = ["Name", "Max HP", "Current HP", "Attack", "Defense", "Speed", "Move 1 Name", "Move 1 Damage",
                      "Move 2 Name", "Move 3 Damage", ]
        stats_values = [self.name, self.max_HP, self.curr_HP, self.attack, self.defense, self.speed,
                        self.move1_name, self.move1_dmg, self.move2_name, self.move2_dmg]
        self.stats = pd.DataFrame(data=[stats_values], columns=stats_keys)

    def PrintStats(self):
        print("The stats for " + self.name + " are: \n", self.stats)


# global vars
# to be reworked
global wizard, archer, knight
global sphinx, mimir, athena
global playerChars, enemyChars

# creating player chars
wizard = PlayerChar("Wizard", 0)
knight = PlayerChar("Knight", 1)
archer = PlayerChar("Archer", 2)

# print stats for all characters
playerChars = [wizard, archer, knight]

# creating enemy chars
sphinx = Enemy(0)
mimir = Enemy(1)
athena = Enemy(2)

# print stats for all characters
enemyChars = [sphinx, mimir, athena]


# display messages in log screen and adds them to text file
def log_msg(a: str, newline):
    level = logging.INFO
    format_ = '%(message)s'
    handlers = [logging.FileHandler('Brains+BrawnsBattleEncounter.txt'), logging.StreamHandler()]
    logging.basicConfig(level=level, format=format_, handlers=handlers)
    logging.info(a)
    if newline == 1:
        logging.info(" ")


# player to enemy damage calculator
# uses player's attack and dmg along with enemy's defense + some randomisation
def calculateDMG_P2E(player: PlayerChar, enemy: Enemy) -> int:
    # random factor
    randomfac = random.uniform(1, 2)

    # calculate damage
    dmg = (player.attack * player.move_dmg * randomfac) / enemy.defense
    return int(dmg)


# actually deals damage and updates the enemy's hp
def dealDMG_P2E(dmg: int, enemy: Enemy):
    print(enemy.name, "'s HP was: ", enemy.curr_HP)
    enemy.curr_HP -= dmg
    print(enemy.name, "'s HP is now: ", enemy.curr_HP)
    print("Damage dealt was: ", dmg)


# enemy to player damage calculator
# uses enemy's attack and dmg along with player's defense + some randomisation
def calculateDMG_E2P(enemy: Enemy, move_num: int, player: PlayerChar) -> int:
    # random factor
    randomfac = random.uniform(0.1, 0.45)

    #  pick move number (thus dmg) based on move_num arg
    if move_num == 1:
        move_dmg = enemy_stats.iat[enemy.enemy_num, 6]  # move 1
    elif move_num == 2:
        move_dmg = enemy_stats.iat[enemy.enemy_num, 8]  # move 2

    # calculate damage per player (regardless of move type)
    dmg = (enemy.attack * move_dmg * randomfac) / player.defense
    return int(dmg)


# actually deals damage and updates the enemy's hp
def dealDMG_E2P(player: PlayerChar, dmg: int, move_num: int):
    if (move_num == 1):  # deal damage only to one player
        print("This move deals damage only to ",player.name)
        print(player.name, "'s HP was: ", player.curr_HP)
        player.curr_HP -= dmg
        print(player.name, "'s HP is now: ", player.curr_HP)
        print("Damage dealt was: ", dmg)
    elif (move_num == 2): # deal damage to everyone
        print("This move deals damage to all players")
        for i in playerChars:
            print(i.name, "'s HP was: ", i.curr_HP)
            player.curr_HP -= dmg
            print(i.name, "'s HP is now: ", i.curr_HP)
            print("Damage dealt was: ", dmg)
            print()



def initialise():
    # printing stats for all entities in game
    for i in playerChars:
        i.PrintStats()
        print()

    for i in enemyChars:
        i.PrintStats()
        print()


def main():
    initialise()

    # dealDMG_P2E(calculateDMG_P2E(wizard, sphinx), sphinx)

    # calculateDMG_E2P(sphinx, 1, wizard)
    playertohit = wizard
    enemyhitting = sphinx
    move_num = 2
    dealDMG_E2P(playertohit, calculateDMG_E2P(enemyhitting, move_num, playertohit), move_num)

    """print("Enemy To Specific Player, Move 1: ", calculateDMG_E2P(sphinx,1,wizard))
    print("Enemy To Each Player, Move 2: ", calculateDMG_E2P(sphinx,2,wizard))"""


# run only the main function if the .py file is run
if __name__ == "__main__":
    main()
