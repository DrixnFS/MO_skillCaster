import time, threading, math, os
import pyautogui
from pynput.keyboard import Key, Listener

# JS-like setInterval function
class setInterval:
    def __init__(self, interval, action, name = '', bool_param = False, params = []):
        self.name = name
        self.interval = interval
        self.action = action
        self.bool_param = bool_param
        self.params = params
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.start()
        print('inicialized interval: ', self.name)

    def __setInterval(self):
        nextTime = time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()):
            nextTime+=self.interval
            self.action(self.bool_param, self.params)

    def cancel(self):
        print('removing interval: ', self.name)
        self.stopEvent.set()

# Class that handles the endless skill skilling
class SkillSkiller:
    def __init__(self):
        # add other skills if you want with the same syntax!
        self.skills = {
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
            # 'spurt':{
            #     'key': '@',
            #     'base_mana': 8,
            #     'cast_time': 1.2,
            #     'is_self_cast': True
            # },
        }

        # Sequence how the skills are casted
        self.skill_sequence = ['outburst', 'outburst', 'lesser_heal']

        # Editable fields based on the character this "macro" is used for
        self.total_mana = 207 # Total mana character have
        self.self_cast_key = 'e' # Key mapped to self cast skill
        self.cast_key = 'q' # Key mapped to cast skill on target
        self.sitdown_key = '#' # Key mapped to sitdown skill
        self.mental_focus_current_skill = 61 # Current Mental Focus skill level
        self.mana_regen_skill = 100 # Current Mana Regeneration skill level
        self.meditation_skill = 54 # Current meditation skill level


        # !!!! DO NOT EDIT ANYTHING UNDER THIS LINE IF YOU DO NOT PERFECTLY KNOW HOW EVERYTHING WORKS, ONLY CHANGE THE VARIABLES ABOVE TO ALTER THE BEHAVIOR !!! #

        #Script variables, do not edit if you dont know exactly what they do
        self.__mental_focus_rate = 0.5
        self.__idle_time = 1.2
        self.__mana_regen_rate = 2
        self.__mana_regen_timer = 3
        self.__current_mana = 0
        self.__current_mana_regen = 0
        self.__current_mana_regen_sitdown = 0

        pb = threading.Thread(target=self.__panicButton)
        pb.start()

        self.__setSkillsManaCost()
        print('!--- YOU HAVE 5 SECONDS TO ACTIVATE MORTAL ONLINE WINDOW ---!')
        time.sleep(5);

        self.castSkills();

    def __panicButton(self):
        def on_press(key):
            if(key == Key.f5):
                print('--Stopping the script based on user input--')
                os._exit(0)

        # Collect events until released
        with Listener(on_press=on_press,) as listener:
            listener.join()

    def __setSkillsManaCost(self):
        for skill in self.skills.keys():
            print('initializating skill: ', skill)
            if 'base_mana' not in self.skills[skill]:
                print('Invalidly setuped skill: ', skill);
                break;
            self.skills[skill]['mana_cost'] = math.floor(self.skills[skill]['base_mana'] - ((self.skills[skill]['base_mana'] / 100) * (self.__mental_focus_rate * self.mental_focus_current_skill)))

    def __doManaRegenTick(self, is_sitdown = False, params = []):
        percentage_bonus = 25.0 + (self.mana_regen_skill * 0.75)
        if is_sitdown:
            percentage_bonus += self.meditation_skill
            
        mana_regen_value = self.__mana_regen_rate + (percentage_bonus * (self.__mana_regen_rate / 100))
        if is_sitdown:
            self.__current_mana_regen_sitdown = mana_regen_value
        else:
            self.__current_mana_regen = mana_regen_value
        if self.__current_mana + mana_regen_value <= self.total_mana:
            self.__current_mana += mana_regen_value
        else:
            self.__current_mana += self.total_mana - self.__current_mana
        print('- Mana regen tick happened, regenerated ', mana_regen_value, ' mana');
        print('-- Current mana after tick ', self.__current_mana);

    def castSkills(self, bool_param = False, params = []):
        self.__current_mana = self.total_mana
        mana_regen_interval = setInterval(self.__mana_regen_timer, self.__doManaRegenTick, 'casting-mana-tick')
        while self.__current_mana > 0:
            print('enough mana, starting to cast all the skills')
            for skill in self.skill_sequence:
                if 'mana_cost' not in self.skills[skill]:
                    break;
                if self.__current_mana < self.skills[skill]['mana_cost']:
                    print('not enough mana to cast a skill', skill, ' sitting down...')
                    self.sitDown()
                    t=threading.Timer(0, mana_regen_interval.cancel)
                    t.start()
                    return False;

                print('casting skill: ', skill, ' mana cost: ', self.skills[skill]['mana_cost'])
                pyautogui.press(self.skills[skill]['key']);
                time.sleep(self.skills[skill]['cast_time'] + self.__idle_time)
                if(self.skills[skill]['is_self_cast']):
                    print('self casting the skill')
                    pyautogui.press(self.self_cast_key)
                else:
                    print('casting the skill')
                    pyautogui.press(self.cast_key)
                time.sleep(self.__idle_time)
                self.__current_mana -= self.skills[skill]['mana_cost']
                print('finished casting skill: ', skill, ' Current mana is: ', self.__current_mana)
                time.sleep(self.__idle_time)
        else:
            print('Mana have reached 0, sitting down')
            self.sitDown()
            t=threading.Timer(0, mana_regen_interval.cancel)
            t.start()

    def __doSitdown(self, bool_param = False, params = []):
        mana_to_refill = self.total_mana - self.__current_mana
        time_to_refill = (mana_to_refill / (self.__current_mana_regen + self.__current_mana_regen_sitdown)) * self.__mana_regen_timer
        print('sitting down now for: ', time_to_refill, ' seconds')

        pyautogui.press(self.sitdown_key)
        inter = setInterval(time_to_refill, self.castSkills, 'sitdown-wait-time')
        t=threading.Timer(time_to_refill, inter.cancel)
        t.start()
        mr=threading.Timer(time_to_refill, params[0].cancel)
        mr.start()
        mrs=threading.Timer(time_to_refill, params[1].cancel)
        mrs.start()
        time.sleep(4)

    def sitDown(self):
        mana_regen_interval = setInterval(self.__mana_regen_timer, self.__doManaRegenTick, 'casting-mana-tick')
        mana_regen_interval_sitdown = setInterval(self.__mana_regen_timer, self.__doManaRegenTick, 'casting-mana-sitdown-tick', True)

        sitdown_interval = setInterval(self.__mana_regen_timer + 1, self.__doSitdown, 'do-sitdown', False, [mana_regen_interval, mana_regen_interval_sitdown])
        sdi=threading.Timer(self.__mana_regen_timer + 1, sitdown_interval.cancel)
        sdi.start()


#Start the "macro"
SkillSkiller()