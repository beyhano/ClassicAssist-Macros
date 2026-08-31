// CraftingTrainer.cs
using System;
using System.Collections.Generic;
using System.Linq;
using RazorEnhanced;
using System.Windows.Forms;

namespace RazorScripts
{
    public class CraftingTrainer
    {
        private Dictionary<string, int> _craftSkills = new Dictionary<string, int>
        {
            {"Tailoring", 100},
            {"Blacksmithy", 100},
            {"Alchemy", 100},
            {"Tinkering", 100},
            {"Bowcraft/Fletching", 100},
            {"Inscription", 100},
            {"Carpentry", 100},
            {"Cooking", 100}
        };

        private Dictionary<string, List<CraftItem>> _craftHolder = new Dictionary<string, List<CraftItem>>();

        public void Run()
        {
            ShowSkillSelectorForm();
            Setup();
            UpdateGump("");
            bool training = true;
            while (training)
            {
                training = false;
                foreach (var craft in _craftHolder)
                {
                    if (_craftSkills[craft.Key] <= 0)
                        continue;

                    if (Player.GetRealSkillValue(craft.Key) < _craftSkills[craft.Key])
                    {
                        TrainCraft(craft.Key, singlePass: true);
                        training = true;
                    }
                }
            }
            UpdateGump("", true);
        }

        private void ShowSkillSelectorForm()
        {
            Form form = new Form()
            {
                Width = 300,
                Height = 400,
                Text = "Crafting Trainer - Select Skills"
            };

            var skillCheckboxes = new Dictionary<string, CheckBox>();
            int top = 20;
            foreach (var skill in _craftSkills.Keys.ToList())
            {
                CheckBox chk = new CheckBox()
                {
                    Text = skill,
                    Checked = _craftSkills[skill] > 0,
                    Top = top,
                    Left = 20,
                    Width = 200
                };
                form.Controls.Add(chk);
                skillCheckboxes[skill] = chk;
                top += 25;
            }

            Button startButton = new Button()
            {
                Text = "Start",
                Top = top + 10,
                Left = 100,
                Width = 80
            };
            startButton.Click += (sender, e) => { form.DialogResult = DialogResult.OK; form.Close(); };
            form.Controls.Add(startButton);

            form.ShowDialog();

            foreach (var skill in skillCheckboxes.Keys)
            {
                _craftSkills[skill] = skillCheckboxes[skill].Checked ? 100 : 0;
            }
        }

