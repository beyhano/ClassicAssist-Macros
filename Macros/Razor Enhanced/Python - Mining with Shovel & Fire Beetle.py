## Likeaminer.py - By: Bur'Gar - UO Unchained
## Adjust MINING_DELAY as needed for pang pong Jennay - Great success. Make weps and armors to klomp umies.
import Misc
import Items
import Player
import Mobiles
import Journal
import Target
import time
from System.Collections.Generic import List
from System import Int32

# Constants
SHOVEL_TYPE = 0x0F39
MINING_DELAY = 1500  # Adjust as needed
NO_ORE_MESSAGE = "There is no metal here to mine."
OVERWEIGHT_MESSAGE = "You can't carry that much weight."
RESOURCE_SATCHEL_IDS = [0x1576, 0x5576]  # IDs for both equipped and backpack satchels

# Resource types and their corresponding ore/ingot IDs and hues
RESOURCES = {
    'Iron': {'ore': 0x19B9, 'ingot': 0x1BF2, 'hue': 0x0000},
    'Dull Copper': {'ore': 0x19B9, 'ingot': 0x1BF2, 'hue': 0x0973},
    'Shadow Iron': {'ore': 0x19B9, 'ingot': 0x1BF2, 'hue': 0x0966},
    'Copper': {'ore': 0x19B9, 'ingot': 0x1BF2, 'hue': 0x096D},
    'Bronze': {'ore': 0x19B9, 'ingot': 0x1BF2, 'hue': 0x0972},
    'Golden': {'ore': 0x19B9, 'ingot': 0x1BF2, 'hue': 0x08A5},
    'Agapite': {'ore': 0x19B9, 'ingot': 0x1BF2, 'hue': 0x0979},
    'Verite': {'ore': 0x19B9, 'ingot': 0x1BF2, 'hue': 0x089F},
    'Valorite': {'ore': 0x19B9, 'ingot': 0x1BF2, 'hue': 0x08AB}
}

class MiningTracker:
    def __init__(self):
        self.ingot_counts = {resource: 0 for resource in RESOURCES}
        self.start_time = time.time()
    
    def print_totals(self):
        Misc.SendMessage("=== Ingots Created ===", 68)  # Light green
        
        # Calculate total count
        total_ingots = sum(self.ingot_counts.values())
        Misc.SendMessage(f"Total ingots: {total_ingots}", 65)
        
        # Sort resources by rarity/type
        rare_ores = ["Valorite", "Verite"]
        uncommon_ores = ["Agapite", "Golden"]
        common_ores = ["Iron", "Dull Copper", "Shadow Iron", "Copper", "Bronze"]
        
        # Display rare ores first
        for resource in rare_ores:
            if self.ingot_counts[resource] > 0:
                Misc.SendMessage(f"{resource}: {self.ingot_counts[resource]}", 38)  # Red
        
        # Then uncommon ores
        for resource in uncommon_ores:
            if self.ingot_counts[resource] > 0:
                Misc.SendMessage(f"{resource}: {self.ingot_counts[resource]}", 53)  # Yellow
        
        # Finally common ores
        for resource in common_ores:
            if self.ingot_counts[resource] > 0:
                Misc.SendMessage(f"{resource}: {self.ingot_counts[resource]}", 90)  # Gray
        
        # Calculate and display ingots per hour
        elapsed_time = time.time() - self.start_time
        hours = elapsed_time / 3600  # Convert seconds to hours
        if hours > 0:
            ingots_per_hour = int(total_ingots / hours)
            Misc.SendMessage(f"Estimated rate: {ingots_per_hour} ingots/hour", 68)
        
        Misc.SendMessage("==================", 68)

    def update_counts(self, beetle_serial):
        """Count all ingots in player's backpack"""
        # Reset all counts first
        for resource in RESOURCES:
            self.ingot_counts[resource] = 0
        
        # Iterate through all items in backpack
        for item in Player.Backpack.Contains:
            if item.ItemID == 0x1BF2:  # If it's an ingot
                # Check for regular iron first (no hue)
                if item.Hue == 0x0000:
                    self.ingot_counts['Iron'] += item.Amount
                    continue
                
                # Check for special ingots by hue
                for resource, info in RESOURCES.items():
                    if item.Hue == info['hue']:
                        self.ingot_counts[resource] += item.Amount
                        Misc.SendMessage(f"Found {resource} ingots: {item.Amount} (Hue: {hex(item.Hue)})", 65)
                        break

def find_fire_beetle():
    """Find and return the fire beetle serial"""
    filter = Mobiles.Filter()
    filter.Bodies = List[Int32]([Int32(0x00A9)])
    filter.RangeMax = 2
    filter.Enabled = True
    
    beetles = Mobiles.ApplyFilter(filter)
    if beetles and len(beetles) > 0:  # Check if list exists and has items
        return beetles[0].Serial  # Return first beetle's serial
    return None

