#importing necessary tools
import pandas as pd
import matplotlib as plt
import os

#initializing variables
moveselect = True
playerstun1 = False
playerstun2 = False
punish1 = 0
punish2 = 0
gameend =False
selecting1 = True
selecting2 = True
interrupt = False
doubling = False
Moves = ["nothing", "strike", "kick", "dodge", "parry", "heal"]
Characters = ["Knight", "Samurai", "Mage", "Cowboy", "Pirate", "Ninja", "Astronaut", "Copycat"]
HP1 = 15
HP2 = 15

#creating classes for characters
class Character:
    def __init__(self, name):
        self.name = name

#note: overheal mechanic perchance? (healing over your max health gives you temporary HP for that turn. would certainly make coding this easier and maybe make the game more interesting)

class Knight(Character):
    def __init__(self, playerhp):
        self.playerhp = playerhp
    def help(self):
        print("MOVES: \n Strike - Deals 2 damage, interrupts Heal (STRIKE type)\n Kick - Deals 1 damage, deals 3 damage against Dodge (KICK type)\nDodge - Counters Strike and Parry. Causes Strike to miss, granting an extra turn if dodged. Causes Parry to miss, granting an extra turn and +2 damage to any attacks done during said turn (DODGE type)\n Parry - Counters any attacks, returning the attack with an extra +2 damage (PARRY type)\n Heal - Heals for 2 HP (HEAL type)")
    def moveinfo(self, move):
        if move == "strike":
            damage = 2
            interrupt = True
            heal = 0
            movetype = "striketype"
            return damage, interrupt, heal, movetype
        if move == "kick":
            damage = 1
            interrupt = False
            heal = 0
            movetype = "kicktype"
            return damage, interrupt, heal, movetype
        if move == "dodge":
            damage = 0
            interrupt = False
            heal = 0
            movetype = "dodgetype"
            return damage, interrupt, heal, movetype
        if move == "parry":
            damage = 0
            interrupt = False
            heal = 0
            movetype = "parrytype"
            return damage, interrupt, heal, movetype
        if move == "heal":
            damage = 0
            interrupt = False
            heal = 2
            movetype = "healtype"
            return damage, interrupt, heal, movetype
        else:
            damage = 0
            interrupt = False
            heal = 0
            movetype = "nothing"
            return damage, interrupt, heal, movetype
    def takedamage(self, damagetaken, healingtaken):
        if self.playerhp <=13:
            self.playerhp = (self.playerhp) + healingtaken - damagetaken
            return self.playerhp
        else:
            self.playerhp = 15 - damagetaken
            return self.playerhp
    def doturn(self, yourmove, opponentmove, opponentdamage, stopheal):
        if yourmove == "strike" or yourmove == 1:
            heal = 0
            stun = False
            parrystun = False
            if opponentmove == "strike" or opponentmove == "kick":
                damage = 2
                return damage, heal, stun, parrystun
            elif opponentmove == "dodge":
                damage = 0
                return damage, heal, stun, parrystun
            elif opponentmove == "parry":
                damage = 0
                return damage, heal, stun, parrystun
            elif opponentmove == "heal":
                damage = 2
                interrupt = True
                return damage, heal, stun, parrystun
            else:
                damage = 2
                interrupt = True
                return damage, heal, stun, parrystun
        if yourmove == "kick" or yourmove == 2:
            heal = 0
            stun = False
            parrystun = False
            if opponentmove == "strike" or opponentmove == "kick" or opponentmove == "heal":
                damage = 1
                return damage, heal, stun, parrystun
            elif opponentmove == "dodge":
                damage = 3
                return damage, heal, stun, parrystun
            elif opponentmove == "parry":
                damage = 0
                return damage, heal, stun, parrystun
            else:
                damage = 1
                return damage, heal, stun, parrystun
        if yourmove == "dodge" or yourmove == 3:
            heal = 0
            damage = 0
            stun = False
            parrystun = False
            if opponentmove == "strike":
                stun = True
                return damage, heal, stun, parrystun
            elif opponentmove == "dodge" or opponentmove == "heal" or opponentmove == "kick":
                return damage, heal, stun, parrystun
            elif opponentmove == "parry":
                stun = True
                parrystun = True
                return damage, heal, stun, parrystun
            else:
                return damage, heal, stun, parrystun
        if yourmove == "parry" or yourmove == 4:
            heal = 0
            stun = False
            parrystun = False
            if opponentmove == "strike" or opponentmove == "kick":
                damage = opponentdamage+2
                return damage, heal, stun, parrystun
            elif opponentmove == "dodge" or opponentmove == "parry" or opponentmove == "heal":
                damage = 0
                return damage, heal, stun, parrystun
            else:
                damage = 0
                return damage, heal, stun, parrystun
        if yourmove == "heal" or yourmove == 5:
            damage = 0
            stun = False
            parrystun = False
            if stopheal == True:
                heal = 0
                return damage, heal, stun, parrystun
            else:
                heal = 2
                return damage, heal, stun, parrystun
        else:
            damage = 0
            heal = 0
            stun = False
            parrystun = False
            return damage, heal, stun, parrystun
    
