playerstun1 = False
playerstun2 = False
punish1 = 0
punish2 = 0
gameend =False
selecting = True
interrupt = False

Moves = ["nothing", "strike", "kick", "dodge", "parry", "heal"]
Characters = ["Knight", "Samurai", "Mage", "Cowboy", "Pirate", "Ninja", "Astronaut"]

HP1 = 15
HP2 = 15

class Character:
    def __init__(self, name):
        self.name = name


class Knight(Character):
    def __init__(self, playerhp):
        self.playerhp = playerhp
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
    
while selecting == True:
    whichcharacter1 = input("Player 1, which character do you want to play? (type 'list' for a list of all characters): ")
    if whichcharacter1 == "knight" or whichcharacter1 == "Knight":
        knight = Knight(HP1)
    elif whichcharacter1 == "samurai" or whichcharacter1 == "Samurai":
        knight = Knight(HP1)
    whichcharacter2 = input("Player 2, which character do you want to play? (type 'list' for a list of all characters): ")
    if whichcharacter2 == "knight" or whichcharacter2 == "Knight":
        knight = Knight(HP2)
        selecting = False







def turn(firstmove, secondmove, character1, character2, health1, health2, punishvalue1, punishvalue2):
    punishvalue1 -= 1
    punishvalue2 -= 1
    damageamount1, checkinterrupt1, healamount1, movetype1 = character1.moveinfo(firstmove)
    damageamount2, checkinterrupt2, healamount2, movetype2 = character2.moveinfo(secondmove)
    damage1, heal1, stun2, failparry2 = character1.doturn(firstmove, secondmove, damageamount2, checkinterrupt2)
    damage2, heal2, stun1, failparry1 = character2.doturn(secondmove, firstmove, damageamount1, checkinterrupt1)
    
    if punishvalue1 >= 1:
        if movetype2 == "striketype" or movetype2 == "kicktype":
            damage2+=2
            health1-=damage2
            punishvalue1 = 0
        else:
            punishvalue1 = 0
    else:
        health1 -= damage2

    if punishvalue2 >= 1:
        if movetype1 == "striketype" or movetype1 == "kicktype":
            damage1+=2
            health2-=damage1
            punishvalue2 = 0
        else:
            punishvalue2 = 0
    else:
        health2 -= damage1

    if failparry1 == True:
        punishvalue1+=2
    if failparry2 == True:
        punishvalue2+=2

              
        
    

    if health1<=13:
        health1 += heal1
    else:
        health1 = 15

    if health2<=13:
        health2 += heal2
    else:
        health2 = 15

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

    
    



while gameend == False:
    if playerstun1 == False:
        move1 = input("Player 1, it is your turn. What would you like to do? (type 'help' for a list of commands/moves!')    ")
    else:
        move1 = "stunned"

    if playerstun2 == False:
        move2 = input("Player 2, it is your turn. What would you like to do? (type 'help' for a list of commands/moves!')    ")
    else:
        move2 = "stunned"
    
    HP1, HP2, playerstun1, playerstun2, punish1, punish2 = turn(move1, move2, knight, knight, HP1, HP2, punish1, punish2)

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