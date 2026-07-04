import sys
import os
import random

sys.path.insert(0, os.path.dirname(__file__))

from models.warrior import Warrior
from models.mage import Mage
from models.archer import Archer
from models.character import Character
from models.enemy import make_enemy
from services.battle_service import BattleService
from services.save_service import save_character, load_character
from utils.validators import get_nonempty_input, get_int_input
 
def create_character():
    print("\n-- Create Character --")
    print("  1. Warrior  (HP: 120 | ATK: 15 | DEF: 8  | Ability: Shield Bash)")
    print("  2. Mage     (HP: 80  | ATK: 22 | DEF: 3  | Ability: Fireball)")
    print("  3. Archer   (HP: 95  | ATK: 18 | DEF: 5  | Ability: Quick Shot)")

    choice = get_int_input("  Choose class (1-3): ", 1, 3)
    while True:
        name = get_nonempty_input("  Enter your character's name: ")
        if Character.validate_name(name):
            break
        print("  Name must contain only letters and spaces.") 
    if choice == 1:
        return Warrior(name)
    elif choice == 2:
        return Mage(name)
    else:
        return Archer(name)

def action_view_character(character):
    print("\n-- Character Sheet --")
    print(f"  {character}")
    print(f"  XP: {character.experience}/{character.exp_to_level_up}")
    print(f"\n  Inventory:")
    character.inventory.show()

def action_go_on_adventure(character):
    print("\n-- Adventure --")
    print("  You head out into the wilderness...")

    num_enemies = random.randint(1, min(3, character.level))
    enemies = [make_enemy(character.level) for _ in range(num_enemies)]
    if len(enemies) == 1:
        print(f"  You encounter a {enemies[0].name}!")
    else:
        names = ", ".join(e.name for e in enemies)
        print(f"  You encounter {len(enemies)} enemies: {names}!")
    battle = BattleService(character)
    survived = battle.run(enemies) 
    if survived:
        print("\n  You return to town victorious!")
    else:
        print(f"\n  Game over. {character.name} reached Level {character.level}.")
        return False
 
    return True
 
def action_save(character):
    save_character(character)
 
def print_main_menu(character):
    print(f"\n{'='*45}")
    print(f"  {character.name} the {type(character).__name__} — Lv.{character.level}")
    print(f"{'='*45}")
    print("  1. View character sheet")
    print("  2. Go on an adventure (battle)")
    print("  3. Save character")
    print("  0. Quit")
    print(f"{'='*45}")

def main():
    print("=" * 45)
    print("   Welcome to the RPG!")
    print("=" * 45)
    print("  1. New game")
    print("  2. Load saved character")
    print("  0. Quit")

    choice = input("  Your choice: ").strip()
    if choice == "1":
        character = create_character()
    elif choice == "2":
        character = load_character()
        if character is None:
            print("  No save found. Creating a new character.")
            character = create_character()
    elif choice == "0":
        print("  Goodbye!")
        return
    else:
        print("  Invalid choice. Starting new game.")
        character = create_character()
    print(f"\n  Welcome, {character.name} the {type(character).__name__}!")
    while True:
        print_main_menu(character)
        choice = input("  Your choice: ").strip() 
        if choice == "1":
            action_view_character(character)
        elif choice == "2":
            still_alive = action_go_on_adventure(character)
            if not still_alive:
                break
        elif choice == "3":
            action_save(character)
        elif choice == "0":
            action_save(character)
            print("  Thanks for playing!")
            break
        else:
            print("  Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
 