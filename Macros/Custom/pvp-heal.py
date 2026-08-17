# Name: PvP/PvE Heal
# Description: Bandaj + cure + heal potion
# Author: Mordor
# Era: Any

while not Dead('self'):
    # --- Cure (zehirlenmişse) ---
    if Poisoned('self'):
        UseType(0x0F09)
        Pause(300)
        Target('self')
        Pause(2000)

    # --- Bandaj (can azsa) ---
    if Hits('self') < MaxHits('self'):
        UseType(0x0E21)
        Pause(300)
        Target('self')
        Pause(8000)

    # --- Heal potion (can hala azsa) ---
    if Hits('self') < MaxHits('self'):
        UseType(0x0F09)
        Pause(300)
        Target('self')
        Pause(2000)

    Pause(500)
