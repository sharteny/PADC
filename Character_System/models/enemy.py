import random 
 
class Enemy:
 
    def __init__(self, name, health, attack, defense, exp_reward):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack
        self.defense = defense
        self.exp_reward = exp_reward

    def is_alive(self):
        return self.health > 0
 
    def take_damage(self, raw_damage):
        damage = max(1, raw_damage - self.defense)
        self.health -= damage
        self.health = max(0, self.health)
        return damage

    def attack(self, target):
        damage_roll = random.randint(
            int(self.attack_power * 0.8),
            int(self.attack_power * 1.2)
        )
        actual_damage = target.take_damage(damage_roll)
        print(f"  {self.name} attacks {target.name} for {actual_damage} damage!")
        return actual_damage

    def __str__(self):
        from models.character import _make_bar
        hp_bar = _make_bar(self.health, self.max_health, 20)
        return (
            f"{self.name} [Enemy] | "
            f"HP [{hp_bar}] {self.health}/{self.max_health} | "
            f"ATK {self.attack_power} | DEF {self.defense}"
        )

    def __repr__(self):
        return f"Enemy(name={self.name!r}, health={self.health})"

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
