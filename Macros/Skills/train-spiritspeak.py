# Name: Train Spirit Speak
# Description: Spam Spirit Speak to cap. Gains are faster near corpses (it heals you when corpses are in range).
# Author: AreS
# Era: Any

GOAL = int(SkillCap('Spirit Speak'))
PING = 800

while not Dead('self') and Skill('Spirit Speak') < GOAL:
    UseSkill('Spirit Speak')
    Pause(1500 + PING)
