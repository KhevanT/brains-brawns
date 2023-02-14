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

# global vars
potionHealth = 10
attackBoost = 1.25

# I - Logging & Output Functions

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
        self.alive = True  # DOA status

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

    def isAlive(self):
        if self.curr_HP > 0:
            self.alive = True
        else:
            self.curr_HP = 0  # min value of curr hp
            self.alive = False

        return self.alive


class Enemy:
    def __init__(self, enemy_num: int):
        # draw stats from stats csv based on index
        # enemy num: 0 - Sphinx, 1 - Mimir, 2 - Athena
        self.enemy_num = enemy_num
        self.name = enemy_stats.iat[enemy_num, 0]

        # read stats from csv
        self.max_HP = enemy_stats.iat[enemy_num, 1]
        self.curr_HP = self.max_HP
        self.alive = True  # DOA status

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

        # weakness code
        self.weakness = enemy_stats.iat[enemy_num, 9]
        self.weaknessActive = False

        # stats dictionary
        stats_keys = ["Name", "Max HP", "Current HP", "Attack", "Defense", "Speed", "Move 1 Name", "Move 1 Damage",
                      "Move 2 Name", "Move 2 Damage", ]
        stats_values = [self.name, self.max_HP, self.curr_HP, self.attack, self.defense, self.speed,
                        self.move1_name, self.move1_dmg, self.move2_name, self.move2_dmg]
        self.stats = pd.DataFrame(data=[stats_values], columns=stats_keys)

    def __str__(self):  # for print (playerChar)
        str = "Name: " + self.name
        return str

    def PrintStats(self):
        log_msg("The stats for " + self.name + " are: \n" + self.stats.to_string())

    def isAlive(self):
        if self.curr_HP > 0:
            self.alive = True
        else:
            self.curr_HP = 0  # min value of curr hp
            self.alive = False

        return self.alive


# creating player chars (default values in case of errors with character creation
classes = ["Wizard", "Knight", "Archer"]
wizard = PlayerChar("Wizard", 0)
knight = PlayerChar("Knight", 1)
archer = PlayerChar("Archer", 2)
# create char list
playerChars = [wizard, knight, archer]

# creating enemy chars
sphinx = Enemy(0)
mimir = Enemy(1)
athena = Enemy(2)

# create enemy list
enemyChars = [sphinx, mimir, athena]


# === End Of II - Classes ===

# III - Combat Related Functions


def characterCreation():
    names = []
    global classes
    for i in classes:
        log_msg("For class: " + i)
        log_msg("Enter Name: ")
        name = input()
        log_msg("The " + i + " of the party is: " + name)
        names.append(name)
        log_msg(" ")

    # creating player chars
    global wizard, knight, archer, playerChars
    wizard = PlayerChar(names[0], 0)
    knight = PlayerChar(names[1], 1)
    archer = PlayerChar(names[2], 2)

    # create char list
    playerChars = [wizard, knight, archer]

    # printing stats for all entities in game
    log_msg("The player stats are: ")
    for i in playerChars:
        i.PrintStats()
        log_msg(" ")
    log_msg("\n")

    '''log_msg("The stats for the enemies are: ")
    for i in enemyChars:
        i.PrintStats()
        log_msg(" ")
    log_msg("\n")'''


# initialises things needed for combat encounter to start
def initialiseCombat(enemy: Enemy):
    # 1. check for weakness code and set damage multiplier
    log_msg("Would you like to enter the answer to the weakness riddle?: (Y/N)")
    ch = input().upper()
    if ch == 'Y':
        log_msg("Enter the answer to the weakness riddle: ")
        ans = input().lower()
        if ans == enemy.weakness:
            log_msg(
                "Congratulations! The weakness found is correct! All your attacks will do significantly more damage to the enemy!")
            enemy.weaknessActive = True
        else:
            log_msg("The weakness you found was incorrect. You do not get an attack boost for this encounter")

    # 2. sort all entities in combat

    # create a list for all entities
    global orderOfCombat
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
    log_msg(" ")
    log_msg("The order of combat is: ")
    for i in orderOfCombat:
        log_msg((i.name + ", Speed: " + str(i.speed)))
    log_msg(" ")

    # 3. Restore dead player's health with penalty and alive's health fully
    for i in playerChars:
        if i.curr_HP <= 0:
            i.curr_HP = int(i.max_HP * 0.3)  # Restored health == 30% of max
        else:
            i.curr_HP = i.max_HP

    # reset all unused guards
    for i in playerChars:
        i.guardUp = False

    # checking if it worked
    log_msg("The health of players with 0 HP from previous combat has been restored with a penalty")
    log_msg(" ")
    '''log_msg("The health of players after restoring health is: ")
    for i in orderOfCombat:
        log_msg(str(i.name + ", Current HP:" + str(i.curr_HP) + ", Max HP: " + str(i.max_HP)))
    log_msg(" ")'''


