# Name: Mining Random Macro
# Description: MACRO MINER RANDOM - TROY UO
# Shard: Troy UO
# Date: 2026-07-19

import System
from System import Random

print("=== TROY UO - MINER RANDOM ===")
print("Once kazmani hedef goster!")
PromptAlias('pickaxe')
print("YEDEK kazma sandigini hedef goster (bitince otomatik alir)!")
PromptAlias('pickaxe_chest')
print("Simdi pack llama'yi hedef goster!")
PromptAlias('Packlhama')

# Kazma grafik ID'leri (ServUO: 0xE86/0xE85, bazi shard'lar 0xf39)
pickaxeIDs = [0x0E86, 0x0E85, 0x0f39]

def get_new_pickaxe():
    """Sandiktan yeni kazma al"""
    for pid in pickaxeIDs:
        if FindType(pid, -1, 'pickaxe_chest'):
            MoveItem('found', 'backpack')
            Pause(500)
            # Kazmayi backpack'te bul ve alias yap
            for pid2 in pickaxeIDs:
                if FindType(pid2, -1, 'backpack'):
                    SetAlias('pickaxe', GetAlias('found'))
                    HeadMsg("Yeni kazma alindi!")
                    return True
    HeadMsg("Sandikta kazma yok! Elle koy...")
    PromptAlias('pickaxe')
    return False

def guardar():
    HeadMsg("Guardando minerios...")
    llama = GetAlias('Packlhama')
    if llama == '':
        HeadMsg("Pack llama secilmedi!")
        return
    UseObject(llama)
    Pause(800)
    while FindType(0x19b9, -1, 'backpack'):
        ore = GetAlias('found')
        MoveItem(ore, llama)
        Pause(500)

def Mine():
    HeadMsg("Minerando...")
    ClearJournal()
    while not InJournal('There is no metal here to mine.'):
        if InJournal('You have worn out your tool!'):
            ClearJournal()
            HeadMsg("Kazma bitti! Yedek aliniyor...")
            get_new_pickaxe()
            Pause(500)
        UseObject(GetAlias('pickaxe'))
        WaitForTarget(2000)
        TargetTileOffsetResource(0, 0, 0)
        Pause(1200)
        if Weight() >= 300:
            guardar()
    HeadMsg("Proximo local...")

# --- Ana dongu ---
dirs = ['East','West','North','South','Northeast','Southeast','Southwest','Northwest']
rnd = Random()

while True:
    Mine()
    Run(dirs[rnd.Next(8)])
    for i in range(3):
        Run(Direction('self'))
