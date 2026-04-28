#importing necessary tools
import pandas as pd
import matplotlib as plt
import pytest
import os
import random
from git import Repo

#initializing variables
moveselect = True
playerstun1 = False
playerstun2 = False
punish1 = 0
punish2 = 0
gameend =False
selecting1 = True
selecting2 = True
overhealing1 = False
overhealing2 = False
interrupting1 = False
interrupting2 = False
delaying_heal1 = False
delaying_heal2 = False
bulwark1 = 0
bulwark2 = 0
demonic_rage1 = 0
demonic_rage2 = 0
doubling1 = False
doubling2 = False
defensive_magic1 = False
defensive_magic2 = False
pirate_counter1 = True
pirate_counter2 = True
elusive1 = 0
elusive2 = 0
elusive_decay1 = 0
elusive_decay2 = 0
float1 = False
float2 = False
jetpack1 = False
jetpack2 = False
float_decay1 = 3
float_decay2 = 3
no_float1 = False
no_float2 = False
boating1 = False
boating2 = False
Moves = ["nothing", "strike", "kick", "dodge", "parry", "heal"] #PLACEHOLDER, PLEASE IMPLEMENT SOMETHING BETTER
Characters = ["Knight", "Samurai", "Mage", "Cowboy", "Pirate", "Ninja", "Astronaut", "Copycat"] #I don't really know if I need this but never hurts to keep around jusssttt in case :)
HP1 = 15
HP2 = 15



#creating classes for characters
class Character:
    def __init__(self, name):
        self.name = name

class Knight(Character):
    def __init__(self, playerhp, undying):
        self.playerhp = playerhp
        self.undying = undying
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
            self.playerhp = (self.playerhp) + healingtaken - damagetaken
            if self.playerhp <= 0:
                if self.undying == 0:
                    bulwark = 1
                    if bulwark == 1:
                        self.playerhp = 1
                        self.undying+=1
                        print("Knight held out a little longer!")
                elif self.undying == 1:
                    bulwark = random.randint(0, 2)
                    if bulwark == 2:
                        self.playerhp = 1
                        self.undying+=1
                        print("Knight held out a little longer!")
                elif self.undying == 2:
                    bulwark = random.randint(0, 4)
                    if bulwark == 4:
                        self.playerhp = 1
                        self.undying+=1
                        print("Knight held out a little longer!")
                elif self.undying >= 3:
                    bulwark = random.randint(0, 10)
                    if bulwark == 10:
                        self.playerhp = 1
                        self.undying+=1
                        print("Knight held out a little longer!")
                        
            return self.playerhp
    def resetoverheal(self):
        overheal = False
        if self.playerhp > 15:
            self.playerhp = 15
            overheal = True
        return overheal
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
    def __init__(self, playerhp, rage):
        self.playerhp = playerhp
        self.rage = rage
    def help(self):
        print("MOVES: \n Slash - Deals 2 damage, deals 3 damage if you take damage on the same turn, interrupts Heal (STRIKE type)\n Kick - Deals 1 damage, deals 3 damage against Dodge (KICK type)\nShoulder Bash - Counters Parry and Heal. Breaks through Parry, granting an extra turn and +2 damage to any attacks done during said turn. Interrupts and deals 1 damage against Heal (DODGE type)\n Warrior's Parry - Counters any attacks, returning the attack with an extra +2 damage and healing for 1 HP (PARRY type)")
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
            self.playerhp = (self.playerhp) + healingtaken - damagetaken
            return self.playerhp
    def resetoverheal(self):
        overheal = False
        if self.playerhp > 15:
            self.playerhp = 15
            overheal = True
        return overheal
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
                stun = True
                return damage, heal, stun, parrystun
            else:
                return damage, heal, stun, parrystun
        elif yourmove == "parry" or yourmove == 4:
            heal = 0
            stun = False
            parrystun = False
            if opponentmove == "strike" or opponentmove == "kick":
                damage = opponentdamage+2
                heal = 2
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
            self.rage += 1
            return damage, heal, stun, parrystun

