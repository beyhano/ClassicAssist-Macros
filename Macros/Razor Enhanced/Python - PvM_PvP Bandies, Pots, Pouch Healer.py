## - Non-Magery Healer: By: Bur'Gar - UO Unchained
## Uses bandies monitoring journal. Cure pots, GHeal pots at 50%, uses magic pouch on Paras
## You need to set PARALYZE_CURE_ID to the ID of pouch type you use. Great success.
import sys
import time
from System.Collections.Generic import List
import Misc
import Player
import Items
import Journal
import Timer
import Target
import Mobiles

# === CONFIGURATION ===
BANDAGE_ID = 0x0E21
GREATER_HEAL_POT_ID = 0x0F0C
GREATER_CURE_POT_ID = 0x0F07
PARALYZE_CURE_ID = 0x09B0  # Special paralysis cure item
HEALTH_THRESHOLD = 50  # Use greater heal at 50% health
CURE_CHECK_DELAY = 500  # Time to wait between cure checks
GREATER_HEAL_COOLDOWN = 10000  # 10 seconds in milliseconds
STRENGTH_POT_ID = 0x0F09  # Greater Strength potion
AGILITY_POT_ID = 0x0F08   # Greater Agility potion
PVP_BUFF_COOLDOWN = 30000  # 30 seconds in milliseconds
SUPPLY_BAG_ID = 0x0E76    # Bag to search for bandages if not in main backpack

# Initialize timers and flags
last_paralysis_cure = 0
bandage_start_time = 0
bandage_start_health = 0
last_second_displayed = 0
last_greater_heal = 0
cure_pots_warning_shown = False
last_str_buff = 0
last_agi_buff = 0
pvp_warning_shown = False
poison_warning_shown = False
last_poison_state = False
heal_pots_warning_shown = False

def is_bandaging():
    """Check if bandaging is in progress"""
    # Add a time check to prevent stuck states
    global bandage_start_time
    current_time = time.time()

    # If bandaging has been going for more than 15 seconds, assume it's stuck
    if bandage_start_time > 0 and (current_time - bandage_start_time) > 6:
        bandage_start_time = 0
        return False

    return Journal.Search("You begin applying") and not Journal.Search("You finish applying")

def find_bandage():
    """Find bandages in backpack or supply bag"""
    # First check main backpack
    bandage = Items.FindByID(BANDAGE_ID, -1, Player.Backpack.Serial)
    if bandage:
        return bandage

    # If not found, check in supply bag
    supply_bag = Items.FindByID(SUPPLY_BAG_ID, -1, Player.Backpack.Serial)
    if supply_bag:
        # Look for bandages in the supply bag
        for item in Items.FindBySerial(supply_bag.Serial).Contains:
            if item.ItemID == BANDAGE_ID:
                return item

    # No bandages found anywhere
    return None

def use_bandage():
    """Apply bandage to self"""
    global bandage_start_time, bandage_start_health

    # Clear journal before checking for bandages
    Journal.Clear()

    bandage = find_bandage()
    if not bandage:
        Mobiles.Message(Player.Serial, 33, "No bandages in backpack or supply bag!")
        return False

    if is_bandaging():
        return False

    # Record start time and health
    bandage_start_time = time.time()
    bandage_start_health = Player.Hits

    Mobiles.Message(Player.Serial, 68, "Bandaging...")
    Items.UseItem(bandage)
    Target.WaitForTarget(1000)
    Target.TargetExecute(Player.Serial)

    # Verify bandaging started
    Misc.Pause(100)
    if not Journal.Search("You begin applying"):
        bandage_start_time = 0
        return False

    return True

def check_bandage_healing():
    """Check if healing is complete and report time"""
    global bandage_start_time, bandage_start_health, last_second_displayed

    if bandage_start_time > 0:
        # Check for failure messages
        if Journal.Search("You fail to apply the bandages.") or Journal.Search("You cannot heal"):
            bandage_start_time = 0
            bandage_start_health = 0
            last_second_displayed = 0
            Journal.Clear()
            return

        # Show current elapsed time while healing
        if Player.Hits < Player.HitsMax:
            current_time = time.time() - bandage_start_time
            current_second = int(current_time)
            # Only display if we're on a new second
            if current_second > last_second_displayed:
                Mobiles.Message(Player.Serial, 68, f"{current_second}s")
                last_second_displayed = current_second
        # Final report when fully healed
        elif Player.Hits == Player.HitsMax:
            elapsed_time = time.time() - bandage_start_time
            health_gained = Player.Hits - bandage_start_health

            if health_gained > 0:
                # Send both messages
                Misc.SendMessage(f"Healed {health_gained} HP in {elapsed_time:.1f} seconds", 68)
                Mobiles.Message(Player.Serial, 68, f"+{health_gained}hp {elapsed_time:.1f}s")

            # Reset timers
            bandage_start_time = 0
            bandage_start_health = 0
            last_second_displayed = 0
            Journal.Clear()

def use_greater_heal():
    """Use greater heal potion"""
    global last_greater_heal, heal_pots_warning_shown

    # Check cooldown
    if time.time() * 1000 - last_greater_heal < GREATER_HEAL_COOLDOWN:
        return False

    pot = Items.FindByID(GREATER_HEAL_POT_ID, -1, Player.Backpack.Serial)
    if not pot:
        if not heal_pots_warning_shown:
            Mobiles.Message(Player.Serial, 33, "No heal pots!")
            heal_pots_warning_shown = True
        return False

    # Reset warning flag when we find a potion
    heal_pots_warning_shown = False
    Mobiles.Message(Player.Serial, 68, "Using greater heal!")
    Items.UseItem(pot)
    last_greater_heal = time.time() * 1000
    return True

