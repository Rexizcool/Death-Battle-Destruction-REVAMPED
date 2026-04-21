from MainGame.py import Knight, Samurai, Mage, Cowboy, Pirate, Ninja, turn

testHP = 15

test_knight = Knight(testHP)

test_damage = 2

test_healing = 1

def test_take_damage():
    assert test_knight.takedamage(test_damage, test_healing) == 14

