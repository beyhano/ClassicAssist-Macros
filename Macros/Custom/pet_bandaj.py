# Name: Pet Bandage (2 Pets) - ClassicAssist
# Description: Auto bandage up to 2 pets while they fight.
# Requirements: ClassicAssist.Avalonia, Python macros.
# Usage:
#   - First run: target pet1, then pet2 when prompted.
#   - Bandages (0x0E21) must be in your backpack.
#   - Run this macro in a loop (CA Loop checkbox) or bind to a hotkey.

BANDAGE_GRAPHIC = 0x0E21
COOLDOWN_MS = 6100

# Silence "Object found updated" spam from FindType.
# HeadMsg() calls still work; only internal "found/update" notices are hidden.
SetQuietMode(True)

# ---- Stop if dead ----
if Dead("self"):
    Stop()

# ---- Ensure pets are aliased (select in-game when missing) ----
if not FindAlias("pet1"):
    HeadMsg("Target Pet 1", "self", 33)
    PromptAlias("pet1")
    Stop()

if not FindAlias("pet2"):
    HeadMsg("Target Pet 2", "self", 33)
    PromptAlias("pet2")
    Stop()

# ---- Out of bandages? ----
if not FindType(BANDAGE_GRAPHIC, -1, "backpack"):
    HeadMsg("Out of Bandages", "self", 33)
    Stop()

# ---- Per-pet timers (ready on first run) ----
if not TimerExists("BandagePet1"):
    CreateTimer("BandagePet1")
    SetTimer("BandagePet1", COOLDOWN_MS)

if not TimerExists("BandagePet2"):
    CreateTimer("BandagePet2")
    SetTimer("BandagePet2", COOLDOWN_MS)

# ---- Try to heal each pet once per run ----
for p in ("pet1", "pet2"):
    if not FindAlias(p):
        continue

    # Skip if pet nearly full
    if Hits(p) >= MaxHits(p) - 5:
        continue

    # Per-pet cooldown
    if p == "pet1" and Timer("BandagePet1") < COOLDOWN_MS:
        continue
    if p == "pet2" and Timer("BandagePet2") < COOLDOWN_MS:
        continue

    # Must be within 3 tiles
    if not InRange(p, 3):
        HeadMsg("Pet out of range: " + p, "self", 33)
        continue

    # Apply bandage to this pet
    UseType(BANDAGE_GRAPHIC, -1, "backpack")
    WaitForTarget(2000)

    if not TargetExists():
        continue

    Target(p)
    HeadMsg("Healing " + p, "self", 33)

    if p == "pet1":
        SetTimer("BandagePet1", 0)
    else:
        SetTimer("BandagePet2", 0)

# ---- Wait for an in-progress bandage to finish ----
ClearJournal()

while Timer("BandagePet1") < COOLDOWN_MS or Timer("BandagePet2") < COOLDOWN_MS:
    if InJournal("finish applying the bandage", "system"):
        HeadMsg("Heal complete", "self", 88)
        break
    if InJournal("too far away", "system"):
        HeadMsg("Pet too far", "self", 44)
        break
    if InJournal("stay close enough", "system"):
        break
    if InJournal("you are able to resurrect", "system"):
        HeadMsg("Resurrection available", "self", 44)
        break
    Pause(100)

ClearJournal()