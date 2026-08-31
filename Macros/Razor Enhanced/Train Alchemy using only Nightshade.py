# Train Alchemy using only Poisons by Jaseowns
# UO Unchained
# BE IN POISON MASTERY TO BECOME IMMUNE TO POISONS
def TrainAlchemy():
        
    if Player.GetRealSkillValue("Alchemy") == 0:
        Player.HeadMessage(34,"We do not have any skill yet - go train at vendor")
        return
        
    if Player.GetRealSkillValue("Alchemy") == Player.GetSkillCap("Alchemy"):
        Player.HeadMessage(68,"We did it!")
        return
        
    gained = True
    while gained == True:    
        Player.HeadMessage(68,"Lesser")
        gained = CraftPoisonPotion(1, 2)
        
    gained = True
    while gained == True:    
        Player.HeadMessage(68,"Regular")
        gained = CraftPoisonPotion(2, 9)
    
    gained = True
    while gained == True:    
        Player.HeadMessage(68,"Greater")
        gained = CraftPoisonPotion(4, 16)
        
#    gained = True
#    while gained == True:    
#        Player.HeadMessage(68,"Deadly")
#        gained = CraftPoisonPotion(8, 23)

    TrainAlchemy()


def CraftPoisonPotion(count,gump):
    
    if Player.GetRealSkillValue("Alchemy") == Player.GetSkillCap("Alchemy"):
        Player.HeadMessage(68,"We did it!")
        return False
    
    emptyBottle = Items.FindByID(0x0F0E,-1,Player.Backpack.Serial,-1)
    pestal = Items.FindByID(0x0E9B,-1,Player.Backpack.Serial,-1)
    if pestal is None:
        Player.HeadMessage(34,"We do not have a tool")
        Misc.Pause(1000)
        CraftPoisonPotion(count,gump)
        
    if emptyBottle is None:
        Player.HeadMessage(34,"We do not have an empty bottle")
        DrinkPoisonPotion()
        Misc.Pause(1000)
        CraftPoisonPotion(count,gump)
    
    nightShadeCount = Items.BackpackCount(0x0F88,-1)
    if nightShadeCount >= count:
        Journal.Clear()
        Items.UseItem(pestal)
        Gumps.WaitForGump(0x38920abd, 1000)
        Gumps.SendAction(0x38920abd, 22)
        Gumps.WaitForGump(0x38920abd, 10000)
        Gumps.SendAction(0x38920abd, gump)
        Timer.Create("skillGainTimer",10000)
        while Timer.Check("skillGainTimer") > 0:
            Misc.Pause(200)
            if Journal.Search("Gain Chance (Alchemy)"):
                Player.HeadMessage(89,"we gained bro!")
                DrinkPoisonPotion()
                return True
        return False
    else:
        Player.HeadMessage(34,"We are out of nigthshade")
        Misc.Pause(1000)
        CraftPoisonPotion(count,gump)
            
def DrinkPoisonPotion():
    potion = Items.FindByID(0x0F0A,-1,Player.Backpack.Serial,-1)
    if potion is None:
        return
    Items.UseItem(potion)
    Misc.Pause(650)
    

TrainAlchemy()