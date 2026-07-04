from models.character import Character
from models.item import Item 

class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=120, attack=15, defense=8)
        self.inventory.items.append(Item("Iron Sword", "weapon", 3))
        self.inventory.items.append(Item("Health Potion", "potion", 40))

    def special_ability(self, target):
        import random
        total_attack = self.attack_power + self.inventory.get_weapon_bonus()
        damage_roll = int(total_attack * 1.5)
        actual_damage = target.take_damage(damage_roll)
        print(f"  {self.name} SHIELD BASHES {target.name} for {actual_damage} damage!")
        return actual_damage

    def _apply_level_bonuses(self):
        self.max_health += 15
        self.health = self.max_health
        self.attack_power += 2
        self.defense += 2

    def __repr__(self):
        return f"Warrior(name={self.name!r}, level={self.level})"
 