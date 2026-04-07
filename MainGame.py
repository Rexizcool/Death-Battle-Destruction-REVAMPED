
class Move:
    def __init__(self, name, damage, self_damage, interrupt, block):
        self.name = name
        self.damage = damage
        self.self_damage = self_damage
        self.interrupt = interrupt
        self.block = block



class Character:
    def __init__(self, name):
        self.name = name


class Knight(Character):
    def __init__(self, name):
        self.name = name