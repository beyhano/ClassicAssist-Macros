#Beetle lumberjacking - By: BURGER KING - UO Unchained
#Get on your beetle with a hatchet. All you need to do is drive. Great success.
from System.Collections.Generic import List
from System import Int32

# User Configuration
USE_BEETLE = True  # Set to False to use resource satchel instead

# Constants
HATCHET_ID = 0x0F43
LOG_ID = 0x1BDD
BOARD_ID = 0x1BD7
BEETLE_TYPE = 0x317
RESOURCE_SATCHEL_IDS = [0x1576, 0x5576]  # IDs for both equipped and backpack satchels

# No board tracking for faster performance

# Clear journal at start
Journal.Clear()

def find_hatchet():
    # Check if equipped
    if Player.GetItemOnLayer('LeftHand') and Player.GetItemOnLayer('LeftHand').ItemID == HATCHET_ID:
        return Player.GetItemOnLayer('LeftHand')
    if Player.GetItemOnLayer('RightHand') and Player.GetItemOnLayer('RightHand').ItemID == HATCHET_ID:
        return Player.GetItemOnLayer('RightHand')

    # Check backpack
    hatchet = Items.FindByID(HATCHET_ID, -1, Player.Backpack.Serial)
    return hatchet

def find_logs():
    return Items.FindByID(LOG_ID, -1, Player.Backpack.Serial)

def find_beetle():
    filter = Mobiles.Filter()
    filter.RangeMax = 10
    filter.Enabled = True
    filter.Bodies = List[Int32]([BEETLE_TYPE])
    beetles = Mobiles.ApplyFilter(filter)

    if len(beetles) > 0:
        return beetles[0]
    return None

def is_overweight():
    return Player.Weight >= Player.MaxWeight

# Removed board counting functions for faster performance

def check_no_wood():
    if Journal.Search('There\'s not enough wood here to harvest.'):
        Journal.Clear()
        return True
    return False

def cut_tree():
    # Get equipped hatchet
    equipped_hatchet = Player.GetItemOnLayer('LeftHand')
    if not equipped_hatchet:
        equipped_hatchet = Player.GetItemOnLayer('RightHand')
    if not equipped_hatchet:
        Misc.SendMessage("No hatchet equipped!", 33)
        return False

    Items.UseItem(equipped_hatchet)
    Target.WaitForTarget(1000, False)  # Reduced from 1500ms
    Target.TargetExecute(Player.Serial)  # Target self instead of tree
    Misc.Pause(600)  # Reduced from 1000ms - minimum time needed for server response
    return True

def cut_logs():
    # Find hatchet
    hatchet = find_hatchet()
    if not hatchet:
        Misc.SendMessage("No hatchet found!", 33)
        return False

    # Try to equip the hatchet if not equipped
    if not Player.GetItemOnLayer('LeftHand') and not Player.GetItemOnLayer('RightHand'):
        Player.EquipItem(hatchet)
        Misc.Pause(600)  # Reduced from 1000ms - minimum time needed for equip

    # Get equipped hatchet
    equipped_hatchet = Player.GetItemOnLayer('LeftHand')
    if not equipped_hatchet:
        equipped_hatchet = Player.GetItemOnLayer('RightHand')
    if not equipped_hatchet:
        Misc.SendMessage("Failed to equip hatchet!", 33)
        return False

    # Process all logs in backpack
    found_logs = False
    for item in Player.Backpack.Contains:
        if item.ItemID == LOG_ID:
            found_logs = True
            Misc.SendMessage("Found log, cutting...", 65)

            # Cut the log
            Items.UseItem(equipped_hatchet)
            Target.WaitForTarget(1500, False)
            Target.TargetExecute(item)

            # Wait for cutting animation and board creation
            Misc.Pause(1800)  # Reduced from 2500ms - minimum time needed for log cutting

            # Additional pause between logs - removed to speed up processing
            # No need for additional pause between logs

    if not found_logs:
        Misc.SendMessage("No logs found in backpack!", 33)
        return False

    return True

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

def transfer_boards_to_storage():
    """Transfer boards to either beetle or resource satchel based on configuration"""
    if USE_BEETLE:
        return transfer_boards_to_beetle()
    else:
        return transfer_boards_to_satchel()

