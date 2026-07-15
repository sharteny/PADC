import random 
from utils.helper import make_bar

class Enemy:
 
    def __init__(self, name, health, attack, defense, exp_reward):
        self._name = name
        self._health = health
        self._max_health = health
        self._attack_power = attack
        self._defense = defense
        self._exp_reward = exp_reward

    @property
    def name(self):
        return self._name

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value

    @property
    def max_health(self):
        return self._max_health

    @max_health.setter
    def max_health(self, value):
        self._max_health = value

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
    def exp_reward(self):
        return self._exp_reward

    def is_alive(self):
        return self.health > 0
 
    def take_damage(self, raw_damage):
        damage = max(1, raw_damage - self._defense)
        self._health -= damage
        self._health = max(0, self._health)
        return damage

    def attack(self, target):
        damage_roll = random.randint(
            int(self._attack_power * 0.8),
            int(self._attack_power * 1.2)
        )
        actual_damage = target.take_damage(damage_roll)
        print(f"  {self._name} attacks {target._name} for {actual_damage} damage!")
        return actual_damage

    def __str__(self):

        hp_bar = make_bar(self._health, self._max_health, 20)
        return (
            f"{self._name} [Enemy] | "
            f"HP [{hp_bar}] {self._health}/{self._max_health} | "
            f"ATK {self._attack_power} | DEF {self._defense}"
        )

    def __repr__(self):
        return f"Enemy(name={self._name!r}, health={self._health})"

def make_enemy(player_level):
    templates = [
        ("Goblin",    0.6, 0.5, 0.3, 30),
        ("Orc",       0.9, 0.8, 0.6, 50),
        ("Troll",     1.2, 0.7, 1.0, 70),
        ("Dark Mage", 0.7, 1.2, 0.4, 80),
        ("Dragon",    2.0, 1.5, 1.2, 150),
    ]
    name, hp_mult, atk_mult, def_mult, base_exp = random.choice(templates)

    health  = int(40 * hp_mult  * (1 + player_level * 0.3))
    attack  = int(10 * atk_mult * (1 + player_level * 0.2))
    defense = int(3  * def_mult * (1 + player_level * 0.1))
    exp     = int(base_exp * (1 + player_level * 0.1))

    return Enemy(name, health, attack, defense, exp)
