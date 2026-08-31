from System.Collections.Generic import List
from System import Int32
import sys

KINDLING_ID = 0x0DE1
CAMPFIRE_ID = 0x0DE3

COLOR_RED = 38
COLOR_GREENISH = 85

DEFAULT_SCRIPT_DELAY = 250
ITEM_INTERACTION_DELAY = 650
CREATE_CAMPFIRE_DELAY = 1000

if Player.GetRealSkillValue("Camping") < 50:
    Player.HeadMessage(COLOR_RED, "Skill too low, buy from NPC")
    sys.exit(99)

campFireFilter = Items.Filter()
campFireFilter.Enabled = True
campFireFilter.RangeMin = 0
campFireFilter.RangeMax = 2
campFireFilter.Graphics = List[Int32](CAMPFIRE_ID)

while Player.Connected and Player.GetRealSkillValue("Camping") < Player.GetSkillCap("Camping"):
    if not Items.FindByID(KINDLING_ID, -1, Player.Backpack.Serial, True):
        Player.HeadMessage(COLOR_RED, "No kindling found in backpack.")
        sys.exit(99)

    if not Timer.Check("CAMPFIRE_COOLDOWN"):
        Items.UseItemByID(KINDLING_ID, -1)
        Timer.Create("CAMPFIRE_COOLDOWN", CREATE_CAMPFIRE_DELAY)
        Misc.Pause(DEFAULT_SCRIPT_DELAY)

    campFires = Items.ApplyFilter(campFireFilter)
    if not campFires or len(campFires) < 1:
        Misc.Pause(DEFAULT_SCRIPT_DELAY)
        continue

    for campFire in campFires:
        Items.MoveOnGround(campFire.Serial, 1, campFire.Position.X + 1, campFire.Position.Y, campFire.Position.Z)
        Misc.Pause(ITEM_INTERACTION_DELAY)
    
    Misc.Pause(DEFAULT_SCRIPT_DELAY)

Player.HeadMessage(COLOR_GREENISH, "Skill maxed")