def transfer_boards_to_beetle():
    # First dismount if mounted
    was_mounted = False
    if Player.Mount:
        was_mounted = True
        Misc.SendMessage("Dismounting...", 65)
        Mobiles.UseMobile(Player.Serial)
        Misc.Pause(1000)  # Reduced from 1500ms - minimum time needed for dismount

    # Verify dismount was successful
    if Player.Mount:
        Misc.SendMessage("Failed to dismount!", 33)
        return False

    # Now search for beetle
    beetle = find_beetle()
    if not beetle:
        Misc.SendMessage("No beetle found nearby! Make sure your beetle is close!", 33)
        if was_mounted:  # Try to remount if we were mounted before
            Misc.SendMessage("Attempting to remount...", 65)
            Misc.Pause(300)  # Reduced from 500ms
            Player.ChatSay(52, "All Guard Me")
            Misc.Pause(300)  # Reduced from 500ms
            if beetle:
                Mobiles.UseMobile(beetle)
                Misc.Pause(600)  # Reduced from 1000ms
        return False

    # Find and move ALL boards in backpack
    moved_any = False

    # Keep checking for boards until none are left
    while True:
        found_boards = False
        # Look for any boards in backpack
        for item in Player.Backpack.Contains:
            if item.ItemID == BOARD_ID:
                found_boards = True
                moved_any = True
                Misc.SendMessage(f"Moving {item.Amount} boards to beetle...", 65)
                Items.Move(item, beetle.Backpack, 0)
                Misc.Pause(400)  # Reduced from 600ms - minimum reliable delay for item moves
                break  # Break after moving one stack to refresh container contents

        # If no more boards found, we're done
        if not found_boards:
            break

    if not moved_any:
        Misc.SendMessage("No boards found to transfer!", 33)
        if was_mounted:  # Remount if we were mounted before
            Mobiles.UseMobile(beetle)
            Misc.Pause(600)  # Reduced from 1000ms
        return False

    if moved_any:
        Misc.SendMessage("All boards moved to beetle!", 68)

    # Remount beetle if we were mounted before
    if was_mounted:
        Misc.SendMessage("Remounting...", 65)
        # Make sure beetle is still valid
        current_beetle = find_beetle()
        if current_beetle:
            Mobiles.UseMobile(current_beetle)
            Misc.Pause(1000)  # Increased back to 1000ms for reliable mounting

            # Verify mount was successful
            if not Player.Mount:
                Misc.SendMessage("First mount attempt failed, trying again...", 33)
                Misc.Pause(500)
                Mobiles.UseMobile(current_beetle)
                Misc.Pause(1000)
        else:
            Misc.SendMessage("Could not find beetle to remount!", 33)

    return True

def transfer_boards_to_satchel():
    """Transfer boards to resource satchel"""
    # Find resource satchel
    satchel = find_resource_satchel()
    if not satchel:
        Misc.SendMessage("No resource satchel found! (Check waist or backpack)", 33)
        return False

    # Find and move ALL boards in backpack
    moved_any = False
    for item in Player.Backpack.Contains:
        if item.ItemID == BOARD_ID:
            Items.Move(item, satchel, 0)
            Misc.Pause(400)  # Reduced from 600ms - minimum reliable delay for item moves
            moved_any = True

    if not moved_any:
        Misc.SendMessage("No boards found to transfer!", 33)
        return False

    if moved_any:
        Misc.SendMessage("All boards moved to satchel!", 68)

    return True

def main():
    storage_type = "beetle" if USE_BEETLE else "resource satchel"
    Misc.SendMessage(f"Starting lumberjack script - using {storage_type} for storage!", 68)

    try:
        while True:
            # Check for "no wood" message
            if check_no_wood():
                continue

            if is_overweight():
                Misc.SendMessage("Overweight! Processing logs and moving boards to storage...", 65)

                # First cut all logs into boards
                cut_logs()
                Misc.Pause(500)  # Reduced from 1000ms

                # Then transfer boards to storage
                if not transfer_boards_to_storage():
                    Misc.SendMessage("Failed to transfer boards. Stopping.", 33)
                    # Removed resource totals display for faster performance
                    break
                continue

            # Just cut the tree to get logs - don't process them yet
            cut_tree()
            # No need for additional pause here as cut_tree already has a pause

            # Wait a bit before next cut - reduced to minimum needed
            Misc.Pause(800)  # Reduced from 1500ms - minimum time between tree cuts
    except:
        Misc.SendMessage("Script interrupted!", 33)
        # Removed resource totals display for faster performance
        raise  # Re-raise the exception after showing totals

if __name__ == "__main__":
    main()
