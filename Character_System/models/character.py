
import random
from models.inventory import Inventory
from models.item import Item
from utils.helper import make_bar
 
 
class Character:

    total_characters_created = 0

    def __init__(self, name, health, attack, defense):
        self._name = name
        self._max_health = health
        self._health = health
        self._attack_power = attack
        self._defense = defense
        self._level = 1
        self._experience = 0
        self._exp_to_level_up = 100
        self._inventory = Inventory()
 
        Character.total_characters_created += 1

    @property
    def name(self):
        return self._name

    @property
    def max_health(self):
        return self._max_health

    @max_health.setter
    def max_health(self, value):
        self._max_health = value

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value

    @property
    def attack_power(self):
        return self._attack_power

    @attack_power.setter
    def attack_power(self, value):
        self._attack_power = value

    @property
    def defense(self):
        return self._defense

    @defense.setter
    def defense(self, value):
        self._defense = value

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, value):
        self._experience = value

    @property
    def exp_to_level_up(self):
        return self._exp_to_level_up

    @exp_to_level_up.setter
    def exp_to_level_up(self, value):
        self._exp_to_level_up = value

    @property
    def inventory(self):
        return self._inventory

    @inventory.setter
    def inventory(self, value):
        self._inventory = value

    def is_alive(self):
        return self.health > 0

    def take_damage(self, raw_damage):
        total_defense = self._defense + self._inventory.get_armor_bonus()
        damage = max(1, raw_damage - total_defense)
        self._health -= damage
        self._health = max(0, self._health)
        return damage

    def basic_attack(self, target):
        total_attack = self._attack_power + self._inventory.get_weapon_bonus()
        damage_roll = random.randint(int(total_attack * 0.8), int(total_attack * 1.2))
        actual_damage = target.take_damage(damage_roll)
        print(f"  {self._name} attacks {target._name} for {actual_damage} damage!")
        return actual_damage

    def special_ability(self, target):
        self.basic_attack(target)

    def use_potion(self):
        potion = self._inventory.get_first_potion()
        if potion is None:
            print("  No potions in inventory!")
            return False
        self._inventory.items.remove(potion)
        healed = min(potion.value, self._max_health - self._health)
        self.health += healed
        print(f"  {self._name} drinks {potion.name} and restores {healed} HP! "
              f"({self._health}/{self._max_health})")
        return True

    def gain_experience(self, amount):
        self._experience += amount
        print(f"  {self._name} gains {amount} XP! ({self._experience}/{self._exp_to_level_up})")
        if self.experience >= self.exp_to_level_up:
            self.level_up()

    def level_up(self):
        self._level += 1
        self._experience = 0
        self._exp_to_level_up = int(self._exp_to_level_up * 1.5)
        self._apply_level_bonuses()
        print(f"\n  *** {self._name} reached Level {self._level}! ***")
        print(f"  HP: {self._max_health} | ATK: {self._attack_power} | DEF: {self._defense}\n")

    def _apply_level_bonuses(self):
        self._max_health += 10
        self._health = self._max_health
        self._attack_power += 2
        self._defense += 1

    @staticmethod
    def validate_name(name):
        return isinstance(name, str) and len(name.strip()) > 0 and name.replace(" ", "").isalpha()

    def to_dict(self):
        return {
            "type": type(self).__name__,
            "name": self._name,
            "max_health": self._max_health,
            "health": self._health,
            "attack_power": self._attack_power,
            "defense": self._defense,
            "level": self._level,
            "experience": self._experience,
            "exp_to_level_up": self._exp_to_level_up,
            "inventory": self._inventory.to_list(),
        }

    def __str__(self):
        hp_bar = make_bar(self._health, self._max_health, 20)
        return (
            f"{self._name} [{type(self).__name__}] Lv.{self._level} | "
            f"HP [{hp_bar}] {self._health}/{self._max_health} | "
            f"ATK {self._attack_power} | DEF {self._defense}"
        )

    def __repr__(self):
        return f"{type(self).__name__}(name={self._name!r}, level={self._level})"
