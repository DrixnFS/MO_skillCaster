# MO_skillCaster

Mortal Online 2 Magic skill leveling macro

Currently there is a known bug that the macro works badly at low skills, as your skills go higher it gets much and much precise and in the end its pretty much 1to1 with the game. Currently testing what exactly causes the issue, seems like the mana regen works different, probably on smaller mana pools that the script was made for (200+)

IMPORTANT! Panic button has been added, now you can stop the script anytime by pressing F5 whenever the script is running
## How to use
- You need a Python 3 installed on your device (https://www.python.org/downloads/)
- After python 3 is on your device youll need pyautogui library (https://pyautogui.readthedocs.io/en/latest/) py -m install pyautogui
- After python 3 is on your device youll need pynput library (https://pypi.org/project/pynput/) py -m install pynput
- Then you simply have to open terminal in the folder where the script is located at, have MO2 running and execute the python file, all the instructions and logs will follow in the terminal

## How it works
Simply by editing your current level of specific skills and setting up what skills you want the macro to use and in what sequence, macro casts the skills and regens the mana at very VERY efficient way

## How to setup
- self.skills = {
            'outburst': {
                'key' : '!', # key under which the spell is mapped
                'base_mana': 26, # must be base mana_cost before any skill effect are applied to it
                'cast_time': 2.5, # game cast time of the skill, add 0.2-0.3 to it due to lag etc
                'is_self_cast': True # if True spell will be cast on self with the self_cast_key, otherwise cast on the target with cast_key
            },
            'lesser_heal':{
                'key': '$',
                'base_mana': 8,
                'cast_time': 1.5,
                'is_self_cast': True
            },
        }
- self.skills that can be found inside SkillSkiller class is used to define all the skills youll want the bot to be using, make sure you specify everything seen as described!
- self.skill_sequence = ['outburst', 'outburst', 'lesser_heal']
- self.skill_sequence determines the sequence in which the skills are casted, it goes from the first position to the last and then starts over, make sure the name used is EXACTLY the same as the one specificed in self.skills
-    self.total_mana = 207 # Total mana character have
-    self.self_cast_key = 'e' # Key mapped to self cast skill
-    self.cast_key = 'q' # Key mapped to cast skill on target
-    self.sitdown_key = '#' # Key mapped to sitdown skill
-    self.mental_focus_current_skill = 61 # Current Mental Focus skill level
-    self.mana_regen_skill = 100 # Current Mana Regeneration skill level
-    self.meditation_skill = 54 # Current meditation skill level