        private void Setup()
        {
            // Tailoring recipes
            _craftHolder.Add("Tailoring", new List<CraftItem>
            {
                new CraftItem { SkillLevel = 42.0, Tool="Sewing Kit", GumpId=949095101, CategoryButtonId=29, ItemButtonId=16, ItemType=0x1EFD },
                new CraftItem { SkillLevel = 54.0, Tool="Sewing Kit", GumpId=949095101, CategoryButtonId=29, ItemButtonId=44, ItemType=0x1515 },
                new CraftItem { SkillLevel = 74.6, Tool="Sewing Kit", GumpId=949095101, CategoryButtonId=29, ItemButtonId=51, ItemType=0x1F03 },
                new CraftItem { SkillLevel = 99.6, Tool="Sewing Kit", GumpId=949095101, CategoryButtonId=1,  ItemButtonId=37, ItemType=0x175D }
            });

            // Alchemy recipes
            _craftHolder.Add("Alchemy", new List<CraftItem>
            {
                new CraftItem { SkillLevel = 45.0, Tool="Mortar and Pestle", GumpId=949095101, CategoryButtonId=22, ItemButtonId=2,  ItemType=0x0F0A },
                new CraftItem { SkillLevel = 55.0, Tool="Mortar and Pestle", GumpId=949095101, CategoryButtonId=22, ItemButtonId=9,  ItemType=0x0F0B },
                new CraftItem { SkillLevel = 90.0, Tool="Mortar and Pestle", GumpId=949095101, CategoryButtonId=22, ItemButtonId=16, ItemType=0x0F0C },
                new CraftItem { SkillLevel = 98.0, Tool="Mortar and Pestle", GumpId=949095101, CategoryButtonId=22, ItemButtonId=23, ItemType=0x0F0D }
            });

            // Tinkering recipes
            _craftHolder.Add("Tinkering", new List<CraftItem>
            {
                new CraftItem { SkillLevel = 30.0, Tool="Tinker Tools", GumpId=949095101, CategoryButtonId=23, ItemButtonId=5,  ItemType=0x1EB8 },
                new CraftItem { SkillLevel = 50.0, Tool="Tinker Tools", GumpId=949095101, CategoryButtonId=23, ItemButtonId=20, ItemType=0x0E7E },
                new CraftItem { SkillLevel = 70.0, Tool="Tinker Tools", GumpId=949095101, CategoryButtonId=23, ItemButtonId=14, ItemType=0x1EB9 },
                new CraftItem { SkillLevel = 90.0, Tool="Tinker Tools", GumpId=949095101, CategoryButtonId=23, ItemButtonId=9,  ItemType=0x1EB9 }
            });

            // Blacksmithy recipes
            _craftHolder.Add("Blacksmithy", new List<CraftItem>
            {
                new CraftItem { SkillLevel = 30.0, Tool="Smith's Hammer", GumpId=949095101, CategoryButtonId=21, ItemButtonId=0,  ItemType=0x13FB },
                new CraftItem { SkillLevel = 45.0, Tool="Smith's Hammer", GumpId=949095101, CategoryButtonId=21, ItemButtonId=8,  ItemType=0x1403 },
                new CraftItem { SkillLevel = 60.0, Tool="Smith's Hammer", GumpId=949095101, CategoryButtonId=21, ItemButtonId=15, ItemType=0x1438 },
                new CraftItem { SkillLevel = 75.0, Tool="Smith's Hammer", GumpId=949095101, CategoryButtonId=21, ItemButtonId=19, ItemType=0x13B9 },
                new CraftItem { SkillLevel = 90.0, Tool="Smith's Hammer", GumpId=949095101, CategoryButtonId=21, ItemButtonId=26, ItemType=0x141B }
            });

            // Carpentry recipes
            _craftHolder.Add("Carpentry", new List<CraftItem>
            {
                new CraftItem { SkillLevel = 30.0, Tool="Carpenter's Tools", GumpId=949095101, CategoryButtonId=24, ItemButtonId=0,  ItemType=0x0E7D },
                new CraftItem { SkillLevel = 45.0, Tool="Carpenter's Tools", GumpId=949095101, CategoryButtonId=24, ItemButtonId=5,  ItemType=0x0E7E },
                new CraftItem { SkillLevel = 60.0, Tool="Carpenter's Tools", GumpId=949095101, CategoryButtonId=24, ItemButtonId=6,  ItemType=0x0E7F },
                new CraftItem { SkillLevel = 75.0, Tool="Carpenter's Tools", GumpId=949095101, CategoryButtonId=24, ItemButtonId=7,  ItemType=0x0E80 },
                new CraftItem { SkillLevel = 90.0, Tool="Carpenter's Tools", GumpId=949095101, CategoryButtonId=24, ItemButtonId=12, ItemType=0x0E83 }
            });

            // Bowcraft/Fletching recipes
            _craftHolder.Add("Bowcraft/Fletching", new List<CraftItem>
            {
                new CraftItem { SkillLevel = 30.0, Tool="Fletcher's Tools", GumpId=949095101, CategoryButtonId=25, ItemButtonId=0,  ItemType=0x0F3F },
                new CraftItem { SkillLevel = 50.0, Tool="Fletcher's Tools", GumpId=949095101, CategoryButtonId=25, ItemButtonId=1,  ItemType=0x0F3B },
                new CraftItem { SkillLevel = 70.0, Tool="Fletcher's Tools", GumpId=949095101, CategoryButtonId=25, ItemButtonId=6,  ItemType=0x13B2 },
                new CraftItem { SkillLevel = 90.0, Tool="Fletcher's Tools", GumpId=949095101, CategoryButtonId=25, ItemButtonId=7,  ItemType=0x13FD }
            });

            // Inscription recipes
            _craftHolder.Add("Inscription", new List<CraftItem>
            {
                new CraftItem { SkillLevel = 30.0, Tool="Scribe's Pen", GumpId=949095101, CategoryButtonId=27, ItemButtonId=1,  ItemType=0x1F2E },
                new CraftItem { SkillLevel = 50.0, Tool="Scribe's Pen", GumpId=949095101, CategoryButtonId=27, ItemButtonId=3,  ItemType=0x1F2F },
                new CraftItem { SkillLevel = 70.0, Tool="Scribe's Pen", GumpId=949095101, CategoryButtonId=27, ItemButtonId=16, ItemType=0x1F3C },
                new CraftItem { SkillLevel = 90.0, Tool="Scribe's Pen", GumpId=949095101, CategoryButtonId=27, ItemButtonId=29, ItemType=0x1F4A }
            });

            // Cooking recipes
            _craftHolder.Add("Cooking", new List<CraftItem>
            {
                new CraftItem { SkillLevel = 30.0, Tool="Skillet", GumpId=949095101, CategoryButtonId=26, ItemButtonId=0,  ItemType=0x097B },
                new CraftItem { SkillLevel = 50.0, Tool="Skillet", GumpId=949095101, CategoryButtonId=26, ItemButtonId=10, ItemType=0x09B7 },
                new CraftItem { SkillLevel = 70.0, Tool="Skillet", GumpId=949095101, CategoryButtonId=26, ItemButtonId=15, ItemType=0x097E },
                new CraftItem { SkillLevel = 90.0, Tool="Skillet", GumpId=949095101, CategoryButtonId=26, ItemButtonId=18, ItemType=0x1608 }
            });
        }

