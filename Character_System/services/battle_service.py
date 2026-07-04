from models.item import Item
import random

class BattleService:
 
    def __init__(self, player):
        self.player = player
 
    def run(self, enemies):
        for enemy in enemies:
            survived = self._fight_one(enemy)
            if not survived:
                return False
        return True

    def _fight_one(self, enemy):
        print(f"\n  {'='*50}")
        print(f"  A wild {enemy.name} appears!")
        print(f"  {'='*50}")

        while self.player.is_alive() and enemy.is_alive():
            print(f"\n  {self.player}")
            print(f"  {enemy}")
            print()
            action = self._get_player_action()
            if action == "1":
                self.player.basic_attack(enemy)
            elif action == "2":
                self.player.special_ability(enemy)
            elif action == "3":
                self.player.use_potion()
            elif action == "4":
                print("  You fled from battle!")
                return True
            if enemy.is_alive():
                enemy.attack(self.player)
        if self.player.is_alive():
            print(f"\n  {enemy.name} was defeated!")
            self.player.gain_experience(enemy.exp_reward)
            if random.random() < 0.4:
                drop = Item("Health Potion", "potion", 30)
                print(f"  {enemy.name} dropped a {drop.name}!")
                self.player.inventory.add_item(drop)
            return True
        else:
            print(f"\n  {self.player.name} was defeated...")
            return False

    def _get_player_action(self):
        print("  Your turn:")
        print("  1. Basic Attack")
        print("  2. Special Ability")
        print("  3. Use Potion")
        print("  4. Flee")
        while True:
            choice = input("  Choose (1-4): ").strip()
            if choice in ("1", "2", "3", "4"):
                return choice
            print("  Please enter 1, 2, 3, or 4.")