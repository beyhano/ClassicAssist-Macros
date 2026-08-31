while Player.Connected and not Player.IsGhost and (Player.GetRealSkillValue("Hiding") < 100 or Player.GetRealSkillValue("Stealth") < 100):
    if Timer.Check("SKILL_COOLDOWN"):
        Misc.Pause(250)
        continue

    if Player.Visible or Player.GetRealSkillValue("Hiding") < 100:
        Player.UseSkill("Hiding")
    else:
        Player.UseSkill("Stealth")

    Timer.Create("SKILL_COOLDOWN", 10000)
    Misc.Pause(250)