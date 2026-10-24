import random
import time

#  Variables
_dBonus = 20
_maxRNG = 25
_outDelay = 0.3
_batDelay = 1


#  Classes and functions
class Character:  # Class containing all the attributes of each character
    def __init__(self, health, armour, agility, strength):
        self.health = health
        self.armour = armour
        self.agility = agility
        self.strength = strength


class Weapon:  # Class containing the basic stats of each weapon
    def __init__(self, damage, accuracy, str_req):
        self.damage = damage
        self.accuracy = accuracy
        self.str_req = str_req

    def strength_check(self, char):  # Class function to check if weapon is compatible with character
        assert char.strength >= self.str_req  # Raises an error when incompatible


def dodge(agility, accuracy):
    return (random.randrange(1, _maxRNG) <= agility) and (random.randrange(1, _maxRNG) <= accuracy)


class Energy(Weapon):  # Class for categorizing energy weapons
    def attack(self, enemy_stat, enemy):
        if dodge(enemy.agility, self.accuracy):
            return enemy_stat  # Returns stat unchanged
        else:
            if enemy_stat == (C_choice.armour or C_enemy.armour):
                return enemy_stat - (self.damage + _dBonus)  # Returns damaged stat
            else:
                return enemy_stat - (self.damage - _dBonus)


class Ballistic(Weapon):  # Class for categorizing ballistic weapons
    def attack(self, enemy_stat, enemy):
        if dodge(enemy.agility, self.accuracy):
            return enemy_stat
        else:
            if enemy_stat == (C_choice.health or C_enemy.health):
                return enemy_stat - (self.damage + _dBonus)
            else:
                return enemy_stat - (self.damage - _dBonus)


class Melee(Weapon):  # Class for categorizing melee weapons
    def attack(self, enemy_stat, enemy):
        if dodge(enemy.agility, self.accuracy):
            return enemy_stat
        else:
            return enemy_stat - self.damage


def output_chars(dic):  # Function that outputs all characters and their stats
    for i in dic:
        print("="*len(i))
        print(i)
        print("=" * len(i))
        print(f"Health - {dic[i].health}")
        print(f"Armour - {dic[i].armour}")
        print(f"Agility - {dic[i].agility}")
        print(f"Strength - {dic[i].strength}\n")
        time.sleep(_outDelay)


def output_weapons(dic):  # Function that outputs all weapons and their stats
    for i in dic:
        print("="*len(i))
        print(i)
        print("=" * len(i))
        print(f"Damage - {dic[i].damage}")
        print(f"Accuracy - {dic[i].accuracy}")
        print(f"Str Requirement - {dic[i].str_req}\n")
        time.sleep(_outDelay)


#  Instances
c = {"tank": Character(150, 150, 2, 5),  # Dictionary containing all characters
     "cyborg": Character(50, 200, 5, 3),
     "ninja": Character(70, 30, 10, 1),
     "soldier": Character(100, 10, 7, 2),
     "mutant": Character(200, 0, 4, 4),
     "robot": Character(1, 275, 1, 5)}

w = {"laser pistol": Energy(30, 10, 1),  # Dictionary containing all weapons
     "laser rifle": Energy(45, 7, 2),
     "laser shotgun": Energy(60, 5, 3),
     "laser machine gun": Energy(85, 3, 4),
     "laser cannon": Energy(100, 8, 5),
     "pistol": Ballistic(30, 10, 1),
     "rifle": Ballistic(45, 7, 2),
     "shotgun": Ballistic(60, 5, 3),
     "machine gun": Ballistic(85, 3, 4),
     ".50 cal sniper": Ballistic(100, 8, 5),
     "knife": Melee(20, 15, 1),
     "axe": Melee(30, 15, 2),
     "katana": Melee(50, 15, 3),
     "great sword": Melee(70, 15, 4),
     "gravity hammer": Melee(100, 15, 5)}

#  Battle Code
output_chars(c)
while True:
    try:
        C_choice_name = str(input("Choose your character: ")).lower()  # Allows the player to choose a character
        C_choice = c[C_choice_name]
        Player_base_ag = C_choice.agility  # Variable to hold player's default agility for reverting buffs
    except KeyError:
        print("\nEnter a valid character.\n")
        continue
    break

output_weapons(w)
while True:
    try:
        W_choice_name = str(input("Choose your weapon: ")).lower()  # Allows the player to choose a weapon
        W_choice = w[W_choice_name]
        W_choice.strength_check(C_choice)  # Variable to hold enemy's default agility for reverting buffs
    except KeyError:
        print("\nEnter a valid weapon.\n")
        continue
    except AssertionError:
        print("\nYou lack the strength for this weapon.\n")
        continue
    break

C_enemy_name = random.choice(list(c.keys()))  # Picks a character as the enemy
C_enemy = c[C_enemy_name]
Enemy_base_ag = C_enemy.agility
while True:
    try:
        W_enemy_name = random.choice(list(w.keys()))  # Picks a weapon for the enemy
        W_enemy = w[W_enemy_name]
        W_enemy.strength_check(C_enemy)
    except AssertionError:
        continue
    break