class Mage(Character):
    def __init__(self, playerhp, doubling, defense_magic):
        self.playerhp = playerhp
        self.doubling = doubling
        self.defense_magic = defense_magic
    def help(self):
        print("MOVES: \n Staff Stike - Deals 1 damage, deals 3 damage when Doubled, interrupts Heal (STRIKE type)\n Vine Grab - Deals 0 damage, deals 1 damage and stuns when catching dodge, allowing for a free turn. Deals an extra +1 damage when doubled (KICK type)\n Clone - Sets up a clone in your place, granting the Doubling effect to your next action. Counters Strike and Parry. Causes strike to hit your clone instead, removing the Doubling effect but granting an extra turn, as well as causing Parry to miss, granting an extra turn and +2 damage to any attacks done during said turn. Take +1 damage when getting hit by Kick (DODGE type)\n Arcane Barrier - Counters any attacks, returning the attack with no extra damage(+2 extra when Doubled), as well as reducing the next damage you take by -1 (PARRY type)\n Heal Spell - Heals for 3 HP (4 HP when Doubled)")
    def moveinfo(self, move):
        if move == "strike":
            damage = 1
            interrupt = True
            heal = 99
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
            if self.defense_magic == True:
                if damagetaken>=1:
                    self.playerhp = (self.playerhp) + healingtaken - (damagetaken - 1)
                    self.defense_magic = False
                    return self.playerhp
                else:
                    self.playerhp = (self.playerhp) + healingtaken - damagetaken
                    return self.playerhp
            else:
                self.playerhp = (self.playerhp) + healingtaken - damagetaken
                return self.playerhp
    def resetoverheal(self):
        overheal = False
        if self.playerhp > 15:
            self.playerhp = 15
            overheal = True
        return overheal
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
                if self.doubling == True:
                    self.doubling = False
                damage = 0
                return damage, heal, stun, parrystun
            elif opponentmove == "parry":
                if self.doubling == True:
                    self.doubling = False
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
                if self.doubling == True:
                    self.doubling = False
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
                if self.doubling == True:
                    self.doubling = False
                damage = 0
                return damage, heal, stun, parrystun
            else:
                damage = 0
                if self.doubling == True:
                    self.doubling = False
                return damage, heal, stun, parrystun
        if yourmove == "heal" or yourmove == 5:
            damage = 0
            stun = False
            parrystun = False
            if stopheal == True:
                heal = 0
                if self.doubling == True:
                    self.doubling = False
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