class Samurai(Character):
    def __init__(self, playerhp):
        self.playerhp = playerhp
     def help(self):
        print("MOVES: \n Slash - Deals 2 damage, deals 3 damage if you take damage on the same turn, interrupts Heal (STRIKE type)\n Kick - Deals 1 damage, deals 3 damage against Dodge (KICK type)\nShoulder Bash - Counters Parry and Heal. Causes Parry to miss, granting an extra turn and +2 damage to any attacks done during said turn (DODGE type)\n Parry - Counters any attacks, returning the attack with an extra +2 damage (PARRY type)\n Heal - Heals for 2 HP (HEAL type)")
    def moveinfo(self, move):
        if move == "strike":
            damage = 2
            interrupt = True
            heal = 0
            movetype = "striketype"
            return damage, interrupt, heal, movetype
        if move == "kick":
            damage = 1
            interrupt = False
            heal = 0
            movetype = "kicktype"
            return damage, interrupt, heal, movetype
        if move == "dodge":
            damage = 0
            interrupt = True
            heal = 0
            movetype = "dodgetype"
            return damage, interrupt, heal, movetype
        if move == "parry":
            damage = 0
            interrupt = False
            heal = 0
            movetype = "parrytype"
            return damage, interrupt, heal, movetype
        else:
            damage = 0
            interrupt = False
            heal = 0
            movetype = "nothing"
            return damage, interrupt, heal, movetype
    def takedamage(self, damagetaken, healingtaken):
        if self.playerhp <=13:
            self.playerhp = (self.playerhp) + healingtaken - damagetaken
            return self.playerhp
        else:
            self.playerhp = 15 - damagetaken
            return self.playerhp
    def doturn(self, yourmove, opponentmove, opponentdamage, stopheal):
        if yourmove == "strike" or yourmove == 1:
            heal = 0
            stun = False
            parrystun = False
            if opponentdamage >= 1:
                damage = 3
                return damage, heal, stun, parrystun
            elif opponentmove == "dodge":
                damage = 0
                return damage, heal, stun, parrystun
            elif opponentmove == "parry":
                damage = 0
                return damage, heal, stun, parrystun
            elif opponentmove == "heal":
                damage = 2
                interrupt = True
                return damage, heal, stun, parrystun
            else:
                damage = 2
                interrupt = True
                return damage, heal, stun, parrystun
        if yourmove == "kick" or yourmove == 2:
            heal = 0
            stun = False
            parrystun = False
            if opponentmove == "strike" or opponentmove == "kick" or opponentmove == "heal":
                damage = 1
                return damage, heal, stun, parrystun
            elif opponentmove == "dodge":
                damage = 3
                return damage, heal, stun, parrystun
            elif opponentmove == "parry":
                damage = 0
                return damage, heal, stun, parrystun
            else:
                damage = 1
                return damage, heal, stun, parrystun
        if yourmove == "dodge" or yourmove == 3 or yourmove == "shoulder bash":
            heal = 0
            damage = 0
            stun = False
            parrystun = False
            if opponentmove == "strike":
                heal = -opponentdamage
                return damage, heal, stun, parrystun
            elif opponentmove == "dodge" or opponentmove == "kick":
                return damage, heal, stun, parrystun
            elif opponentmove == "parry":
                stun = True
                parrystun = True
                return damage, heal, stun, parrystun
            elif opponentmove == "heal":
                damage = 1
                return damage, heal, stun, parrystun
            else:
                return damage, heal, stun, parrystun
        if yourmove == "parry" or yourmove == 4:
            heal = 0
            stun = False
            parrystun = False
            if opponentmove == "strike" or opponentmove == "kick":
                damage = opponentdamage+2
                heal = 1
                return damage, heal, stun, parrystun
            elif opponentmove == "dodge" or opponentmove == "parry" or opponentmove == "heal":
                damage = 0
                return damage, heal, stun, parrystun
            else:
                damage = 0
                return damage, heal, stun, parrystun
        else:
            damage = 0
            heal = 0
            stun = False
            parrystun = False
            return damage, heal, stun, parrystun