print(f"\nYour character is {C_choice_name}")
time.sleep(_batDelay)
print(f"Your weapon is a {W_choice_name}")
time.sleep(_batDelay)
print(f"You have {C_choice.health} health and {C_choice.armour} armour\n")
time.sleep(_batDelay)
print(f"Your enemy is {C_enemy_name}")
time.sleep(_batDelay)
print(f"Their weapon is a {W_enemy_name}")
time.sleep(_batDelay)
print(f"They have {C_enemy.health} health and {C_enemy.armour} armour\n")

name = str(input("Enter your name: "))

while True:
    C_choice.agility = Player_base_ag  # Reverts agility back to default each turn
    C_enemy.agility = Enemy_base_ag
    uInput = str(input("Attack or Defend?: ")).lower()  # Allows the player to choose between attacking or defending
    if uInput == "attack" and C_enemy.armour > 0:  # Checks whether to damage armour or health
        dmg_reduction = W_choice.attack(C_enemy.armour, C_enemy)
        if dmg_reduction == C_enemy.armour:
            print(f"\nEnemy {C_enemy_name} dodged the attack!")
            time.sleep(_batDelay)
        else:
            C_enemy.armour = dmg_reduction  # Sets the enemy's armour to the damaged value
            if C_enemy.armour <= 0:  # Checks if enemy's armour is gone
                print(f"\n{C_choice_name} {name} uses {W_choice_name}...")
                time.sleep(_batDelay)
                print(f"Enemy {C_enemy_name}'s armour has been destroyed!")
                time.sleep(_batDelay)
            else:
                print(f"\n{C_choice_name} {name} uses {W_choice_name}...")
                time.sleep(_batDelay)
                print(f"Enemy {C_enemy_name}'s armour is now at {C_enemy.armour}!")
                time.sleep(_batDelay)
    elif uInput == "attack":
        dmg_reduction = W_choice.attack(C_enemy.health, C_enemy)
        if dmg_reduction == C_enemy.health:
            print(f"\nEnemy {C_enemy_name} dodged the attack!")
            time.sleep(_batDelay)
        else:
            C_enemy.health = dmg_reduction  # Sets the enemy's health to the damaged value
            if C_enemy.health <= 0:  # Checks if the enemy is dead
                time.sleep(_batDelay)
                print("You win!")
                break
            else:
                print(f"\n{C_choice_name} {name} uses {W_choice_name}...")
                time.sleep(_batDelay)
                print(f"Enemy {C_enemy_name}'s health is now at {C_enemy.health}!")
                time.sleep(_batDelay)
    elif uInput == "defend":
        print(f"\n{C_choice_name} {name} defends...")
        C_choice.agility += 2
    else:
        print("Enter a valid action.")
        continue

    eInput = random.choice(["attack", "defend"])  # Enemy chooses between attacking and defending
    if eInput == "attack" and C_choice.armour > 0:  # Checks whether to damage armour or health
        dmg_reduction = W_enemy.attack(C_choice.armour, C_choice)  # Sets the player's armour to the damaged value
        if dmg_reduction == C_choice.armour:
            print(f"\n{C_choice_name} {name} dodged the attack!")
            time.sleep(_batDelay)
        else:
            C_choice.armour = dmg_reduction  # Sets the player's armour to the damaged value
            if C_choice.armour <= 0:  # Checks if player's armour is gone
                print(f"\nEnemy {C_enemy_name} uses {W_enemy_name}...")
                time.sleep(_batDelay)
                print(f"{C_choice_name} {name}'s armour has been destroyed!")
                time.sleep(_batDelay)
            else:
                print(f"\nEnemy {C_enemy_name} uses {W_enemy_name}...")
                time.sleep(_batDelay)
                print(f"{C_choice_name} {name}'s armour is now at {C_choice.armour}!")
                time.sleep(_batDelay)
    elif eInput == "attack":
        dmg_reduction = W_enemy.attack(C_choice.health, C_choice)
        if dmg_reduction == C_choice.health:
            print(f"\n{C_choice_name} {name} dodged the attack!")
            time.sleep(_batDelay)
        else:
            C_choice.health = dmg_reduction  # Sets the player's health to the damaged value
            if C_choice.health <= 0:  # Checks if the player is dead
                time.sleep(_batDelay)
                print("You lose!")
                break
            else:
                print(f"\nEnemy {C_enemy_name} uses {W_enemy_name}...")
                time.sleep(_batDelay)
                print(f"{C_choice_name} {name}'s health is now at {C_choice.health}!")
                time.sleep(_batDelay)
    elif eInput == "defend":
        print(f"\nEnemy {C_enemy_name} defends...")
        C_enemy.agility += 2
        time.sleep(_batDelay)