class Cowboy(Character):
    def __init__(self, playerhp, delayed_heal):
        self.playerhp = playerhp
        self.delayed_heal = delayed_heal
    def help(self):
        print("MOVES: \n Strike - Deals 2 damage, interrupts Heal (STRIKE type)\n Kick - Deals 1 damage, deals 3 damage against Dodge (KICK type)\nDodge - Counters Strike and Parry. Causes Strike to miss, granting an extra turn if dodged. Causes Parry to miss, granting an extra turn and +2 damage to any attacks done during said turn (DODGE type)\n Parry - Counters any attacks, returning the attack with an extra +2 damage (PARRY type)\n Heal - Heals for 2 HP (HEAL type)")
    def moveinfo(self, move):
        if move == "strike":
            damage = 2
            interrupt = False
            heal = 0
            movetype = "striketype"
            return damage, interrupt, heal, movetype
        if move == "kick":
            damage = 1
            interrupt = True
            heal = 0
            movetype = "kicktype"
            return damage, interrupt, heal, movetype
        if move == "dodge":
            damage = 1
            interrupt = False
            heal = 0
            movetype = "dodgetype"
            return damage, interrupt, heal, movetype
        if move == "parry":
            damage = 1
            interrupt = False
            heal = 0
            movetype = "parrytype"
            return damage, interrupt, heal, movetype
        if move == "heal":
            damage = 1
            interrupt = False
            heal = 0
            movetype = "healtype"
            return damage, interrupt, heal, movetype
        else:
            damage = 0
            interrupt = False
            heal = 0
            movetype = "nothing"
            return damage, interrupt, heal, movetype
    def takedamage(self, damagetaken, healingtaken):
            self.playerhp = (self.playerhp) + healingtaken - damagetaken
            return self.playerhp
    def resetoverheal(self):
        overheal = False
        if self.playerhp > 15:
            self.playerhp = 15
            overheal = True
        return overheal
    def doturn(self, yourmove, opponentmove, opponentdamage, stopheal):
        if stopheal == True:
            if opponentmove == "strike" and (yourmove == "dodge" or yourmove == "parry"):
                stopheal = False
            elif opponentmove == "kick" and yourmove == "parry":
                stopheal = False
            elif opponentmove == "dodge" and (yourmove == "strike" or yourmove == "kick" or yourmove == "dodge"):
                stopheal = False
        if self.delayed_heal == True:
            if stopheal == False:
                heal = 2
                self.delayed_heal = False
            else:
                heal = 0
                self.delayed_heal = False
        else:
            heal = 0
        if yourmove == "strike" or yourmove == 1:
            stun = False
            parrystun = False
            if opponentmove == "strike":
                damage = 2
                return damage, heal, stun, parrystun
            elif opponentmove == "kick":
                damage = 2
                heal += 1
                return damage, heal, stun, parrystun
            elif opponentmove == "dodge":
                damage = 0
                return damage, heal, stun, parrystun
            elif opponentmove == "parry":
                damage = 0
                heal += -1
                return damage, heal, stun, parrystun
            elif opponentmove == "heal":
                damage = 2
                interrupt = True
                return damage, heal, stun, parrystun
            else:
                damage = 2
                interrupt = False
                return damage, heal, stun, parrystun
        if yourmove == "kick" or yourmove == 2:
            stun = False
            parrystun = False
            if opponentmove == "strike" or opponentmove == "kick" or opponentmove == "heal":
                damage = 1
                interrupt = True
                return damage, heal, stun, parrystun
            elif opponentmove == "dodge":
                damage = 2
                return damage, heal, stun, parrystun
            elif opponentmove == "parry":
                damage = 0
                heal += -1
                return damage, heal, stun, parrystun
            else:
                damage = 1
                return damage, heal, stun, parrystun
        if yourmove == "dodge" or yourmove == 3:
            damage = 1
            stun = False
            parrystun = False
            if opponentmove == "strike":
                stun = True
                return damage, heal, stun, parrystun
            elif opponentmove == "dodge" or opponentmove == "heal" or opponentmove == "kick":
                return damage, heal, stun, parrystun
            elif opponentmove == "parry":
                stun = True
                parrystun = False
                return damage, heal, stun, parrystun
            else:
                return damage, heal, stun, parrystun
        if yourmove == "parry" or yourmove == 4:
            damage = 1
            stun = False
            parrystun = False
            if opponentmove == "strike" or opponentmove == "kick":
                damage = 2
                return damage, heal, stun, parrystun
            elif opponentmove == "dodge": 
                damage = 0
                return damage, heal, stun, parrystun
            elif opponentmove == "parry" or opponentmove == "heal":
                return damage, heal, stun, parrystun
            else:
                damage = 1
                return damage, heal, stun, parrystun
        if yourmove == "heal" or yourmove == 5:
            self.delayed_heal = True
            if opponentmove != "dodge":
                damage = 1
            else:
                damage = 0
            stun = False
            parrystun = False
            if stopheal == True:
                self.delayed_heal = False
                return damage, heal, stun, parrystun
            else:
                self.delayed_heal = True
                return damage, heal, stun, parrystun
        else:
            damage = 0
            heal += random.randint(-1,1)
            stun = False
            parrystun = False
            if heal == 1:
                print("Cowboy got lucky with his Pocket Tonic! Healed 1 HP")
            return damage, heal, stun, parrystun

