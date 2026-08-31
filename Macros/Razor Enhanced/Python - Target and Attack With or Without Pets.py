## Tank Script - By: Bur'Gar - UO Unchained
## Hotkey to attack nearest monster, criminal, murderer. Config for pets
## Auto-switches to criminal/murderer players when they appear
import sys
import Misc
import Items
import Player
import Target
import Mobiles
from System.Collections.Generic import List
from System import Byte

# Constants
GUARD_RANGE = 12  # Maximum range to search for targets
CRIMINAL_NOTORIETY = 3
MURDERER_NOTORIETY = 6
USE_PET_COMMANDS = True  # Set to False if you're not a pet class (Tamer/Beastmaster)

def get_priority_target():
    """Find highest priority target (murderer > criminal > monster)"""
    filter = Mobiles.Filter()
    filter.RangeMax = GUARD_RANGE
    filter.Enabled = True
    
    # First check for hostile players
    filter.IsHuman = True  # Only actual players
    filter.Notorieties = List[Byte]([
        Byte(MURDERER_NOTORIETY),  # Murderer (red)
        Byte(CRIMINAL_NOTORIETY),  # Criminal (gray)
        Byte(4),  # Enemy (orange)
        Byte(5),  # Enemy (orange)
    ])
    players = Mobiles.ApplyFilter(filter)
    
    if players:
        # Sort by notoriety then distance
        valid_players = sorted(players, key=lambda x: (-x.Notoriety, Player.DistanceTo(x)))
        return valid_players[0]
    
    # If no hostile players, look for hostile mobiles
    filter = Mobiles.Filter()  # Reset filter
    filter.RangeMax = GUARD_RANGE
    filter.Enabled = True
    filter.Notorieties = List[Byte]([
        Byte(MURDERER_NOTORIETY),  # Murderer (red)
        Byte(CRIMINAL_NOTORIETY),  # Criminal (gray)
        Byte(4),  # Enemy (orange)
        Byte(5),  # Enemy (orange)
        Byte(3),  # Attackable but not criminal (gray)
    ])
    
    # Don't filter by IsHuman - catch everything hostile
    targets = Mobiles.ApplyFilter(filter)
    
    if targets:
        # Sort by distance only for non-players
        targets = sorted(targets, key=lambda x: Player.DistanceTo(x))
        return targets[0]
    
    return None

def is_combat_finished(target):
    """Check if target is dead or gone"""
    try:
        if not target:
            Misc.SendMessage("Target lost", 33)
            return True
            
        # Debug message for target status
        Misc.SendMessage(f"Target HP: {target.Hits}/{target.HitsMax}", 68)
        
        if target.Hits <= 0:
            Misc.SendMessage("Target is dead", 68)
            return True
        if Player.DistanceTo(target) > GUARD_RANGE:
            Misc.SendMessage("Target out of range", 33)
            return True
        return False
    except Exception as e:
        Misc.SendMessage(f"Error checking target: {e}", 33)
        return True

def attack_and_guard():
    """Attack nearest valid target and call for guards"""
    target = get_priority_target()
    
    if target:
        # Store target serial for tracking
        target_serial = target.Serial
        initial_hp = target.Hits
        
        # Call guards FIRST for any target
        if target.IsHuman:
            status = "Murderer" if target.Notoriety == MURDERER_NOTORIETY else "Criminal"
            Misc.SendMessage(f"*** ATTACKING {status}: {target.Name}! ***", 33)
        else:
            Misc.SendMessage(f"*** ATTACKING MONSTER: {target.Name} ({target.Hits}/{target.HitsMax}) ***", 68)
        
        # Call guards once at start of combat if using pet commands
        if USE_PET_COMMANDS:
            Player.ChatSay(33, "All Guard Me")
            Misc.Pause(200)
        
        # Attack target after guard call
        Player.Attack(target)
        Misc.Pause(500)  # Small pause to ensure attack goes through
            
        # Wait for combat to finish
        while True:
            current_target = Mobiles.FindBySerial(target_serial)
            if not current_target:
                Misc.SendMessage("Target lost completely", 33)
                break
                
            if current_target.Hits <= 0:
                Misc.SendMessage("Target confirmed dead", 68)
                break
                
            if Player.DistanceTo(current_target) > GUARD_RANGE:
                Misc.SendMessage("Target ran away", 33)
                break
                
            # Just re-attack, no guard calls needed during combat
            Player.Attack(target_serial)
            Misc.Pause(100)
        
        # Extra pause to ensure target is really dead
        Misc.Pause(1000)
        
        # Double check target state
        final_target = Mobiles.FindBySerial(target_serial)
        if final_target and final_target.Hits > 0:
            Misc.SendMessage("Target still alive - not recalling pets", 33)
            return
            
        # Now that target is confirmed dead, recall followers if using pet commands
        if USE_PET_COMMANDS:
            Misc.SendMessage("Combat finished - recalling followers", 68)
            Player.ChatSay(33, "All Follow Me")
    else:
        Misc.SendMessage("No valid targets found!", 33)

def main():
    pet_status = "with pet commands" if USE_PET_COMMANDS else "without pet commands"
    Misc.SendMessage(f"Tank script started {pet_status}! Use hotkey to attack and call guards.", 68)
    attack_and_guard()

if __name__ == "__main__":
    main()










