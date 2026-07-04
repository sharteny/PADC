from models.character import Character
from models.item import Item

class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=80, attack=22, defense=3)
        self.mana = 50
        self.max_mana = 50
        self.inventory.items.append(Item("Magic Staff", "weapon", 4))
        self.inventory.items.append(Item("Health Potion", "potion", 30))
 
    def special_ability(self, target):
        mana_cost = 20
        if self.mana < mana_cost:
            print(f"  {self.name} is out of mana! Falling back to basic attack.")
            self.basic_attack(target)
            return

        self.mana -= mana_cost
        raw = int(self.attack_power * 2)
        damage = max(1, raw - (target.defense // 2))
        target.health -= damage
        target.health = max(0, target.health)
        print(f"  {self.name} casts FIREBALL on {target.name} for {damage} damage! "
              f"({self.mana}/{self.max_mana} mana left)")

    def _apply_level_bonuses(self):
        self.max_health += 8
        self.health = self.max_health
        self.attack_power += 4
        self.defense += 1
        self.max_mana += 10
        self.mana = self.max_mana

    def to_dict(self):
        data = super().to_dict()
        data["mana"] = self.mana
        data["max_mana"] = self.max_mana
        return data

    def __str__(self):
        base = super().__str__()
        return base + f" | Mana {self.mana}/{self.max_mana}"

    def __repr__(self):
        return f"Mage(name={self.name!r}, level={self.level})"