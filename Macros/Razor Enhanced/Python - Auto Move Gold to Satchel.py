## Gold Mover - By: Bur'Gar - UO Unchained
## Automatically moves gold to gold satchel when amount changes

import sys
import Misc
import Items
import Player
import Journal

# Constants
GOLD_SATCHEL_IDS = [0x1575, 0x5575]  # IDs for both equipped and backpack satchels
GOLD_ID = 0x0EED  # ID for gold coins

class GoldMover:
    def __init__(self):
        self.last_gold = Player.Gold
        Journal.Clear()
    
    def find_gold_satchel(self):
        """Find gold satchel in backpack or equipped"""
        if Player.GetItemOnLayer('Waist'):
            item = Player.GetItemOnLayer('Waist')
            if item.ItemID in GOLD_SATCHEL_IDS:
                return item
        
        for satchel_id in GOLD_SATCHEL_IDS:
            satchel = Items.FindByID(satchel_id, -1, Player.Backpack.Serial)
            if satchel:
                return satchel
        return None
    
    def check_and_move_gold(self):
        """Check if gold amount changed and move it to satchel if it did"""
        current_gold = Player.Gold
        gold_in_backpack = False
        
        satchel = self.find_gold_satchel()
        if not satchel:
            self.last_gold = current_gold
            return
        
        gold_stacks = []
        for item in Player.Backpack.Contains:
            if item.ItemID == GOLD_ID:
                gold_stacks.append(item)
                gold_in_backpack = True
        
        if current_gold != self.last_gold or gold_in_backpack:
            if gold_stacks:
                total_moved = 0
                for gold in gold_stacks:
                    total_moved += gold.Amount
                    Items.Move(gold, satchel, 0)
                    Misc.Pause(1000)
                if total_moved > 0:
                    Misc.SendMessage(f"Moved {total_moved} gold to satchel", 68)
            
            self.last_gold = current_gold

def main():
    mover = GoldMover()
    
    try:
        while True:
            mover.check_and_move_gold()
            Misc.Pause(100)
    except Exception as e:
        Misc.SendMessage(f"Error: {e}", 33)
        raise

if __name__ == "__main__":
    main()





