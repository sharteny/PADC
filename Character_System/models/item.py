 
from dataclasses import dataclass

@dataclass
class Item:
    name: str
    item_type: str
    value: int

    def __str__(self):
        if self.item_type == "weapon":
            return f"{self.name} (Weapon, +{self.value} ATK)"
        elif self.item_type == "armor":
            return f"{self.name} (Armor, +{self.value} DEF)"
        elif self.item_type == "potion":
            return f"{self.name} (Potion, restores {self.value} HP)"
        return f"{self.name} ({self.item_type}, value: {self.value})"