# Name: Smelt Ore from Pack Llama
# Description: Llama'daki ore'leri al -> pack'te erit -> kulceyi geri koy
# Shard: Troy UO

print("=== TROY UO - SMELT FROM LLAMA ===")
print("Pack llama'yi hedef goster!")
PromptAlias('llama')
print("Ocagi (forge) hedef goster!")
PromptAlias('forge')

oreTypes = [0x19b7, 0x19b8, 0x19b9, 0x19ba]
LLAMA = -1

def move_ore():
    # Llama acikken ground uzerinden ore'leri bulup pack'e at
    for ore_id in oreTypes:
        while FindType(ore_id, -1, 'ground'):
            MoveItem('found', 'backpack')
            Pause(500)

def smelt_ore():
    for ore_id in oreTypes:
        while FindType(ore_id, -1, 'backpack'):
            UseObject('found')
            WaitForTarget(5000)
            Target(GetAlias('forge'))
            Pause(2000)

def move_ingots():
    while FindType(0x1bf2, -1, 'backpack'):
        HeadMsg("Kulce: " + str(GetAlias('found')))
        Pause(500)
        break

ClearIgnoreList()
LLAMA = GetAlias('llama')

while True:
    HeadMsg("[1] Llama aciliyor...")
    UseObject(LLAMA)
    Pause(2000)

    HeadMsg("[2] Ore'ler aliniyor...")
    move_ore()

    HeadMsg("[3] Eritiliyor...")
    smelt_ore()

    HeadMsg("[4] Bekliyor...")
    Pause(3000)