def use_greater_cure():
    """Use greater cure potion"""
    global cure_pots_warning_shown

    pot = Items.FindByID(GREATER_CURE_POT_ID, -1, Player.Backpack.Serial)
    if not pot:
        if not cure_pots_warning_shown:
            Mobiles.Message(Player.Serial, 33, "No cure pots!")
            cure_pots_warning_shown = True
        return False

    # Reset the warning flag when we find a potion
    cure_pots_warning_shown = False
    Mobiles.Message(Player.Serial, 68, "Using cure...")
    Items.UseItem(pot)
    Misc.Pause(500)
    return True

def use_paralysis_cure():
    """Use paralysis cure item"""
    global last_paralysis_cure

    if time.time() * 1000 - last_paralysis_cure < 5000:
        return False

    cure = Items.FindByID(PARALYZE_CURE_ID, -1, Player.Backpack.Serial)
    if not cure:
        Mobiles.Message(Player.Serial, 33, "No para cures!")
        return False

    Journal.Clear()
    Mobiles.Message(Player.Serial, 53, "Using para pouch!")
    Items.UseItem(cure)
    Misc.Pause(500)

    if not Journal.Search("You are still paralyzed"):
        last_paralysis_cure = time.time() * 1000
        return True
    return False

def use_strength_potion():
    """Use greater strength potion"""
    global last_str_buff

    if time.time() * 1000 - last_str_buff < PVP_BUFF_COOLDOWN:
        return False

    pot = Items.FindByID(STRENGTH_POT_ID, -1, Player.Backpack.Serial)
    if not pot:
        return False

    Mobiles.Message(Player.Serial, 68, "Using strength!")
    Items.UseItem(pot)
    last_str_buff = time.time() * 1000
    return True

def use_agility_potion():
    """Use greater agility potion"""
    global last_agi_buff

    if time.time() * 1000 - last_agi_buff < PVP_BUFF_COOLDOWN:
        return False

    pot = Items.FindByID(AGILITY_POT_ID, -1, Player.Backpack.Serial)
    if not pot:
        return False

    Mobiles.Message(Player.Serial, 68, "Using agility!")
    Items.UseItem(pot)
    last_agi_buff = time.time() * 1000
    return True

def check_pvp_attack():
    """Check if we're being attacked by another player"""
    pvp_triggers = [
        "is attacking you",  # Main trigger for your shard
        "You are under attack!",  # Keep some backup triggers just in case
        "begins to move menacingly"
    ]

    for trigger in pvp_triggers:
        if Journal.Search(trigger):
            Mobiles.Message(Player.Serial, 38, "*** PVP ATTACK DETECTED ***")
            # Debug messages
            Mobiles.Message(Player.Serial, 43, "Attempting to use strength potion...")
            if use_strength_potion():
                Mobiles.Message(Player.Serial, 68, "Strength potion used successfully!")
            else:
                Mobiles.Message(Player.Serial, 33, "Failed to use strength potion!")

            Misc.Pause(200)  # Small delay between potions

            Mobiles.Message(Player.Serial, 43, "Attempting to use agility potion...")
            if use_agility_potion():
                Mobiles.Message(Player.Serial, 68, "Agility potion used successfully!")
            else:
                Mobiles.Message(Player.Serial, 33, "Failed to use agility potion!")

            Journal.Clear()
            return True
    return False

def check_health():
    """Check health and heal if needed"""
    health_percent = (Player.Hits / Player.HitsMax) * 100

    # Check if healing is complete
    check_bandage_healing()

    # If already bandaging, don't try to heal
    if is_bandaging():
        return

    # If health is critical, try greater heal first
    if health_percent <= HEALTH_THRESHOLD:
        used_heal = use_greater_heal()
        # Always try bandaging if health is critical, regardless of heal pot result
        if not is_bandaging():
            use_bandage()
    # Otherwise try to bandage if not at full health
    elif Player.Hits < Player.HitsMax:
        use_bandage()

def check_poison():
    """Check for poison and cure if needed"""
    global poison_warning_shown, last_poison_state

    if Player.Poisoned:
        # Check if this is a new poison application
        if not last_poison_state:
            Mobiles.Message(Player.Serial, 33, "POISON!")
            last_poison_state = True

        # If we're already bandaging, wait for current bandage to finish
        if is_bandaging():
            return

        # Try cure potion first
        if use_greater_cure():
            Misc.Pause(500)  # Give the potion time to work
            if not Player.Poisoned:  # If cure worked, we're done
                last_poison_state = False
                return

        # If we get here, either cure failed or we had no potions
        # Try bandages as backup if not already bandaging
        if not is_bandaging():
            Mobiles.Message(Player.Serial, 68, "Using bandage for poison...")
            use_bandage()
    else:
        # Reset states when not poisoned
        last_poison_state = False

def check_paralysis():
    """Check for paralysis and cure if needed"""
    if Player.Paralized:
        Mobiles.Message(Player.Serial, 38, "*** PARALYZED ***")
        Misc.Pause(100)  # Small pause before cure attempt
        use_paralysis_cure()

def main():
    Mobiles.Message(Player.Serial, 68, "Healer started!")
    Journal.Clear()

    try:
        while True:
            if check_pvp_attack():
                Misc.Pause(1000)  # Pause after PvP response
            if Player.Poisoned:
                check_poison()
                Misc.Pause(500)  # Reduced pause after poison check
            check_health()
            check_paralysis()
            Misc.Pause(100)

    except Exception as e:
        Mobiles.Message(Player.Serial, 33, f"Error: {e}")
        raise

if __name__ == "__main__":
    main()
