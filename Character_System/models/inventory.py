from models.item import Item

class Inventory:

    def __init__(self):
        self._items = []

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value):
        self._items = value

    def add_item(self, item):
        self._items.append(item)
        print(f"  '{item.name}' added to inventory.")

    def remove_item(self, item_name):
        for item in self._items:
            if item.name.lower() == item_name.lower():
                self._items.remove(item)
                return item
        return None

    def get_first_potion(self):
        for item in self._items:
            if item.item_type == "potion":
                return item
        return None

    def get_weapon_bonus(self):
        for item in self._items:
            if item.item_type == "weapon":
                return item.value
        return 0

    def get_armor_bonus(self):
        for item in self._items:
            if item.item_type == "armor":
                return item.value
        return 0

    def show(self):
        if not self._items:
            print("  Inventory is empty.")
            return
        for i, item in enumerate(self._items, start=1):
            print(f"  {i}. {item}")

    def to_list(self):
        result = []
        for item in self._items:
            result.append({
                "name": item.name,
                "item_type": item.item_type,
                "value": item.value,
            })
        return result

    @staticmethod
    def from_list(data):
        inv = Inventory()
        for entry in data:
            inv._items.append(Item(entry["name"], entry["item_type"], entry["value"]))
        return inv