        private void TrainCraft(string craftKey, bool singlePass = false)
        {
            var craftList = _craftHolder[craftKey].OrderBy(c => c.SkillLevel).ToList();
            var skillCap = _craftSkills[craftKey];
            while (Player.GetRealSkillValue(craftKey) < skillCap)
            {
                double currentSkill = Player.GetRealSkillValue(craftKey);
                UpdateGump(craftKey);
                CraftItem itemToCraft = null;
                foreach (var item in craftList)
                {
                    if (currentSkill < item.SkillLevel)
                    {
                        itemToCraft = item;
                        break;
                    }
                }
                if (itemToCraft == null && craftList.Count > 0)
                    itemToCraft = craftList.Last();

                if (itemToCraft != null)
                {
                    CraftItemAction(itemToCraft);
                    Misc.Pause(2000);
                    if (craftKey == "Tailoring")
                        RecycleItems(itemToCraft.ItemType);
                    else if (craftKey == "Alchemy" || craftKey == "Tinkering" || craftKey == "Blacksmithy" ||
                             craftKey == "Bowcraft/Fletching" || craftKey == "Inscription" ||
                             craftKey == "Carpentry" || craftKey == "Cooking")
                        UseCraftedItem(itemToCraft.ItemType);
                }
                else
                {
                    Misc.SendMessage("No suitable item found for your current skill level.");
                }

                Misc.Pause(itemToCraft?.WaitTime ?? 3000);
                if (singlePass) break;
            }
        }

        private void CraftItemAction(CraftItem item)
        {
            // Determine the correct tool ID based on the item.Tool string.
            int toolId = 0;
            switch (item.Tool)
            {
                case "Sewing Kit":
                    toolId = 0x0F9D;
                    break;
                case "Mortar and Pestle":
                    toolId = 0x0E9B;
                    break;
                case "Tinker Tools":
                    toolId = 0x1EB8;
                    break;
                case "Smith's Hammer":
                    toolId = 0x13FB;
                    break;
                case "Carpenter's Tools":
                    toolId = 0x0E7D;
                    break;
                case "Fletcher's Tools":
                    toolId = 0x0F3F;
                    break;
                case "Scribe's Pen":
                    toolId = 0x1F2E;
                    break;
                case "Skillet":
                    toolId = 0x097B;
                    break;
                default:
                    toolId = 0;
                    break;
            }

            // Find the correct tool in the player's backpack.
            var tool = Player.Backpack.Contains.Find(i => i.ItemID == toolId);
            if (tool == null)
            {
                Misc.SendMessage("Crafting tool not found.");
                return;
            }
            if (Gumps.HasGump((uint)item.GumpId))
            {
                Gumps.CloseGump((uint)item.GumpId);
                Misc.Pause(200);
            }
            Items.UseItem(tool);
            if (WaitForGump((uint)item.GumpId, 3000))
            {
                Gumps.SendAction((uint)item.GumpId, (int)item.CategoryButtonId);
                Misc.Pause(500);
                Gumps.SendAction((uint)item.GumpId, (int)item.ItemButtonId);
                Misc.Pause(500);
                Gumps.SendAction((uint)item.GumpId, (int)item.MakeButtonId);
            }
            else
            {
                Misc.SendMessage("Gump did not open correctly.");
            }
        }

