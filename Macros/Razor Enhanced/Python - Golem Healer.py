## Golem Healer Script - By: Bur'Gar
## Automatically repairs nearby golem when damaged
import sys
import Misc
import Items
import Player
import Target
import Mobiles
from System.Collections.Generic import List
from System import Int32

# Constants
GOLEM_ID = 0x02C1
REPAIR_KIT_ID = 0x4B12
GOLEM_RANGE = 2  # Maximum tiles away to heal golem

def find_golem():
    """Find damaged golem within range"""
    filter = Mobiles.Filter()
    filter.Bodies = List[Int32]([Int32(GOLEM_ID)])
    filter.RangeMax = GOLEM_RANGE
    filter.Enabled = True
    
    golems = Mobiles.ApplyFilter(filter)
    
    # Return first damaged golem found
    for golem in golems:
        if golem.Hits < golem.HitsMax:
            return golem
            
    return None

def repair_golem():
    """Find and repair damaged golem"""
    # Find damaged golem
    golem = find_golem()
    if not golem:
        Misc.SendMessage("No damaged golem found nearby!", 33)
        return False
        
    # Find repair kit
    repair_kit = Items.FindByID(REPAIR_KIT_ID, -1, Player.Backpack.Serial)
    if not repair_kit:
        Misc.SendMessage("No repair kits found!", 33)
        return False
    
    # Use repair kit on golem
    Misc.SendMessage(f"Repairing golem at {golem.Hits}/{golem.HitsMax} HP", 68)
    Items.UseItem(repair_kit)
    Target.WaitForTarget(1000)
    Target.TargetExecute(golem)
    
    return True

def main():
    Misc.SendMessage("Golem Healer started! Press hotkey to repair nearby golem.", 68)
    repair_golem()

if __name__ == "__main__":
    main()
