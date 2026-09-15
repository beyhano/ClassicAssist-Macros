# Name: Self Heal (Bandage + Spirit Speak fallback)
# Description: Bandajla can doldurur; bandaj yoksa veya can %30 altindaysa Spirit Speak kullanir (Spirit Speak icin yakininda corpse gerekir).
# Author: AreS
# Era: Any

BANDAGE = 0x0E21
LAST_RESORT_HITS = 40

while not Dead('self'):
    if Hits('self') >= MaxHits('self'):
        Pause(500)
        continue

    # --- Son care: bandaj yoksa veya can 40 altindaysa Spirit Speak ---
    if Hits('self') < LAST_RESORT_HITS or not FindType(BANDAGE, -1, 'backpack'):
        UseSkill('Spirit Speak')
        Pause(2000)
        continue

    # --- Normal: bandaj (sure Dex'e gore; Healing etkilemez) ---
    UseType(BANDAGE)
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
