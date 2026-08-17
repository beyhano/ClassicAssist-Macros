# Name: Smelt Ore
# Description: Sandiktaki cevherleri eritip kulceyi sandiga koy
# Shard: Troy UO

print("=== TROY UO - SMELT ORE ===")
print("Cevher sandigini hedef goster!")
PromptAlias('ore_chest')
print("Ocagi (forge) hedef goster!")
PromptAlias('forge')

# Cevher tipleri
oreTypes = [0x19b7, 0x19b8, 0x19b9, 0x19ba]

ClearIgnoreList()

oreNames = {
    0x19b7: "Dull Copper",
    0x19b8: "Shadow Iron",
    0x19b9: "Iron",
    0x19ba: "Copper"
}

while True:
    for ore in oreTypes:
        buldu = FindType(ore, -1, 'ore_chest')
        if buldu:
            ad = oreNames.get(ore, hex(ore))
            HeadMsg("[BULUNDU] " + ad)
            Pause(300)
            UseObject('found')
            hedef_geldi = WaitForTarget(5000)
            if not hedef_geldi:
                HeadMsg("[HATA] Hedef imleci gelmedi! Forge'a tikla once")
                Pause(2000)
                break
            forge = GetAlias('forge')
            if forge == '':
                HeadMsg("[HATA] Forge secilmemis! Yeniden hedef goster")
                PromptAlias('forge')
                break
            Target(forge)
            HeadMsg("[ERITILDI] " + ad)
            Pause(2000)
            # Kulceyi sandiga at (yerden al)
            while FindType(0x1bf2, 3):
                MoveItem('found', 'ore_chest')
                Pause(500)
                IgnoreObject('found')
            # Kulceyi sandiga at (backpack'ten)
            while FindType(0x1bf2, -1, 'backpack'):
                HeadMsg("[KULCE] Sandiga atiliyor...")
                MoveItem('found', 'ore_chest')
                Pause(500)
                IgnoreObject('found')
    Pause(1000)
