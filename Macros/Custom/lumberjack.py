# Name: Lumberjack
# Description: Etraftaki agaclari kes, odunlari pack llama'ya koy
# Shard: Troy UO

from ClassicAssist.UO.Data import Statics
from ClassicAssist.UO import UOMath
from Assistant import Engine
from System import Convert
import clr
clr.AddReference('System.Core')

print("=== TROY UO - LUMBERJACK ===")
print("Baltani hedef goster!")
PromptAlias('axe')
print("Pack llama'yi hedef goster!")
PromptAlias('llama')

logTypes = [0x1be0]

def move_to_llama():
    llama = GetAlias('llama')
    for log in logTypes:
        while FindType(log, -1, 'backpack'):
            MoveItem('found', llama)
            Pause(600)

def find_trees():
    trees = []
    px = Engine.Player.X
    py = Engine.Player.Y
    for x in range(px - 10, px + 10):
        for y in range(py - 10, py + 10):
            statics = Statics.GetStatics(Convert.ChangeType(Engine.Player.Map, int), x, y)
            if statics is None:
                continue
            for s in statics:
                if s.Name.Contains("tree"):
                    trees.append({'X': s.X, 'Y': s.Y})
    return trees

LLAMA = GetAlias('llama')
trees = find_trees()
if len(trees) == 0:
    HeadMsg("Agac bulunamadi!")
    Stop()

HeadMsg(str(len(trees)) + " agac bulundu")
ClearIgnoreList()

for t in trees:
    HeadMsg("Agaca gidiliyor: " + str(t['X']) + "," + str(t['Y']))
    Pathfind(t['X'] + 1, t['Y'], 0)
    Pause(5000)

    deneme = 0
    while deneme < 30:
        ClearJournal()

        axe = GetAlias('axe')
        if axe == '':
            PromptAlias('axe')
            Pause(500)
            deneme += 1
            continue

        # Oyuncunun agaca gore offset'ini hesapla
        dx = t['X'] - Engine.Player.X
        dy = t['Y'] - Engine.Player.Y

        HeadMsg("Offset: " + str(dx) + "," + str(dy))

        UseObject(axe)
        WaitForTarget(3000)

        if not TargetExists():
            HeadMsg("Imlec gelmedi! Yaklas...")
            Pathfind(t['X'] + 1, t['Y'], 0)
            Pause(3000)
            deneme += 1
            continue

        # Dinamik offset ile target et
        TargetTileOffsetResource(dx, dy, 0)
        Pause(2000)
        move_to_llama()

        if InJournal("not enough"):
            HeadMsg("Agac bitti")
            break
        if InJournal("fail") or InJournal("can't") or InJournal("too far"):
            HeadMsg("Kesemedi! Deniyorum...")
            deneme += 1
            continue

        deneme += 1