        private void RecycleItems(int itemType)
        {
            var scissors = Player.Backpack.Contains.FirstOrDefault(i => i.ItemID == 0x0F9F);
            if (scissors == null)
            {
                Misc.SendMessage("No scissors found in backpack.");
                return;
            }
            var item = Player.Backpack.Contains.Where(i => i.ItemID == itemType)
                          .OrderByDescending(i => i.Serial)
                          .FirstOrDefault();
            if (item != null)
            {
                Items.UseItem(scissors);
                Target.WaitForTarget(1000);
                Target.TargetExecute(item);
                Misc.Pause(500);
            }
        }

        private void UseCraftedItem(int itemType)
        {
            var item = Player.Backpack.Contains.FirstOrDefault(i => i.ItemID == itemType);
            if (item != null)
            {
                Items.UseItem(item);
                Misc.Pause(500);
            }
        }

        private static bool WaitForGump(uint gumpId, int timeout = 5000)
        {
            if (!Gumps.HasGump(gumpId))
            {
                for (var i = 0; i < timeout / 10; i++)
                {
                    if (Gumps.HasGump(gumpId))
                        return true;
                    Misc.Pause(10);
                }
                return false;
            }
            // Allow time for the gump to properly close/open
            for (var i = 0; i < timeout / 10; i++)
            {
                if (Gumps.HasGump(gumpId) || Gumps.CurrentGump() == gumpId)
                    return true;
                Misc.Pause(10);
            }
            Misc.Pause(200);
            return Gumps.HasGump(gumpId);
        }

        private void UpdateGump(string currentSkill, bool finished = false)
        {
            var bar = Gumps.CreateGump();
            bar.buttonid = -1;
            bar.gumpId = 123456789;
            bar.serial = (uint)Player.Serial;
            bar.x = 500;
            bar.y = 500;

            var skillsToTrain = _craftSkills.Where(skill => skill.Value > 0).Select(skill => skill.Key).ToList();
            Gumps.AddBackground(ref bar, 0, 0, 300, 50 + (skillsToTrain.Count * 35), 2620);
            Gumps.AddLabel(ref bar, 10, 10, 203, "Crafting Trainer");

            var index = 0;
            foreach (var skill in skillsToTrain)
            {
                var currentValue = Player.GetRealSkillValue(skill);
                var cap = _craftSkills[skill];
                var icon = skill == currentSkill ? 2152 : (currentValue >= cap ? 5826 : 5832);
                Gumps.AddImage(ref bar, 10, 35 + (index * 30), icon);
                Gumps.AddLabel(ref bar, 60, 35 + (index * 30), 203, $"{skill}: {currentValue:F1}/{cap}");
                index++;
            }

            if (finished)
                Gumps.AddLabel(ref bar, 75, 35 + (index * 30), 704, "ALL DONE!");

            Gumps.CloseGump(123456789);
            Gumps.SendGump(bar, 500, 500);
        }
    }

    public class CraftItem
    {
        public double SkillLevel { get; set; }
        public string Tool { get; set; }
        public int GumpId { get; set; }
        public uint CategoryButtonId { get; set; }
        public uint ItemButtonId { get; set; }
        public uint MakeButtonId { get; set; } = 21;
        public int WaitTime { get; set; } = 3000;
        public int ItemType { get; set; }
    }
}