class Mage(Character):
    def __init__(self, playerhp, doubling, defense_magic):
        self.playerhp = playerhp
        self.doubling = doubling
        self.defense_magic = defense_magic
    def moveinfo(self, move):
        if move == "strike":
            damage = 1
            interrupt = True
            heal = 0
            movetype = "striketype"
            return damage, interrupt, heal, movetype
        if move == "kick":
            damage = 0
            interrupt = False
            heal = 0
            movetype = "kicktype"
            return damage, interrupt, heal, movetype
        if move == "dodge":
            damage = 0
            interrupt = False
            heal = 0
            movetype = "dodgetype"
            return damage, interrupt, heal, movetype
        if move == "parry":
            damage = 0
            interrupt = False
            heal = 0
            movetype = "parrytype"
            return damage, interrupt, heal, movetype
        if move == "heal":
            damage = 0
            interrupt = False
            heal = 3
            movetype = "healtype"
            return damage, interrupt, heal, movetype
        else:
            damage = 0
            interrupt = False
            heal = 0
            movetype = "nothing"
            return damage, interrupt, heal, movetype
    def takedamage(self, damagetaken, healingtaken):
        if self.playerhp <=13:
            if self.defense_magic == True:
                self.playerhp = (self.playerhp) + healingtaken - (damagetaken - 1)
                if damagetaken >= 1:
                    self.defense_magic = False
                return self.playerhp
            else:
                self.playerhp = (self.playerhp) + healingtaken - damagetaken
                return self.playerhp
        else:
            if self.defense_magic == True:
                self.playerhp = 15 - (damagetaken - 1)
                if damagetaken >= 1:
                    self.defense_magic = False
                return self.playerhp
            else:
                self.playerhp = 15 - damagetaken
                return 
    def doturn(self, yourmove, opponentmove, opponentdamage, stopheal):
        if yourmove == "strike" or yourmove == 1:
            heal = 0
            stun = False
            parrystun = False
            if opponentmove == "strike" or opponentmove == "kick":
                if self.doubling == False:
                    damage = 1
                    return damage, heal, stun, parrystun
                else:
                    damage = 3
                    self.doubling = False
                    return damage, heal, stun, parrystun
            elif opponentmove == "dodge":
                damage = 0
                return damage, heal, stun, parrystun
            elif opponentmove == "parry":
                damage = 0
                return damage, heal, stun, parrystun
            elif opponentmove == "heal":
                if self.doubling == False:
                    damage = 1
                    interrupt = True
                    return damage, heal, stun, parrystun
                else:
                    damage = 3
                    interrupt = True
                    self.doubling = False
                    return damage, heal, stun, parrystun
            else:
                damage = 1
                interrupt = True
                return damage, heal, stun, parrystun
        if yourmove == "kick" or yourmove == 2:
            heal = 0
            stun = False
            parrystun = False
            if opponentmove == "strike" or opponentmove == "kick" or opponentmove == "heal":
                if self.doubling == False:
                    damage = 0
                    return damage, heal, stun, parrystun
                else:
                    damage = 1
                    stun = True
                    self.doubling = False
                    return damage, heal, stun, parrystun
            elif opponentmove == "dodge":
                if self.doubling == False:
                    damage = 1
                    stun = True
                    return damage, heal, stun, parrystun
                else:
                    damage = 2
                    stun = True
                    self.doubling = False
                    return damage, heal, stun, parrystun
            elif opponentmove == "parry":
                damage = 0
                return damage, heal, stun, parrystun
            else:
                if self.doubling == False:
                    damage = 0
                    return damage, heal, stun, parrystun
                else:
                    damage = 1
                    stun = True
                    self.doubling = False
                    return damage, heal, stun, parrystun
        if yourmove == "dodge" or yourmove == 3:
            heal = 0
            damage = 0
            stun = False
            parrystun = False
            self.doubling = True
            if opponentmove == "strike":
                stun = True
                self.doubling = False
                return damage, heal, stun, parrystun
            if opponentmove == "kick":
                self.doubling = False
                heal = -1
            elif opponentmove == "dodge" or opponentmove == "heal":
                return damage, heal, stun, parrystun
            elif opponentmove == "parry":
                stun = True
                parrystun = True
                return damage, heal, stun, parrystun
            else:
                return damage, heal, stun, parrystun
        if yourmove == "parry" or yourmove == 4:
            heal = 0
            stun = False
            parrystun = False
            self.defense_magic = True
            if opponentmove == "strike" or opponentmove == "kick":
                if self.doubling == False:
                    damage = opponentdamage
                    return damage, heal, stun, parrystun
                else:
                    damage = opponentdamage+2
                    self.doubling = False
                    return damage, heal, stun, parrystun
            elif opponentmove == "dodge" or opponentmove == "parry" or opponentmove == "heal":
                damage = 0
                return damage, heal, stun, parrystun
            else:
                damage = 0
                return damage, heal, stun, parrystun
        if yourmove == "heal" or yourmove == 5:
            damage = 0
            stun = False
            parrystun = False
            if stopheal == True:
                heal = 0
                return damage, heal, stun, parrystun
            else:
                if self.doubling == False:
                    heal = 3
                    return damage, heal, stun, parrystun
                else:
                    if opponentmove == "strike":
                        heal = 3
                        self.doubling = False
                        return damage, heal, stun, parrystun
                    else:
                        heal = 4
                        self.doubling = False
                        return damage, heal, stun, parrystun
        #PLEASE OPTIMIZE THIS LATER. THERE MUST BE A BETTER WAY TO DO THIS (note to self)
        else:
            damage = 0
            heal = 0
            stun = False
            parrystun = False
            return damage, heal, stun, parrystun