class Pirate(Character):
    def __init__(self, playerhp, counter):
        self.playerhp = playerhp
        self.counter = counter
    def help(self):
        print("MOVES: \n Sabre - Deals 2 damage, if your opponent also used Strike, reduce the damage of said Strike by 1. Deals 3 damage against Heal (STRIKE type)\n Peg Leg - Deals 1 damage, deals 2 damage against Dodge and 3 damage against Kick (KICK type)\n All Hands on Deck - Counters Strike, Parry, and Dodge. Causes Strike and Parry to miss, granting an extra turn. If your opponent also used Dodge, stun them and get an extra turn (DODGE type)\n Hook - Counters any attacks, returning the attack with an extra +1 damage. If your opponent also used Parry, deal 3 damage to them (PARRY type)\n Rum - Heals for 1 HP, cannot be interrupted. Throws a bottle that interrupts Heal. (HEAL type)")
    def moveinfo(self, move):
        if move == "strike":
            damage = 2
            interrupt = False
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
            interrupt = True
            heal = 1                                                       
            movetype = "healtype"
            return damage, interrupt, heal, movetype
        else:
            damage = 0
            interrupt = False
            heal = 0
            movetype = "nothing"
            return damage, interrupt, heal, movetype
    def takedamage(self, damagetaken, healingtaken):
            if self.counter == False:
                self.playerhp = (self.playerhp) + healingtaken - damagetaken
                return self.playerhp
            else:
                if damagetaken >=1:
                    self.playerhp = (self.playerhp) + healingtaken - (damagetaken-1)
                    self.counter = False
                    return self.playerhp
                else:
                    self.playerhp = (self.playerhp) + healingtaken - damagetaken
                    self.counter = False
                    return self.playerhp
    def resetoverheal(self):
        overheal = False
        if self.playerhp > 15:
            self.playerhp = 15
            overheal = True
        return overheal
    def doturn(self, yourmove, opponentmove, opponentdamage, stopheal):
        if yourmove == "strike" or yourmove == 1:
            heal = 0
            stun = False
            parrystun = False
            if opponentmove == "strike":
                damage = 2
                self.counter = True
                return damage, heal, stun, parrystun
            elif opponentmove == "dodge":
                damage = 0
                return damage, heal, stun, parrystun
            elif opponentmove == "parry":
                damage = 0
                return damage, heal, stun, parrystun
            elif opponentmove == "heal":
                damage = 3
                return damage, heal, stun, parrystun
            else:
                damage = 2
                return damage, heal, stun, parrystun
        if yourmove == "kick" or yourmove == 2:
            heal = 0
            stun = False
            parrystun = False
            if opponentmove == "strike":
                damage = 1
                return damage, heal, stun, parrystun
            elif opponentmove == "kick":
                damage = 3
                return damage, heal, stun, parrystun
            elif opponentmove == "dodge":
                damage = 2
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
            elif opponentmove == "dodge":
                stun = True
                return damage, heal, stun, parrystun
            elif opponentmove == "heal" or opponentmove == "kick":
                return damage, heal, stun, parrystun
            elif opponentmove == "parry":
                stun = True
                return damage, heal, stun, parrystun
            else:
                return damage, heal, stun, parrystun
        if yourmove == "parry" or yourmove == 4:
            heal = 0
            stun = False
            parrystun = False
            if opponentmove == "strike" or opponentmove == "kick":
                damage = opponentdamage+1
                return damage, heal, stun, parrystun
            elif opponentmove == "dodge" or opponentmove == "heal":
                damage = 0
                return damage, heal, stun, parrystun
            elif opponentmove == "parry":
                damage = 3
                return damage, heal, stun, parrystun
            else:
                damage = 0
                return damage, heal, stun, parrystun
        if yourmove == "heal" or yourmove == 5:
            damage = 0
            stun = False
            parrystun = False
            heal = 1
            return damage, heal, stun, parrystun
        else:
            damage = 0
            heal = 0
            stun = False
            parrystun = False
            return damage, heal, stun, parrystun

