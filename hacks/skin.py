WEP = {
    #AR
    1: ['M4A1', 11100020, 11100018], #11100020 white 11100018 pink
    88: ['SCAR', 231100022, 231100021, 21100009],
    40: ['AK47', 101100029, 101100026], #101100027 == 101100029, 101100026 == 25 == 24
    72: ['KAG6', 141100011], #141100011 == 10 == 9
    91: ['VSS', 251100016], #251100016?250100101
    93: ['AR97', 271199002], #270100085?270100144?271199002
    98: ['AUG', 291100010, 291100011], #291100010 == 7 white 291100005 == 11 ==6 red, 
    101: ['MCX', 311199006], #311199006
    102: ['FAL', 321199005, 321199007], #321199005, 321199007
    144: ['FN2000'], #-
    
    #SNIPER
    77: ['M700', 181100020, 181100019, 181100018], #181100019 == 18 == 20
    103: ['KAR98', 331100003],
    71: ['KALA'], #-
    
    #SHOTGUN
    34: ['ORIGIN12'],
    79: ['MP155'],
    
    #SMG
    2: ['MP5', 21100011, 21100009], # 21199005 == 21100009 red
    # 38: ['VECTOR', 81199007], #81199007 great, 81100015 no!
    75: ['URB'], #-
    76: ['INP9'], #-
    90: ['P90', 241100012], #241100008, == 10 ==9 == 12 gold 11 nakali
    110: ['UZI'], #-
    
}

import random
from gclient.gameplay.logic_base.equips.equip_case import EquipCaseFactory
@HOOK(EquipCaseFactory, 0)
def Create(wid, *args, **kwargs):
    args = list(args)
    
    if wid in WEP:# and kwargs.get('is_fps_weapon', 1) == 1:
        wids = WEP[wid][1:]
        if wids: args[4] = random.choice(wids)

    result = EquipCaseFactory._Create(wid, *args, **kwargs)
    # if result:
        # result.show_guise_hit_effect = True # BAN
        # result.show_guise_bullet_trace = True # IDK
    
    return result

from gclient.gamesystem.uigunsmith.gunsmith_diy_window import GunSmithDiyWindow
@HOOK(GunSmithDiyWindow)
def ChangeGunGuise(self, *_, **__): return self._ChangeGunGuise(*_, **__)
