# UO Unchained
# Mining Script which :
# - uses shovels
# - tinkers 3 shovels in case none is found in backpack
# - mines one single spot until no metal left to mine
# - smelts ore on firebeetle
# - transfers ingots (and found jewels and stuff) from backpack to pack animal
# - notifies you of the actual weight of stuff inside the pack animal
#
# ATTENTION: You must have your shovels and your tinker tools in your characters main backpack
#
#
# Things to do in future:
# - check for tinker tools => if just one is remaining, get iron ingots 
#    from pack animal and craft 2 more tinker tools
###############################################################################################################

# Setting the serials for your actually used animals (pack animal and fire beetle)
# Variable is set as a shared value, so if you restart the script during same mining session
# you do not have to select your animals again everytime

if Misc.CheckSharedValue("firebeetle"):
    localfirebeetle = Misc.ReadSharedValue("firebeetle")
else:
    localfirebeetle = Target.PromptTarget('Target your fire beetle:')
    Misc.SetSharedValue("firebeetle", localfirebeetle)

if Misc.CheckSharedValue("packbeetle"):
    localpackbeetle = Misc.ReadSharedValue("packbeetle")
else:
    localpackbeetle = Target.PromptTarget('Target your pack animal:')
    Misc.SetSharedValue("packbeetle", localpackbeetle)

# short pause and then setting the variable for the pack animals backpack
Misc.Pause(650)
beetlepack = Mobiles.FindBySerial(localpackbeetle).Backpack

# I have set the weightlimit slightly higher than what it actually is
# see what weightlimit suits you best
# you could set as well    weightlimit = Player.MaxWeight
weightlimit = (Player.MaxWeight + 20)

# setting the variables for Tinkers Tools and Shovels
var_tinkertools = 0x1EB8
var_shovel = 0x0F39 
var_ingot = 0x1BF2

# Jessies stuff to transfer from Player backpack to pack animal
juff = [0x1BF2,0x0EED,0x3193,0x3194,0x3195,0x0F10,0x0F28,0x3195,0x318F,0x0F80,0x3194,0x3195,0x3196,0x3197,0x0F16,0x3199,0x0F10,0x3190,0x2F5F,0x318F,0x0F10,0x0F0F,0x0F13,0x3193,0x0F18,0x3192,0x3191,0x3198,0x0F25,0x0F26,0x0F11,0x0F15]

# opening the backpack of our pack animal to see the contents
Misc.WaitForContext(localpackbeetle, 10000)
Misc.ContextReply(localpackbeetle, 8)
Misc.Pause(650)

# starting our mining circle  

Journal.Clear()
while not Journal.SearchByName( 'There is no metal here to mine.', 'System' ):
    if Items.BackpackCount(var_shovel, -1) > 0:
        shovel = Items.FindByID(var_shovel, -1, Player.Backpack.Serial)
        Target.TargetResource(shovel.Serial, "ore")
        Misc.Pause(400)
        shovel = Items.FindByID(var_shovel, -1, Player.Backpack.Serial)
    else:
        Player.HeadMessage(88,"No more shovels in backpack...making 3 now")
        # get 100 iron ingots from pack animal
        Misc.WaitForContext(localpackbeetle, 10000)
        Misc.ContextReply(localpackbeetle, 8)
        Misc.Pause(650)
        beetle = Mobiles.FindBySerial(localpackbeetle)
        iron_ingot = Items.FindByID( var_ingot, 0x0000, beetle.Backpack.Serial )
        Misc.Pause(100)
        Items.Move(iron_ingot,Player.Backpack.Serial,100)
        Misc.Pause(1100)
        # make 3 shovels
        shovel = Items.FindByID(var_shovel, -1, Player.Backpack.Serial)
        while Items.BackpackCount(var_shovel, -1) < 3:
                Items.UseItemByID(var_tinkertools, -1)
                Misc.Pause( 650 )
                Gumps.WaitForGump(0x38920abd,800)
                Gumps.SendAction(0x38920abd, 72)
                Gumps.WaitForGump(0x38920abd,800)
                Misc.Pause(650)
                Gumps.SendAction(0x38920abd, 0)
                Misc.Pause(650)
                shovel = Items.FindByID(var_shovel, -1, Player.Backpack.Serial)

# weight check after every dig...both ingame and reallife ;)
# when the set weightlimit is reached, stuff gets moved to the pack animal               
    if Player.Weight >= weightlimit:
        # smelt the ores on firebeetle
        types = [0x19B9,0x19B8,0x19BA,0x19B7]
        Player.HeadMessage( 44,"Smelting!")
        for t in Items.FindBySerial(Player.Backpack.Serial).Contains:
            if t.ItemID in types:
                Items.UseItem(t)
                Target.WaitForTarget(650,False)
                Target.TargetExecute( localfirebeetle ) 
                Misc.Pause( 650 )
        # move ingots, jewels and such stuff to pack animal        
        Player.HeadMessage( 44,"Moving stuff to pack animal")
        for t in Items.FindBySerial(Player.Backpack.Serial).Contains:
            if t.ItemID in juff:
                Items.Move( t, localpackbeetle, 0 )
                Misc.Pause( 800 )
        # now tell me the actual weight of the stuff inside the pack animal
        beetleweight = Mobiles.GetPropValue(localpackbeetle, "Weight")
        Player.HeadMessage(55, "Your pack animal carries: {0}".format(beetleweight))

# Tell the player when there is no metal left to mine 
# and have him move his char manually to another spot        
Player.HeadMessage(88, "Move on...this spot is sucked dry !")
Misc.Pause(1000)