class Ninja(Character):
    def __init__(self, playerhp, evasion, delayed_heal, evasion_decay):
        self.playerhp = playerhp
        self.evasion = evasion
        self.delayed_heal = delayed_heal
        self.evasion_decay = evasion_decay
    def help(self):
        print("MOVES: \n Strike - Deals 2 damage, interrupts Heal (STRIKE type)\n Kick - Deals 1 damage, deals 3 damage against Dodge (KICK type)\nDodge - Counters Strike and Parry. Causes Strike to miss, granting an extra turn if dodged. Causes Parry to miss, granting an extra turn and +2 damage to any attacks done during said turn (DODGE type)\n Parry - Counters any attacks, returning the attack with an extra +2 damage (PARRY type)\n Heal - Heals for 2 HP (HEAL type)")
    def moveinfo(self, move):
        if move == "strike":
            damage = 2
            interrupt = False
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
            heal = 1
            movetype = "healtype"
            return damage, interrupt, heal, movetype
        else:
            damage = 0
            interrupt = False
            heal = 0
            movetype = "nothing"
            return damage, interrupt, heal, movetype
    def takedamage(self, damagetaken, healingtaken):
        if self.evasion <= damagetaken:
                self.playerhp = (self.playerhp) + healingtaken - (damagetaken - self.evasion)
                self.evasion = 0
        elif self.evasion > damagetaken:
                self.evasion -= damagetaken
                self.playerhp = (self.playerhp) + healingtaken - 0
        return self.playerhp
    def resetoverheal(self):
        overheal = False
        if self.playerhp > 15:
            self.playerhp = 15
            overheal = True
        return overheal
    def doturn(self, yourmove, opponentmove, opponentdamage, stopheal):
        if self.evasion >1:
            self.evasion_decay +=1
            if self.evasion_decay >= 2:
                self.evasion -= 1
        else:
            self.evasion_decay = 0
        if stopheal == True:
            if opponentmove == "strike" and (yourmove == "dodge" or yourmove == "parry"):
                stopheal = False
            elif opponentmove == "kick" and yourmove == "parry":
                stopheal = False
            elif opponentmove == "dodge" and (yourmove == "strike" or yourmove == "kick" or yourmove == "dodge"):
                stopheal = False
        if self.delayed_heal == True:
            if stopheal == False:
                heal = 1
                self.delayed_heal = False
            else:
                heal = 0
                self.delayed_heal = False
        else:
            heal = 0
        if yourmove == "strike" or yourmove == 1:
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
                damage = 3
                return damage, heal, stun, parrystun
            else:
                damage = 2
                interrupt = True
                return damage, heal, stun, parrystun
        if yourmove == "kick" or yourmove == 2:
            stun = False
            parrystun = False
            if opponentmove == "strike" or opponentmove == "kick" or opponentmove == "heal":
                damage = 0
                return damage, heal, stun, parrystun
            elif opponentmove == "dodge":
                damage = 3
                if self.evasion < 3:
                    self.evasion += 1
                else:
                    self.evasion = 3
                return damage, heal, stun, parrystun
            elif opponentmove == "parry":
                damage = 0
                return damage, heal, stun, parrystun
            else:
                damage = 0
                return damage, heal, stun, parrystun
        if yourmove == "dodge" or yourmove == 3:
            damage = 0
            stun = False
            parrystun = False
            if opponentmove == "strike":
                stun = True
                if self.evasion < 3:
                    self.evasion+=1
                else:
                    self.evasion = 3
                return damage, heal, stun, parrystun
            elif opponentmove == "kick":
                return damage, heal, stun, parrystun
            elif opponentmove == "dodge" or opponentmove == "heal":
                if self.evasion < 3:
                    self.evasion+=1
                else:
                    self.evasion = 3
                return damage, heal, stun, parrystun
            elif opponentmove == "parry":
                if self.evasion < 3:
                    self.evasion+=1
                else:
                    self.evasion = 3
                stun = True
                parrystun = True
                return damage, heal, stun, parrystun
            else:
                return damage, heal, stun, parrystun
        if yourmove == "parry" or yourmove == 4:
            stun = False
            parrystun = False
            if opponentmove == "strike" or opponentmove == "kick":
                damage = 2
                if self.evasion <= 1:
                    self.evasion += 2
                elif self.evasion == 2:
                    self.evasion += 1
                else:
                    self.evasion = 3
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
                return damage, heal, stun, parrystun
            else:
                self.delayed_heal = True
                if self.evasion < 3:
                    self.evasion += 1
                else:
                    self.evasion = 3
                return damage, heal, stun, parrystun
        else:
            damage = 0
            heal = 0
            stun = False
            parrystun = False
            return damage, heal, stun, parrystun

