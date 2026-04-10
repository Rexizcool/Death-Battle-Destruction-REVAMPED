stun = False
gameend =False

class Move:
    def __init__(self, name, damage, self_damage, interrupt, block):
        self.name = name
        self.damage = damage
        self.self_damage = self_damage
        self.interrupt = interrupt
        self.block = block
    def getdamage(self):
        return self.damage
    def getselfdamage(self):
        return self.self_damage
    def getinterrupt(self):
        return self.interrupt

class Character:
    def __init__(self, name):
        self.name = name


class Knight(Character):
    def __init__(self, name):
        self.name = name
    def strike(self, opponentmove):
        if opponentmove == strike or opponentmove == kick: or opponentmove == heal
            damage = 2
            return damage
        if opponentmove == dodge:
            damage = 0
            return damage
        if opponentmove == parry
            damage = 0
            return damage
    def kick(self, opponentmove):
        if opponentmove == strike or opponentmove == kick or opponentmove == heal:
            damage = 1
            return damage
        if opponentmove == dodge:
            damage = 3
            return damage
        if opponentmove == parry
            damage = 0
            return damage
    def dodge(self, opponentmove):
        if opponentmove == strike:
            opponentstun = True
            return opponentstun
        if opponentmove == dodge or opponentmove == heal or opponentmove == kick:
            damage = 0
            return damage
        if opponentmove == parry
            opponentstun = True
            return damage
    def parry(self, opponentmove, opponentdamage):
        if opponentmove == strike or opponentmove == kick:
            damage = opponentdamage+2
            return damage
        if opponentmove == dodge or opponentmove == parry or opponentmove == heal:
            damage = 0
            return damage
    def heal(self, interrupt:
        if interrupt == True:
            heal = 0
            return heal
        if interrupt == False:
            heal = 2
            return heal
    






def turn(move1, move2, character1, character2):
    


while gameend == False:
    