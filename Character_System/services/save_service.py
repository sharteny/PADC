import json
import os
from models.warrior import Warrior
from models.mage import Mage
from models.archer import Archer
from models.inventory import Inventory
from models.character import Character

SAVE_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "save.json")

def save_character(character):
    os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
    data = character.to_dict()
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"  Character saved.")

def load_character(): 
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        char_type = data["type"]
        if char_type == "Warrior":
            character = Warrior(data["name"])
        elif char_type == "Mage":
            character = Mage(data["name"])
        elif char_type == "Archer":
            character = Archer(data["name"])
        else:
            print("  Unknown character type in save file.")
            return None
        character.max_health       = data["max_health"]
        character.health           = data["health"]
        character.attack_power     = data["attack_power"]
        character.defense          = data["defense"]
        character.level            = data["level"]
        character.experience       = data["experience"]
        character.exp_to_level_up  = data["exp_to_level_up"]
        character.inventory        = Inventory.from_list(data["inventory"])
        if char_type == "Mage":
            character.mana     = data.get("mana", character.max_mana)
            character.max_mana = data.get("max_mana", character.max_mana)
        Character.total_characters_created -= 1
        print(f"  Loaded {character.name} the {char_type} (Level {character.level}).")
        return character
    except FileNotFoundError:
        return None
    except (json.JSONDecodeError, KeyError) as e:
        print(f"  Could not load save: {e}. Starting a new game.")
        return None