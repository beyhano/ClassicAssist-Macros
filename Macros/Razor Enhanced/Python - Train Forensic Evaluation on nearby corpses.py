corpseFilter = Items.Filter()
corpseFilter.Enabled = True
corpseFilter.RangeMin = 0
corpseFilter.RangeMax = 2
corpseFilter.IsCorpse = True

while Player.Connected and not Player.IsGhost and Player.GetRealSkillValue("Forensic Evaluation") < 100:
    if Timer.Check("SKILL_COOLDOWN"):
        Misc.Pause(250)
        continue

    corpses = Items.ApplyFilter(corpseFilter)
    if not corpses or len(corpses) < 1:
        Misc.Pause(250)
        continue

    for corpse in corpses:
        Player.UseSkill("Forensic Evaluation")
        Target.WaitForTarget(1000)
        Target.TargetExecute(corpse)
        Timer.Create("SKILL_COOLDOWN", 1000)
        break