class Astronaut(Character):
    def __init__(self, playerhp, delayed_heal, floating, boost_counter, float_timer, block_float, float_firstturn):
        self.playerhp = playerhp
        self.delayed_heal = delayed_heal
        self.floating = floating
        self.boost_counter = boost_counter
        self.float_timer = float_timer
        self.block_float = block_float
        self.float_firstturn = float_firstturn
    def help(self):
        print("MOVES: \n Strike - Deals 2 damage, interrupts Heal (STRIKE type)\n Kick - Deals 1 damage, deals 3 damage against Dodge (KICK type)\nDodge - Counters Strike and Parry. Causes Strike to miss, granting an extra turn if dodged. Causes Parry to miss, granting an extra turn and +2 damage to any attacks done during said turn (DODGE type)\n Parry - Counters any attacks, returning the attack with an extra +2 damage (PARRY type)\n Heal - Heals for 2 HP (HEAL type)")
    def moveinfo(self, move):
        if move == "strike":
            damage = 2
            if self.floating == True:
                interrupt = True
            else:
                interrupt = False
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
            if self.floating == True:
                heal = 1
            else:
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
            if self.floating == True:
                heal = 2
            else:
                heal = 1
            movetype = "healtype"
            return damage, interrupt, heal, movetype
        else:
            damage = 0
            interrupt = False
            heal = 0
            movetype = "nothing"
            return damage, interrupt, heal, movetype
    def takedamage(self, damagetaken, healingtaken):
        if self.floating == True and self.float_firstturn == False:
            if damagetaken > 2:
                damagetaken = 2
                self.playerhp = (self.playerhp) + healingtaken - damagetaken
            else:
                self.playerhp = (self.playerhp) + healingtaken - damagetaken
        else:
            self.playerhp = (self.playerhp) + healingtaken - damagetaken
        return self.playerhp
    def resetoverheal(self):
        overheal = False
        if self.playerhp > 15:
            self.playerhp = 15
            overheal = True
        return overheal
    def doturn(self, yourmove, opponentmove, opponentdamage, stopheal):
        self.float_firstturn = False
        if self.float_timer == 0:
            self.floating = False
            self.float_timer = 3
        if stopheal == True:
            if opponentmove == "strike" or opponentmove == "heal" and (yourmove == "dodge" or yourmove == "parry"):
                stopheal = False
            elif opponentmove == "kick" and yourmove == "parry":
                stopheal = False
            elif opponentmove == "dodge" and (yourmove == "strike" or yourmove == "kick" or yourmove == "dodge"):
                stopheal = False
        if self.delayed_heal == True:
            if stopheal == False:
                heal = 1
                self.delayed_heal = False
                if self.floating != True:
                    self.floating = True
                    self.float_firstturn = True
                    print("Astronaut is now floating!")
                    self.boost_counter = 0
            else:
                heal = 0
                self.delayed_heal = False
        else:
            heal = 0
        if self.floating == True:
            self.float_timer -= 1
        if yourmove == "strike" or yourmove == 1:
            damage = 0
            stun = False
            parrystun = False
            if self.floating == True:
                if opponentdamage >= 1:
                    damage = 1
                    heal += 1 
            self.boost_counter += 1
            if self.boost_counter >= 2:
                if self.floating != True:
                    print("Astronaut is now floating!")
                    self.floating = True
                    self.float_firstturn = True
                    self.boost_counter = 0
                else:
                    self.floating = False
                self.boost_counter = 0
            if opponentmove == "strike" or opponentmove == "kick":
                damage += 2
                return damage, heal, stun, parrystun
            elif opponentmove == "dodge":
                damage = 0
                return damage, heal, stun, parrystun
            elif opponentmove == "parry":
                damage = 0
                return damage, heal, stun, parrystun
            elif opponentmove == "heal":
                damage += 2
                interrupt = True
                return damage, heal, stun, parrystun
            else:
                damage += 2
                interrupt = False
                return damage, heal, stun, parrystun
        if yourmove == "kick" or yourmove == 2:
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
            damage = 0
            stun = False
            parrystun = False
            if self.floating == True:
                heal += 1
            if opponentmove == "strike":
                stun = True
                if self.floating != True:
                    print("Astronaut is now floating!")
                    self.floating = True
                    self.float_firstturn = True
                    self.boost_counter = 0
                self.boost_counter = 0
                return damage, heal, stun, parrystun
            elif opponentmove == "kick":
                if self.floating == True:
                    heal -= 1
                self.floating = False
                return damage, heal, stun, parrystun
            elif opponentmove == "dodge" or opponentmove == "heal":
                self.boost_counter = 0
                if self.floating != True:
                    self.floating = True
                    self.float_firstturn = True
                    print("Astronaut is now floating!")
                    self.boost_counter = 0
                else:
                    self.floating = False
                return damage, heal, stun, parrystun
            elif opponentmove == "parry":
                stun = True
                parrystun = False
                if self.floating == True:
                    stun = True
                    parrystun = True
                if self.floating != True:
                    self.floating = True
                    self.float_firstturn = True
                    print("Astronaut is now floating!")
                    self.boost_counter = 0
                else:
                    self.floating = False
                
                return damage, heal, stun, parrystun
            else:
                if self.floating != True:
                    self.floating = True
                    self.float_firstturn = True
                    print("Astronaut is now floating!")
                    self.boost_counter = 0
                else:
                    self.floating = False
                return damage, heal, stun, parrystun
        if yourmove == "parry" or yourmove == 4:
            damage = 0
            stun = False
            parrystun = False
            if opponentmove == "strike" or opponentmove == "kick":
                if self.floating == True:
                    damage = opponentdamage+4
                    heal = -1
                    self.float_timer = 0
                    self.floating = False
                    self.boost_counter = 0
                else:
                    damage = opponentdamage+1
                    self.boost_counter += 1
                    if self.boost_counter >= 2:
                        if self.floating != True:
                            self.floating = True
                            self.float_firstturn = True
                            print("Astronaut is now floating!")
                            self.boost_counter = 0
                        else:
                            self.floating = False
                return damage, heal, stun, parrystun
            elif opponentmove == "dodge": 
                damage = 0
                self.floating = False
                return damage, heal, stun, parrystun
            elif opponentmove == "parry" or opponentmove == "heal":
                self.floating = False
                return damage, heal, stun, parrystun
            else:
                damage = 0
                self.floating = False
                return damage, heal, stun, parrystun
        if yourmove == "heal" or yourmove == 5:
            damage = 0
            if self.floating == True:
                heal = 2
                self.floating = False
                self.boost_counter = 0
                self.float_timer = 0
                stun = 0
                parrystun = 0
                return damage, heal, stun, parrystun
            else:
                self.delayed_heal = True
                stun = False
                parrystun = False
                if stopheal == True:
                    self.delayed_heal = False
                    heal = 0
                    self.floating = False
                    return damage, heal, stun, parrystun
                else:
                    self.delayed_heal = True
                    heal += 1
                    return damage, heal, stun, parrystun
        else:
            damage = 0
            heal = 0
            stun = False
            parrystun = False
            return damage, heal, stun, parrystun