# provides choices to players during their turn and acts on them
def playerMenu(player: PlayerChar, enemy: Enemy):
    global orderOfCombat

    while True:
        log_msg("Menu For: " + player.name)

        log_msg(player.name + "'s current HP is: " + str(player.curr_HP))
        log_msg("The enemy " + enemy.name + "'s current HP is: " + str(enemy.curr_HP))
        log_msg("Your Potion Count: " + str(player.curr_potionCount))

        log_msg(str("Order Of Combat:" + orderOfCombat[0].name + " --> " +
                    orderOfCombat[1].name + " --> " + orderOfCombat[2].name +
                    " --> " + orderOfCombat[3].name))

        log_msg("Choose: \n1.Attack \n2.Guard \n3.Heal")
        log_msg("Enter corresponding number: ")
        choice = int(input())
        # validating menu input
        if choice in range(1,4):
            break
        else:
            log_msg("User input is incorrect, please enter again.")

    log_msg("Option Chosen Is: " + str(choice))

    # get guard down if on previously
    if player.guardUp:
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
def enemyMenu(enemy: Enemy):
    while True:
        log_msg("Menu For: " + enemy.name)
        log_msg(enemy.name + "'s current HP is: " + str(enemy.curr_HP))
        log_msg("Choose: \n1. Target Move \n2. Sweeping Move \n3. Guard")
        log_msg("Enter corresponding number:")
        choice = int(input())
        log_msg("Option Chosen Is: " + str(choice))

        # validating menu input
        if choice in range(1,4):
            break
        else:
            log_msg("User input is incorrect, please enter again.")

    # get guard down if on previously
    if enemy.guardUp:
        enemy.guardUp = False
        log_msg(enemy.name + "'s guard was previously up. It has now been lowered to normal.")

    global playerChars
    player = wizard  # temp
    if choice == 1:  # 1. Target move
        log_msg("\nThe players in combat are: ")
        for i in range(0, len(playerChars)):
            if playerChars[i].isAlive():
                log_msg(str(str(i + 1) + " " + playerChars[i].name))
        log_msg("Enter number corresponding to player for targeting: ")
        target = int(input()) - 1

        # validating menu input
        if target in range(3):
            pass
        else:
            log_msg("User input is incorrect, please enter again from the start")
            enemyMenu(enemy)

        player = playerChars[target]

    if choice == 1 or choice == 2:
        # calculating and dealing damage to player
        dealDMG_E2P(enemy, player, calculateDMG_E2P(enemy, choice, player), choice)
    elif choice == 3:
        enemy.guardUp = True
        log_msg(
            enemy.name + "'s guard has been raised. If attacked, next before next turn, the damage will be significantly reduced")
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
        dmg = int(dmg / enemy.tempDefenseBoost)
        log_msg(enemy.name + " had their guard up. Their damage taken was reduced.")
        enemy.guardUp = False

    # check for weakness code boost
    if enemy.weaknessActive == True:
        dmg = int(dmg * attackBoost)

    # decrement health
    enemy.curr_HP -= int(dmg)
    log_msg("Damage dealt was: " + str(dmg))
    log_msg((enemy.name + "'s HP is now: " + str(enemy.curr_HP)))
    log_msg(" ", 1)


# enemy to player damage calculator
# uses enemy's attack and dmg along with player's defense + some randomisation
def calculateDMG_E2P(enemy: Enemy, move_num: int, player: PlayerChar) -> int:
    # random factor
    randomfac = random.uniform(0.2, 0.45)

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

    log_msg(" ", 1)


# === End Of III - Combat Related Functions ===

# IV - Functions Related To Start Of Whole Program


def gameLogic():
    # title
    log_msg("Welcome to Brains + Brawns!")

    # character creation
    log_msg("Character Creation: ")
    # characterCreation()
    log_msg(" ", 1)

    # function to check if all players are alive or not
    # VERY INEFFICIENT
    def isPartyAlive():
        global playerChars
        # playerChars[0].isAlive() and playerChars[1].isAlive() and playerChars[2].isAlive()
        partyalive = not all(player.isAlive() == False for player in playerChars)
        return partyalive

    # turns of combat
    global enemyChars

    # reduce all players hp to 1 for testing
    # TESTING
    '''for i in playerChars:
        i.curr_HP = 1'''

    for enemy in enemyChars:  # loop code for number of enemies
        if isPartyAlive():

            log_msg("Encounter With " + enemy.name)

            while True:
                # ask if combat or riddle
                log_msg("Will you: \n1. Solve Riddle & Skip Combat \n2. Engage In Combat")
                log_msg("Enter The Menu Choice: ")
                choice = int(input())

                # validating menu input
                if choice == 1 or choice == 2:
                    break
                else:
                    log_msg("User input is incorrect, please enter again.")

            if choice == 1:
                log_msg("The party has decided to solve " + enemy.name + "'s riddle and skip combat")
                log_msg(" ")
                continue  # skip to next loop

            # instead of choice 2, just directly go to next bit since if its choice 1, the code below will be skipped
            log_msg("The party has decided to engage in combat with " + enemy.name, 1)
            initialiseCombat(enemy)  # initiate combat

            # to do left: check for player health and terminate code accordingly
            while enemy.alive and isPartyAlive():  # stop all turns if enemy is dead
                for i in orderOfCombat:
                    if enemy.isAlive() and isPartyAlive():  # have next turn only is enemy is alive
                        if i.isAlive():  # give options only if player is alive
                            log_msg(" ")  # print menu corresponding to type of entity
                            if type(i) == Enemy:
                                enemyMenu(i)
                            elif type(i) == PlayerChar:
                                playerMenu(i, enemy)

                        else:  # dead player can't take their turn
                            log_msg(i.name + "'s HP is 0. They cannot take their turn.")
                    elif not enemy.isAlive():  # WIN!
                        break  # break out of for loop used for turns
                    elif not isPartyAlive():  # LOSE :(((
                        break  # break out of for loop used for turns'

            if not enemy.isAlive():  # WIN!
                log_msg(enemy.name + "'s HP is now 0. They have been defeated! Congratulations!")
                log_msg("Please collect your treasure piece and next set of riddles!")
                log_msg(" ")
            elif not isPartyAlive():  # LOSE :(((
                log_msg(
                    "All your party members have lost their HP. You have lost the game and must return to base location")
                log_msg("Make sure to stop your team's timer and carry all your treasure pieces with you to base")
                log_msg("Thank you for playing!")


def main():
    gameLogic()


# run only the main function if the .py file is run
if __name__ == "__main__":
    main()
