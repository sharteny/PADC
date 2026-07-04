
import random
from models.inventory import Inventory
from models.item import Item
 
 
class Character:

    total_characters_created = 0

    def __init__(self, name, health, attack, defense):
        self.name = name
        self.max_health = health
        self.health = health
        self.attack_power = attack
        self.defense = defense
        self.level = 1
        self.experience = 0
        self.exp_to_level_up = 100
        self.inventory = Inventory()
 
        Character.total_characters_created += 1

    def is_alive(self):
        return self.health > 0

    def take_damage(self, raw_damage):
        total_defense = self.defense + self.inventory.get_armor_bonus()
        damage = max(1, raw_damage - total_defense)
        self.health -= damage
        self.health = max(0, self.health)
        return damage

    def basic_attack(self, target):
        total_attack = self.attack_power + self.inventory.get_weapon_bonus()
        damage_roll = random.randint(int(total_attack * 0.8), int(total_attack * 1.2))
        actual_damage = target.take_damage(damage_roll)
        print(f"  {self.name} attacks {target.name} for {actual_damage} damage!")
        return actual_damage

    def special_ability(self, target):
        self.basic_attack(target)

    def use_potion(self):
        potion = self.inventory.get_first_potion()
        if potion is None:
            print("  No potions in inventory!")
            return False
        self.inventory.items.remove(potion)
        healed = min(potion.value, self.max_health - self.health)
        self.health += healed
        print(f"  {self.name} drinks {potion.name} and restores {healed} HP! "
              f"({self.health}/{self.max_health})")
        return True

    def gain_experience(self, amount):
        self.experience += amount
        print(f"  {self.name} gains {amount} XP! ({self.experience}/{self.exp_to_level_up})")
        if self.experience >= self.exp_to_level_up:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience = 0
        self.exp_to_level_up = int(self.exp_to_level_up * 1.5)
        self._apply_level_bonuses()
        print(f"\n  *** {self.name} reached Level {self.level}! ***")
        print(f"  HP: {self.max_health} | ATK: {self.attack_power} | DEF: {self.defense}\n")

    def _apply_level_bonuses(self):
        self.max_health += 10
        self.health = self.max_health
        self.attack_power += 2
        self.defense += 1

    @staticmethod
    def validate_name(name):
        return isinstance(name, str) and len(name.strip()) > 0 and name.replace(" ", "").isalpha()

    def to_dict(self):
        return {
            "type": type(self).__name__,
            "name": self.name,
            "max_health": self.max_health,
            "health": self.health,
            "attack_power": self.attack_power,
            "defense": self.defense,
            "level": self.level,
            "experience": self.experience,
            "exp_to_level_up": self.exp_to_level_up,
            "inventory": self.inventory.to_list(),
        }

    def __str__(self):
        hp_bar = _make_bar(self.health, self.max_health, 20)
        return (
            f"{self.name} [{type(self).__name__}] Lv.{self.level} | "
            f"HP [{hp_bar}] {self.health}/{self.max_health} | "
            f"ATK {self.attack_power} | DEF {self.defense}"
        )

    def __repr__(self):
        return f"{type(self).__name__}(name={self.name!r}, level={self.level})"

def _make_bar(current, maximum, length):
    if maximum == 0:
        filled = 0
    else:
        filled = int((current / maximum) * length)
    return "#" * filled + "." * (length - filled)