#while loops for selecting characters at the start of the game
while selecting1 == True:
    whichcharacter1 = input("---------- PLAYER 1 : SELECT CHARACTER ----------\nKNIGHT\nSAMURAI\nMAGE\nCOWBOY\nPIRATE\nNINJA\nASTRONAUT\nCOPYCAT\n ")
    if whichcharacter1 == "knight" or whichcharacter1 == "KNIGHT" or whichcharacter1 == "Knight":
        c1 = Knight(HP1, bulwark1)
        selecting1 = False
    elif whichcharacter1 == "samurai" or whichcharacter1 == "SAMURAI" or whichcharacter1 == "Samurai":
        c1 = Samurai(HP1, demonic_rage1)
        selecting1 = False
    elif whichcharacter1 == "mage" or whichcharacter1 == "MAGE" or whichcharacter1 == "Mage":
        c1 = Mage(HP1, doubling1, defensive_magic1)
        selecting1 = False
    elif whichcharacter1 == "pirate" or whichcharacter1 == "PIRATE" or whichcharacter1 == "Pirate":
        c1 = Pirate(HP1, pirate_counter1)
        selecting1 = False
    elif whichcharacter1 == "ninja" or whichcharacter1 == "NINJA" or whichcharacter1 == "Ninja":
        c1 = Ninja(HP1, elusive1, delaying_heal1, elusive_decay1)
        selecting1 = False
    elif whichcharacter1 == "cowboy" or whichcharacter1 == "COWBOY" or whichcharacter1 == "Cowboy":
        c1 = Cowboy(HP1, delaying_heal1)
        selecting1 = False
    elif whichcharacter1 == "astronaut" or whichcharacter1 == "ASTRONAUT" or whichcharacter1 == "Astronaut":
        c1 = Astronaut(HP1, delaying_heal1, float1, jetpack1, float_decay1, no_float1, boating1)
        selecting1 = False
    else:
        print("Sorry, that is not a valid character. Please make sure you typed your character's name correctly before continuing.")

