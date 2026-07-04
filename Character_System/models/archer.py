from models.character import Character
from models.item import Item

class Archer(Character):

    def __init__(self, name):
        super().__init__(name, health=95, attack=18, defense=5)
        self.inventory.items.append(Item("Hunting Bow", "weapon", 3))
        self.inventory.items.append(Item("Health Potion", "potion", 35))

    def special_ability(self, target):
        print(f"  {self.name} fires two arrows!")
        print("  --- Arrow 1 ---")
        self.basic_attack(target)
        if target.is_alive():
            print("  --- Arrow 2 ---")
            self.basic_attack(target)

    def _apply_level_bonuses(self):
        self.max_health += 10
        self.health = self.max_health
        self.attack_power += 3
        self.defense += 1

    def __repr__(self):
        return f"Archer(name={self.name!r}, level={self.level})"