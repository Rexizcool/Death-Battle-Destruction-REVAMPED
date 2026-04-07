
class Strike:
    def __init__(self, strike_name, damage, self_damage, interrupt):
        self.strike_name = strike_name
        self.damage = damage
        self.self_damage = self_damage
        self.interrupt = interrupt

class Character:
    def __init__(self, name, strike, kick, dodge, parry, heal):
        self.name = name