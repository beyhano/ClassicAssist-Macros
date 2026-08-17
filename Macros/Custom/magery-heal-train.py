# Name: Magery + Heal train
# Description: Heal first if low, then cast best spell
# Author: Mordor
# Era: Any

class SpellInfo:
    def __init__(self, name, mana_cost, min_skill, delay_in_ms):
        self.name = name
        self.mana_cost = mana_cost
        self.min_skill = min_skill
        self.delay_in_ms = delay_in_ms

PromptAlias('spell_target')
magery_cap = SkillCap('Magery')
ping = 800

while not Dead('self') and Skill('Magery') < magery_cap:
    while Hits('self') < MaxHits('self'):
        UseType(0x0E21)
        Pause(500)
        Target('self')
        Pause(8000)

    spells = [
        SpellInfo('Fireball', 7, 30, 1000),
        SpellInfo('Lightning', 10, 45, 1250),
        SpellInfo('Paralyze', 12, 55, 1500),
        SpellInfo('Invisibility', 18, 65, 1750),
        SpellInfo('Flame Strike', 30, 75, 2000),
        SpellInfo('Earthquake', 40, 90, 2250),
    ]

    current_spell = None
    for spell in spells:
        if spell.min_skill <= Skill('Magery'):
            current_spell = spell

    if Mana('self') > current_spell.mana_cost:
        Cast(current_spell.name, GetAlias('spell_target'))
        Pause(current_spell.delay_in_ms + ping)
    else:
        UseSkill('Meditation')
        timeout = 0
        while Mana('self') < MaxMana('self') and timeout < 30:
            Pause(1000)
            timeout += 1