#while loops for selecting characters at the start of the game
while selecting1 == True:
    whichcharacter1 = input("---------- PLAYER 1 : SELECT CHARACTER ----------\nKNIGHT\nSAMURAI\nMAGE\nCOWBOY\nPIRATE\nNINJA\nASTRONAUT\nCOPYCAT\n ")
    if whichcharacter1 == "knight":
        c1 = Knight(HP1)
        selecting1 = False
    elif whichcharacter1 == "samurai":
        c1 = Samurai(HP1)
        selecting1 = False
    elif whichcharacter1 == "mage":
        c1 = Mage(HP1, doubling)
        selecting1 = False

while selecting2 == True:
    whichcharacter2 = input("---------- PLAYER 2 : SELECT CHARACTER ----------\nKNIGHT\nSAMURAI\nMAGE\nCOWBOY\nPIRATE\nNINJA\nASTRONAUT\nCOPYCAT\n ")
    if whichcharacter2 == "knight":
        c2 = Knight(HP2)
        selecting2 = False
    if whichcharacter2 == "samurai":
        c2 = Samurai(HP2)
        selecting2 = False
    if whichcharacter2 == "mage":
        c2 = Mage(HP2, doubling)
        selecting2 = False

#function to clear the console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')





#function for determining how turns play out
def turn(firstmove, secondmove, character1, character2, health1, health2, punishvalue1, punishvalue2):
    punishvalue1 -= 1
    punishvalue2 -= 1
    damageamount1, checkinterrupt1, healamount1, movetype1 = character1.moveinfo(firstmove)
    damageamount2, checkinterrupt2, healamount2, movetype2 = character2.moveinfo(secondmove)
    damage1, heal1, stun2, failparry2 = character1.doturn(firstmove, secondmove, damageamount2, checkinterrupt2)
    damage2, heal2, stun1, failparry1 = character2.doturn(secondmove, firstmove, damageamount1, checkinterrupt1)
    
    
    if punishvalue1 >= 1:
        damage2 += 2
        punishvalue1 = 0
    if punishvalue2 >= 1:
        damage1 +=2
        punishvalue2 = 0
    if failparry1 == True:
        punishvalue1+=2
    if failparry2 == True:
        punishvalue2+=2

    
    health1 = character1.takedamage(damage2, heal1)
    health2 = character2.takedamage(damage1, heal2)
    

    

    if stun1 == True:
        print("Player 1 is vulnerable!")
    if stun2 == True:
        print("Player 2 is vulnerable!")
    print(f"Player 1 used {firstmove} and did {damage1} damage")
    print(f"Player 2 used {secondmove} and did {damage2} damage")
    print(f"Player 1 HP: {health1}\nPlayer 2 HP: {health2}")
    punishvalue1+=1
    punishvalue2+=1
    return health1, health2, stun1, stun2, punishvalue1, punishvalue2

    


#while loop that lasts until the game ends
while gameend == False:
    moveselect = True
    while moveselect == True:
        if playerstun1 == False:
            move1 = input("Player 1, it is your turn. What would you like to do? (type 'help' for a list of commands/moves!)  ")
            if move1 in Moves:
                os.system('cls' if os.name == 'nt' else 'clear')
                moveselect = False
            elif move1 == "help":
                c1.help()
            else:
                print("Sorry, that is not a valid move.")
        else:
            move1 = "stunned"
            moveselect = False
    moveselect = True
    while moveselect == True:
        if playerstun2 == False:
            move2 = input("Player 2, it is your turn. What would you like to do? (type 'help' for a list of commands/moves!)  ")
            if move2 in Moves:
                os.system('cls' if os.name == 'nt' else 'clear')
                moveselect = False
            elif move2 == "help":
                c1.help()
            else:
                print("Sorry, that is not a valid move.")
        else:
            move2 = "stunned"
            moveselect = False
    HP1, HP2, playerstun1, playerstun2, punish1, punish2 = turn(move1, move2, c1, c2, HP1, HP2, punish1, punish2)

    if HP1 <= 0 and HP2 > 0:
        print("Player 2 wins!!")
        gameend = True
    elif HP1 > 0 and HP2 <= 0:
        print("Player 1 wins!!")
        gameend = True
    elif HP1 <= 0 and HP2 <= 0:
        print("No one wins, you both suck")
    else:
        gameend = False