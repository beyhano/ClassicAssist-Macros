## Unabomber - By: Bur'Gar - UO Unchained
## Chain throw explosion pots at closest player until hotkey pressed again. 
## Great success, pushdug umies.
import time
import Misc
import Player
import Items
import Target
import Mobiles
import Journal
from System.Collections.Generic import List
from System import Byte

# === CONFIGURATION ===
EXPLOSION_POT_ID = 0x0F0D  # Explosion potion item ID
EXPLOSION_DELAY = 3200  # Adjusted for precise timing (3.2s)
THROW_DELAY = 1000  # Delay between throws
TARGET_RANGE = 10  # Maximum range to throw potions

last_explosion = 0  # Timestamp of last explosion throw

def get_nearest_player():
    """Find the nearest valid player target (not dead)"""
    mob_filter = Mobiles.Filter()
    mob_filter.RangeMax = TARGET_RANGE
    mob_filter.Enabled = True
    mob_filter.IsHuman = True
    mob_filter.Notorieties = List[Byte]([Byte(1), Byte(2), Byte(3), Byte(4), Byte(5), Byte(6)])  # Convert to Byte

    players = Mobiles.ApplyFilter(mob_filter)
    if players:
        return players[0]  # Closest player
    return None

def throw_explosion(target):
    """Throw explosion potion at target with precise timing"""
    global last_explosion
    
    current_time = time.time() * 1000
    if current_time - last_explosion < THROW_DELAY:
        return False  # Avoid spamming

    pot = Items.FindByID(EXPLOSION_POT_ID, -1, Player.Backpack.Serial)
    if not pot:
        Misc.SendMessage("No explosion potions!", 33)
        return False

    # Double-check range
    distance = abs(Player.Position.X - target.Position.X) + abs(Player.Position.Y - target.Position.Y)
    if distance > TARGET_RANGE:
        Misc.SendMessage("Target out of range!", 33)
        return False

    # Use explosion potion
    Items.UseItem(pot)
    Misc.Pause(EXPLOSION_DELAY - 600)  # Adjusted for better timing before targeting

    if Target.HasTarget():
        Target.TargetExecute(target.Serial)  # Throw at player
        last_explosion = current_time
        return True
    else:
        Misc.SendMessage("Failed to target explosion potion!", 33)
        return False

def main():
    while True:
        target = get_nearest_player()
        if target:
            Misc.SendMessage(f"Throwing at {target.Name}", 65)
            throw_explosion(target)
        Misc.Pause(500)

if __name__ == "__main__":
    main()
