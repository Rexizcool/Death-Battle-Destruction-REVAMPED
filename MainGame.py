
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




class Knight(Character):
    def __init__(self, name):
        self.name = name
    def strikeinfo(self):
        damage=2
        interrupt=True
        movetype=strike
        return damage, interrupt, movetype
    def kickinfo(self):
        damage=1
        interrupt=False
        movetype=kick
        dodgedamage=3
        return damage, interrupt, movetype, dodgedamage
    def dodgeinfo(self):
       dodging=True
       interrupt=False