while selecting2 == True:
    whichcharacter2 = input("---------- PLAYER 2 : SELECT CHARACTER ----------\nKNIGHT\nSAMURAI\nMAGE\nCOWBOY\nPIRATE\nNINJA\nASTRONAUT\nCOPYCAT\n ")
    if whichcharacter2 == "knight" or whichcharacter2 == "KNIGHT" or whichcharacter2 == "Knight":
        c2 = Knight(HP2, bulwark2)
        selecting2 = False
    elif whichcharacter2 == "samurai" or whichcharacter2 == "SAMURAI" or whichcharacter2 == "Samurai":
        c2 = Samurai(HP2, demonic_rage2)
        selecting2 = False
    elif whichcharacter2 == "mage" or whichcharacter2 == "MAGE" or whichcharacter2 == "Mage":
        c2 = Mage(HP2, doubling2, defensive_magic2)
        selecting2 = False
    elif whichcharacter2 == "pirate" or whichcharacter2 == "PIRATE" or whichcharacter2 == "Pirate":
        c2 = Pirate(HP2, pirate_counter2)
        selecting2 = False
    elif whichcharacter2 == "ninja" or whichcharacter2 == "NINJA" or whichcharacter2 == "Ninja":
        c2 = Ninja(HP1, elusive2, delaying_heal2, elusive_decay2)
        selecting2 = False
    elif whichcharacter2 == "cowboy" or whichcharacter2 == "COWBOY" or whichcharacter2 == "Cowboy":
        c2 = Cowboy(HP2, delaying_heal2)
        selecting2 = False
    elif whichcharacter2 == "astronaut" or whichcharacter2 == "ASTRONAUT" or whichcharacter2 == "Astronaut":
        c2 = Astronaut(HP2, delaying_heal2, float2, jetpack2, float_decay2, no_float2, boating2)
        selecting2 = False
    else:
        print("Sorry, that is not a valid character. Please make sure you typed your character's name correctly before continuing.")

#function to clear the console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

#function for determining how turns play out
def turn(firstmove, secondmove, character1, character2, health1, health2, punishvalue1, punishvalue2, overheal1, overheal2):
    if overheal1 == True:
        health1 = 15
        overheal1 = False
    if overheal2 == True:
        health2 = 15
        overheal2 = False
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

    
    endinghealth1 = character1.takedamage(damage2, heal1)
    endinghealth2 = character2.takedamage(damage1, heal2)
    overheal1 = character1.resetoverheal()
    overheal2 = character2.resetoverheal()

    healthdifference1 = health1 - endinghealth1
    healthdifference2 = health2 - endinghealth2

    if stun1 == True:
        print("Player 1 is vulnerable!")
    if stun2 == True:
        print("Player 2 is vulnerable!")
    print(f"Player 1 used {firstmove}")
    print(f"Player 2 used {secondmove}")
    if healthdifference1 >= 0:
        print(f"Player 1 took {healthdifference1} damage")
    else:
        print(f"Player 1 healed for {healthdifference1} HP")
    if healthdifference2 >= 0:
        print(f"Player 2 took {healthdifference2} damage")
    else:
        print(f"Player 2 healed for {healthdifference2} HP")
    print(f"Player 1 HP: {endinghealth1}")
    print(f"Player 2 HP: {endinghealth2}")
    punishvalue1+=1
    punishvalue2+=1
    return endinghealth1, endinghealth2, stun1, stun2, punishvalue1, punishvalue2


#while loop that lasts until the game ends
while gameend == False:
    if HP1 >= 15:
        HP1 = 15
    if HP2 >= 15:
        HP2 = 15
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
                c2.help()
            else:
                print("Sorry, that is not a valid move.")
        else:
            move2 = "stunned"
            moveselect = False
    HP1, HP2, playerstun1, playerstun2, punish1, punish2 = turn(move1, move2, c1, c2, HP1, HP2, punish1, punish2, overhealing1, overhealing2)

    if HP1 <= 0 and HP2 > 0:
        print("Player 2 wins!!")
        #df_append_gameresults = pd.DataFrame({'Winning Character': [whichcharacter2], 'Losing Character': [whichcharacter1]})
        gameend = True
    elif HP1 > 0 and HP2 <= 0:
        print("Player 1 wins!!")
        #df_append_gameresults = pd.DataFrame({'Winning Character': [whichcharacter1], 'Losing Character': [whichcharacter2]})
        gameend = True
    elif HP1 <= 0 and HP2 <= 0:
        print("No one wins, you both suck")
    else:
        gameend = False



#df_append_gameresults.to_csv('gameresults.csv', mode='a', index=False, header = False)


#repo_path = 'https://github.com/Rexizcool/Death-Battle-Destruction-REVAMPED'
#repo = Repo(repo_path)
#repo.git.add(update=True)
#repo.index.commit("Added game results")
#origin = repo.remote(name='origin')
#repo.git.push('origin', 'main', force=True) 