# Name: Lumberjack
# Description: Etraftaki agaclari kes, odunlari pack llama'ya koy
# Shard: Troy UO

from ClassicAssist.UO.Data import Statics
from ClassicAssist.UO import UOMath
from Assistant import Engine
from System import Convert
from System import Random
import clr
clr.AddReference('System.Core')

print("=== TROY UO - LUMBERJACK ===")
print("Baltani hedef goster!")
PromptAlias('axe')
print("Pack llama'yi hedef goster!")
PromptAlias('llama')

logTypes = [0x1bdd, 0x1be0]
dirs = ['East','West','North','South','Northeast','Southeast','Southwest','Northwest']
rnd = Random()
dead = set()

def move_to_llama():
    llama = GetAlias('llama')
    if llama == '':
        HeadMsg("Pack llama secilmedi!")
        return
    UseObject(llama)
    Pause(800)
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
                    trees.append({'X': s.X, 'Y': s.Y, 'ID': s.ID})
    uniq = []
    seen = set()
    for t in trees:
        c = (t['X'], t['Y'])
        if c in seen:
            continue
        seen.add(c)
        uniq.append(t)
    return uniq

def chop_once(axe, ox, oy):
    """Bir tile'e TEK vurus. 'ok' / 'empty' / 'no' / 'notarget' doner."""
    ClearJournal()
    UseObject(axe)
    if not WaitForTarget(5000):
        CancelTarget()
        Pause(1000)
        return 'notarget'
    TargetTileOffsetResource(ox, oy, 0)
    Pause(2000)
    move_to_llama()
    if InJournal("not enough"):
        return 'empty'
    if InJournal("can't use an axe"):
        return 'no'
    return 'ok'

def chop_area():
    global dead
    trees = find_trees()
    kesilen = 0
    for t in trees:
        c = (t['X'], t['Y'])
        if c in dead:
            continue

        # Adaya en fazla 1 tile uzakliga kadar git
        deneme = 0
        while deneme < 6:
            if abs(t['X'] - Engine.Player.X) <= 1 and abs(t['Y'] - Engine.Player.Y) <= 1:
                break
            Pathfind(t['X'] + 1, t['Y'], 0)
            Pause(3000)
            deneme += 1
        if abs(t['X'] - Engine.Player.X) > 1 or abs(t['Y'] - Engine.Player.Y) > 1:
            dead.add(c)
            continue

        axe = GetAlias('axe')
        if axe == '':
            HeadMsg("Baltayi goster!")
            PromptAlias('axe')
            Pause(500)

        px = Engine.Player.X
        py = Engine.Player.Y
        offsets = [(t['X'] - px, t['Y'] - py)]
        for ox in (-1, 0, 1):
            for oy in (-1, 0, 1):
                if ox == 0 and oy == 0:
                    continue
                offsets.append((ox, oy))

        tried = set()
        agac_bitti = False
        for ox, oy in offsets:
            key = (ox, oy)
            if key in tried:
                continue
            tried.add(key)

            # Basarili offset'e bitene kadar vur; cursor sorunlarinda en fazla 3 yeniden dene
            offset_ok = False
            no_cursor = 0
            while True:
                r = chop_once(axe, ox, oy)
                if r == 'ok':
                    kesilen += 1
                    offset_ok = True
                    continue
                if r == 'empty':
                    kesilen += 1
                    agac_bitti = True  # agac tamamen tukendi
                    break
                if r == 'no':
                    break  # bu offset bos -> siradaki offset dene
                no_cursor += 1
                if no_cursor >= 3:
                    break

            if agac_bitti or offset_ok:
                # Agac tukendi ya da en az bir kez odun verdi -> isi bitti
                break

        dead.add(c)
        if kesilen > 0:
            HeadMsg("Agac islendi")
    return kesilen

ClearIgnoreList()

while True:
    kes = chop_area()
    if kes == 0:
        HeadMsg("Bolge bitti, uzaklasiyorum")
        d = dirs[rnd.Next(8)]
        for _ in range(10):
            Run(d)
            Pause(1200)
    else:
        Run(dirs[rnd.Next(8)])
        Pause(1500)
