# importing required libraries
import sys
import os
import logging
import random
import numpy as np
import pandas as pd

# TO DO
# PRETTY PRINT MODULE
# LOOK FOR OTHER MODULES

# other import settings
pd.set_option('display.max_columns', None)  # disabling truncation of columns in dataframes

# Import stats datasets
class_stats = pd.read_csv(os.path.join("CSV", "Class_Stats.csv"), header=0, encoding='latin-1')
enemy_stats = pd.read_csv(os.path.join("CSV", "Enemy_Stats.csv"), header=0, encoding='latin-1')

# I - Logging & Output Functionss

# clear log file from previous run of code
# NOT WORKING
if os.path.exists('Brains+BrawnsBattleEncounter.txt'):
    os.remove('Brains+BrawnsBattleEncounter.txt')


# display messages in log screen and adds them to text file
def log_msg(a: str, newline=0):
    level = logging.INFO
    format_ = '%(message)s'
    handlers = [logging.FileHandler('BrainsBrawnsBattleEncounter.txt'), logging.StreamHandler()]
    logging.basicConfig(level=level, format=format_, handlers=handlers)
    logging.info(a)
    if newline == 1:  # default new line is 0
        logging.info(" ")


# === End Of I - Logging & Output Functions ===

# II - Classes
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

        # guard defense
        # will act as a multiplier for defense if guard is up
        self.tempDefenseBoost = 2.5
        self.guardUp = False

        # stats dictionary
        stats_keys = ["Name", "Class", "Max HP", "Current HP", "Attack", "Defense", "Speed", "Move Name", "Move Damage",
                      "Potion Count"]
        stats_values = [self.name, self.class_type, self.max_HP, self.curr_HP, self.attack, self.defense, self.speed,
                        self.move_name, self.move_dmg, self.curr_potionCount]
        self.stats = pd.DataFrame(data=[stats_values], columns=stats_keys)

    def __str__(self):  # for print(playerChar)
        str = "Name: " + self.name + ", " + "Class: " + self.class_type
        return str

    def PrintStats(self):
        log_msg("The stats for " + self.name + " are: \n" + self.stats.to_string())


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

        # guard defense
        # will act as a multiplier for defense if guard is up
        self.tempDefenseBoost = 2.5
        self.guardUp = False

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

    def __str__(self):  # for print (playerChar)
        str = "Name: " + self.name
        return str

    def PrintStats(self):
        log_msg("The stats for " + self.name + " are: \n" + self.stats.to_string())


# global vars
potionHealth = 10

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


# === End Of II - Classes ===

# III - Combat Related Functions

# initialises things needed for combat encounter to start
def initialiseCombat(enemy: Enemy):
    # TO DO LEFT:
    # Check for weakness code and set damage multiplier

    # 1. sort all entities in combat

    # create a list for all entities
    orderOfCombat = [enemy]
    orderOfCombat += playerChars

    # manually sort list based on speed stat of each member
    # list is to be in descending order of speed stat
    # using selection sort
    # i couldnt find any other way T-T
    for i in range(len(orderOfCombat)):

        # take element at i as assumed min
        max = orderOfCombat[i]
        pos = i

        for j in range(i + 1, len(orderOfCombat)):
            if max.speed < orderOfCombat[j].speed:  # if value is smaller than current min, update it
                max = orderOfCombat[j]
                pos = j

        # swap assumed min with actual min
        if i != j:
            orderOfCombat[pos] = orderOfCombat[i]
            orderOfCombat[i] = max

    # print sorted list
    log_msg("The order of combat is: ")
    for i in orderOfCombat:
        log_msg((i.name + ", Speed: " + str(i.speed)))
    log_msg(" ")

    # 2. Restore dead player's health with penalty
    for i in playerChars:
        if i.curr_HP <= 0:
            i.curr_HP = int(i.max_HP * 0.3)  # Restored health == 30% of max

    # checking if it worked
    log_msg("The health of players after restoring health is: ")
    for i in orderOfCombat:
        log_msg(str(i.name + ", Current HP:" + str(i.curr_HP) + ", Max HP: " + str(i.max_HP)))
    log_msg(" ")

    # 3. check for weakness code and set damage multiplier
    # <INCOMPLETE>


# provides choices to players during their turn and acts on them
def playerMenu(player: PlayerChar, enemy: Enemy):  # IN PROGRESS
    log_msg("Menu For: " + player.name)
    log_msg("Choose: \n1.Attack \n2.Guard \n3.Heal")
    choice = int(input("Enter corresponding number: "))
    log_msg("Option Chosen Is: " + str(choice))
    # LEFT TO DO:
    # check for weakness code damage multipliers

    # get guard down if on previously
    if player.guardUp == True:
        player.guardUp = False
        log_msg(player.name + "'s guard was previously up. It has now been lowered to normal.")

    if choice == 1:  # 1. Attack
        # Print move name and dmg
        log_msg("Move Name: " + player.move_name + ", Move DMG: " + str(player.move_dmg))

        # Call for calculation and dealing of damage
        dealDMG_P2E(calculateDMG_P2E(player, enemy), enemy)

    elif choice == 2:  # 2. Guard
        player.guardUp = True
        log_msg(
            player.name + "'s guard has been raised. If attacked, next before next turn, the damage will be significantly reduced")
    elif choice == 3:  # 3. Heal

        # Check if there's any potions left & if health isn't max
        if player.curr_potionCount > 1 and player.curr_HP < player.max_HP:  # if yes, increment health and decrement potion count
            log_msg((player.name + "'s HP:" + str(player.curr_HP) + ", Max HP:" + str(player.max_HP)))
            player.curr_potionCount -= 1
            if player.curr_HP + potionHealth >= player.max_HP:  # don't let health go above max
                player.curr_HP = player.max_HP
            else:
                player.curr_HP += potionHealth
            log_msg((player.name + "'s HP after potion:" + str(player.curr_HP)))
        else:  # if not, send to start of menu
            log_msg(
                "You have no potions left or your health is already at maximum. Please go to the start of the menu again \n")
            playerMenu(player, enemy)

    else:
        log_msg("Invalid Input")


