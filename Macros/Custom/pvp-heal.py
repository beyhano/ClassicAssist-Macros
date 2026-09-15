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

    # --- Bandaj (can azsa, süre Dex'e göre; Healing etkilemez) ---
    if Hits('self') < MaxHits('self'):
        UseType(0x0E21)
        WaitForTarget(2000)
        Target('self')
        dex = Dex()
        if dex >= 140:
            Pause(4000)
        elif dex >= 120:
            Pause(5000)
        elif dex >= 100:
            Pause(6000)
        elif dex >= 80:
            Pause(7000)
        else:
            Pause(8000)

    # --- Heal potion (can hala azsa) ---
    if Hits('self') < MaxHits('self'):
        UseType(0x0F09)
        Pause(300)
        Target('self')
        Pause(2000)

    Pause(500)