def find_shovel():
    """Find a shovel in the backpack"""
    shovel = Items.FindByID(SHOVEL_TYPE, -1, Player.Backpack.Serial)
    return shovel  # Return the item directly

def find_resource_satchel():
    """Find resource satchel in backpack or equipped"""
    # Check if worn on paperdoll first
    if Player.GetItemOnLayer('Waist'):
        item = Player.GetItemOnLayer('Waist')
        if item.ItemID in RESOURCE_SATCHEL_IDS:
            Misc.SendMessage("Found satchel on waist!", 68)
            return item
    
    # Check backpack if not on paperdoll
    for satchel_id in RESOURCE_SATCHEL_IDS:
        satchel = Items.FindByID(satchel_id, -1, Player.Backpack.Serial)
        if satchel:
            Misc.SendMessage("Found satchel in backpack!", 68)
            return satchel
    
    return None

def smelt_ores(beetle_serial, tracker):
    """Smelt all ores in backpack using fire beetle"""
    if not beetle_serial:
        Misc.SendMessage("No fire beetle found!", 33)
        return
    
    # First, smelt all ores
    ore_count = 0
    for resource in RESOURCES.values():
        ore = Items.FindByID(resource['ore'], -1, Player.Backpack.Serial)
        while ore:  # Keep smelting until all ore of this type is gone
            ore_count += 1
            Items.UseItem(ore.Serial)
            Target.WaitForTarget(1500)
            Target.TargetExecute(beetle_serial)
            Misc.Pause(1000)
            ore = Items.FindByID(resource['ore'], -1, Player.Backpack.Serial)
    
    if ore_count > 0:
        Misc.SendMessage(f"Smelted {ore_count} pieces of ore", 68)
        Misc.Pause(1000)
        
        # Update our counts after all smelting is done
        tracker.update_counts(beetle_serial)
        
        # Now move all ingots to satchel
        satchel = find_resource_satchel()
        if satchel:
            Misc.SendMessage(f"Found satchel with serial: {satchel.Serial}", 68)
            ingots_moved = 0
            
            # First, count how many ingots we have
            ingot_count = 0
            for item in Player.Backpack.Contains:
                if item.ItemID == 0x1BF2:  # If it's an ingot
                    ingot_count += 1
            
            Misc.SendMessage(f"Found {ingot_count} ingots to move", 68)
            
            # Now move them
            for item in Player.Backpack.Contains:
                if item.ItemID == 0x1BF2:  # If it's an ingot
                    Misc.SendMessage(f"Moving ingot: {item.Serial}", 68)
                    Items.Move(item, satchel, 0)
                    ingots_moved += 1
                    Misc.Pause(1000)  # Increased pause to ensure move completes
            
            if ingots_moved > 0:
                Misc.SendMessage(f"Moved {ingots_moved} ingots to resource satchel!", 68)
            else:
                Misc.SendMessage("Failed to move any ingots!", 33)
        else:
            Misc.SendMessage("No resource satchel found! (Check waist or backpack)", 33)

def debug_find_beetle():
    filter = Mobiles.Filter()
    filter.RangeMax = 10
    filter.Enabled = True
    
    mobiles = Mobiles.ApplyFilter(filter)
    for mobile in mobiles:
        Misc.SendMessage(f"Found mobile: {mobile.Name}, Body: {hex(mobile.Body)}", 66)

def main():
    Mobiles.Message(Player.Serial, 68, "Starting mining script...")
    
    # Initialize
    beetle_serial = find_fire_beetle()
    if not beetle_serial:
        Mobiles.Message(Player.Serial, 33, "No fire beetle found! Please have your fire beetle nearby.")
        return
    
    tracker = MiningTracker()
    Journal.Clear()
    
    while True:
        if Player.IsGhost:
            break
            
        # Check weight BEFORE mining
        if Journal.Search(OVERWEIGHT_MESSAGE) or Player.Weight >= Player.MaxWeight:
            Mobiles.Message(Player.Serial, 68, "Overweight! Smelting current load...")
            smelt_ores(beetle_serial, tracker)
            tracker.print_totals()
            Journal.Clear()
            continue
            
        shovel = find_shovel()
        if not shovel:
            Mobiles.Message(Player.Serial, 33, "No shovel found in backpack!")
            break
        
        # Mine
        Items.UseItem(shovel.Serial)
        Target.WaitForTarget(1500)
        Target.TargetExecute(Player.Serial)
        Misc.Pause(MINING_DELAY)
        
        # Check for no ore message
        if Journal.Search(NO_ORE_MESSAGE):
            Mobiles.Message(Player.Serial, 68, "No more ore here. Smelting current load...")
            smelt_ores(beetle_serial, tracker)
            tracker.print_totals()
            break
    
    Mobiles.Message(Player.Serial, 68, "Mining session completed!")
    tracker.print_totals()

if __name__ == "__main__":
    main()