# provides choices to enemy during their turn and acts on them
def enemyMenu(enemy: Enemy):  # IN PROGRESS
    log_msg("Menu For: " + enemy.name)
    log_msg("Choose: \n1. Target Move \n2. Sweeping Move \n3. Guard")
    choice = int(input("Enter corresponding number: "))
    log_msg("Option Chosen Is: " + str(choice))

    # get guard down if on previously
    if enemy.guardUp == True:
        enemy.guardUp = False
        log_msg(enemy.name + "'s guard was previously up. It has now been lowered to normal.")

    # validating menu input
    # LEFT

    player = wizard  # temp
    if choice == 1:  # 1. Target move
        log_msg("\nThe players in combat are: ")
        for i in range(0, len(playerChars)):
            log_msg(str(str(i) + " " + playerChars[i].name))
        target = int(input("Enter number corresponding to player for targeting: "))
        player = playerChars[target]

    if choice == 1 or choice == 2:
        # calculating and dealing damage to player
        dealDMG_E2P(enemy, player, calculateDMG_E2P(enemy, choice, player), choice)
    elif choice == 3:
        enemy.guardUp = True
        log_msg(enemy.name + "'s guard has been raised. If attacked, next before next turn, the damage will be significantly reduced")
        log_msg(" ")



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
    log_msg((enemy.name + "'s HP was: " + str(enemy.curr_HP)))

    # reduce damage if guard is up
    if enemy.guardUp:
        dmg = dmg / enemy.tempDefenseBoost
        log_msg(enemy.name + " had their guard up. Their damage taken was reduced.")
        enemy.guardUp = False

    # decrement health
    enemy.curr_HP -= dmg
    log_msg("Damage dealt was: " + str(dmg))
    log_msg((enemy.name + "'s HP is now: " + str(enemy.curr_HP)))
    log_msg(" ",1)

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
def dealDMG_E2P(enemy: Enemy, player: PlayerChar, dmg: int, move_num: int):
    if (move_num == 1):  # deal damage only to one player
        log_msg(str("Move Name: " + enemy.move1_name))
        log_msg(str("The player targeted is: " + player.name))
        log_msg(str(player.name + "'s HP was: " + str(player.curr_HP)))

        # reduce damage if guard is up
        if player.guardUp:
            dmg = int(dmg / player.tempDefenseBoost)
            log_msg(player.name + " had their guard up. Their damage taken was reduced.")
            player.guardUp = False

        # decrement health
        player.curr_HP -= dmg

        log_msg(str("Damage dealt was: " + str(dmg)))
        log_msg(str(player.name + "'s HP is now: " + str(player.curr_HP)))

    elif move_num == 2:  # deal damage to everyone
        log_msg(("Move Name: " + enemy.move2_name))
        log_msg("This move deals damage to all players")
        for i in playerChars:
            log_msg((i.name + "'s HP was: " + str(i.curr_HP)))

            # reduce damage if guard is up
            if i.guardUp:
                i.curr_HP -= int(dmg / player.tempDefenseBoost)  # decrement health with reduced damage
                log_msg(i.name + " had their guard up. Their damage taken was reduced.")
                i.guardUp = False
                log_msg(("Damage dealt was: " + str(int(dmg / player.tempDefenseBoost))))
            else:  # decrement health with normal damage
                i.curr_HP -= dmg
                log_msg(("Damage dealt was: " + str(dmg)))

            log_msg((i.name + "'s HP is now: " + str(i.curr_HP)))

    log_msg(" ",1)


# === End Of III - Combat Related Functions ===

# IV - Functions Related To Start Of Whole Program
def initialise():
    # printing stats for all entities in game
    log_msg("The player stats are: ")
    for i in playerChars:
        i.PrintStats()
        log_msg(" ")
    log_msg("\n")

    log_msg("The stats for the enemies are: ")
    for i in enemyChars:
        i.PrintStats()
        log_msg(" ")
    log_msg("\n")


def main():
    initialise()

    initialiseCombat(mimir)

    # testing enemy and player turns
    for i in range(3):
        playerMenu(archer, mimir)
        enemyMenu(mimir)
        playerMenu(wizard, mimir)
        playerMenu(knight, mimir)



# run only the main function if the .py file is run
if __name__ == "__main__":
    main()
