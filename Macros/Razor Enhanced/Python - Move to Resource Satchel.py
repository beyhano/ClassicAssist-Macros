## likearesourcesatchel.py- By: Bur'Gar - UO Unchained
## Moves resources to resource satchel.
## Set INCLUDE_TOOLS = 1 to include tools, 0 to exclude them.

import sys
import Misc
import Items
import Player

# === USER CONFIGURATION ===
INCLUDE_TOOLS = 1  # Set to 1 to include tools, 0 to exclude them

# Resource Satchel IDs
RESOURCE_SATCHEL_IDS = [0x1576, 0x5576]  # IDs for both equipped and backpack satchels

# Crafting Resources
RESOURCES = {
    'METAL': [
        0x1BF2,  # Ingots
        0x19B9,  # Ore
    ],
    'WOOD': [
        0x1BD7,  # Boards
        0x1BDD,  # Logs
    ],
    'LEATHER': [
        0x1081,  # Leather
        0x1067,  # Cut-up Leather
    ],
    'CLOTH': [
        0x175D,  # Bolt of Cloth
        0x1766,  # Cut Cloth
    ],
    'SCALES': [
        0x26B4,  # Dragon Scales
    ],
    'SCROLLS': [
        0x0EF3,  # Blank Scroll
    ]
}

# Tools (will be included based on INCLUDE_TOOLS setting)
TOOLS = {
    'TOOLS': [
        0x0F9D,  # Sewing Kit
        0x1EB8,  # Tinker Tools
        0x0FBB,  # Tinker Tools
        0x1022,  # Fletcher Tools
        0x1028,  # Dovetail Saw
        0x102C,  # Moulding Planes
        0x102E,  # Scorp
        0x10E6,  # Inshave
        0x10E4,  # Draw Knife
        0x0FB4,  # Sledge Hammer
        0x0FB5,  # Smith's Hammer
        0x13E3,  # Smith's Hammer (another type)
        0x0FBC,  # Tongs
        0x10E5,  # Froe
        0x1026,  # Saw
        0x102A,  # Jointing Plane
        0x1024,  # Smoothing Plane
        0x0FBF,  # Scribe's Pen
        0x0E9B,  # Mortar and Pestle
        0x14FC,  # Lockpick
        0x0F43,  # Hatchet
        0x0F9F,  # Scissors
        0x097F,  # Skillet
    ]
}

def find_resource_satchel():
    """Find resource satchel in backpack or equipped"""
    # Check if worn on paperdoll first
    if Player.GetItemOnLayer('Waist'):
        item = Player.GetItemOnLayer('Waist')
        if item.ItemID in RESOURCE_SATCHEL_IDS:
            Misc.SendMessage("Found resource satchel on waist!", 68)
            return item
    
    # Check backpack if not on paperdoll
    for satchel_id in RESOURCE_SATCHEL_IDS:
        satchel = Items.FindByID(satchel_id, -1, Player.Backpack.Serial)
        if satchel:
            Misc.SendMessage("Found resource satchel in backpack!", 68)
            return satchel
    return None

def move_resources():
    """Move all resources to satchel"""
    satchel = find_resource_satchel()
    if not satchel:
        Misc.SendMessage("No resource satchel found! (Check waist or backpack)", 33)
        return False
    
    Misc.SendMessage("Found resource satchel!", 68)
    items_moved = 0
    
    # Combine resources and tools based on configuration
    all_resources = RESOURCES.copy()
    if INCLUDE_TOOLS:
        all_resources.update(TOOLS)
    
    # Check all items in backpack
    for item in Player.Backpack.Contains:
        # Skip the satchel itself if it's in backpack
        if item.Serial == satchel.Serial:
            continue
            
        # Check crafting resources
        is_resource = False
        for category, ids in all_resources.items():
            if item.ItemID in ids:
                is_resource = True
                Misc.SendMessage(f"Moving {category} resource...", 68)
                break
                
        # Move item if it's a resource
        if is_resource:
            Items.Move(item, satchel, 0)
            items_moved += 1
            Misc.Pause(600)
    
    # Report results
    if items_moved > 0:
        Misc.SendMessage(f"Moved {items_moved} items to resource satchel!", 68)
    else:
        Misc.SendMessage("No resources found to move!", 33)
    
    return True

def main():
    Misc.SendMessage("Starting Resource Organizer...", 68)
    move_resources()
    Misc.SendMessage("Done!", 68)

if __name__ == "__main__":
    main()







