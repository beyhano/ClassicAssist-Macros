# Name: Train Necromancy (ServUO)
# Description: Train Necromancy to cap using ServUO spell requirements. Uses cheapest no-fizzle spell per skill bracket, meditates when low mana.
# Author: AreS
# Era: Any

GOAL = int(SkillCap('Necromancy'))
PING = 800

PromptAlias('train_target')
PromptAlias('weapon')


def cast_train(name, mana_cost, needs_target):
    if Mana('self') < mana_cost:
        if not BuffExists('Active Meditation'):
            UseSkill('Meditation')
        Pause(2000)
        return False
    Cast(name)
    if needs_target:
        WaitForTarget(1500)
        Target(GetAlias('train_target'))
    Pause(2000 + PING)
    return True


while not Dead('self') and Skill('Necromancy') < GOAL:
    s = Skill('Necromancy')
    if s < 20:
        # Curse Weapon hedefi silah itemi, mobile degil
        if Mana('self') >= 7:
            Cast('Curse Weapon')
            WaitForTarget(1500)
            Target(GetAlias('weapon'))
            Pause(2000 + PING)
        else:
            if not BuffExists('Active Meditation'):
                UseSkill('Meditation')
            Pause(2000)
    elif s < 40:
        # Pain Spike: 20 req, 5 mana, cheapest spam 20-40
        cast_train('Pain Spike', 5, True)
    elif s < 50:
        # Horrific Beast: 40 req, 11 mana, no target, no fizzle stalls
        cast_train('Horrific Beast', 11, False)
    elif s < 60:
        # Poison Strike: 50 req, 17 mana
        cast_train('Poison Strike', 17, True)
    elif s < 65:
        # Wither: 60 req, 23 mana, PBAoE, no target needed
        cast_train('Wither', 23, False)
    elif s < 70:
        # Strangle: 65 req, 29 mana
        cast_train('Strangle', 29, True)
    else:
        # Lich Form: 70 req, 23 mana, no target, trains to cap
        cast_train('Lich Form', 23, False)
