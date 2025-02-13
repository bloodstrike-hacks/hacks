import os, struct
# from imp.library import WorldToScreenPoint, IsVisible

FIFO_PATH = "/data/data/com.netease.newspike/cache/fifo"
if not os.path.exists(FIFO_PATH): os.mkfifo(FIFO_PATH)

from gclient.framework.entities.space import Space
from gclient.gameplay.util.replay_util import IsPlayerTeammate
from gclient.gameplay.logic_base.entities.combat_avatar import CombatAvatar

def EspUpdate(*_, **__): # CURRENT IMPLEMENTATION DOESNT LOG ERRORS THIS FUNCTION
    if not isinstance(Space._instance, Space): return
    if not Space._instance.entities: return
    
    entities = []
    for entityId, entity in Space._instance.entities.copy().items():
        if not isinstance(entity, CombatAvatar): continue
        if not getattr(entity, 'model_loaded', False): continue
        if not getattr(entity, 'model', None): continue
        if not entity.is_alive: continue
        if IsPlayerTeammate(entityId): continue
        
        # HIGHLIGH AND XRAY
        # param = highlight color
        # color2 = xray color
        # idk what param2 is
        entity.model.UseTechHighLightXray(param=(1,0,0), param2=(0,0,0,0), color2=(1,1,1))
        
        if entity.IsRobotCombatAvatar: continue
        if entity.is_dying_state: continue
        
        entityHeadPos = entity.model.GetBoneWorldPosition('biped Head')
        if not entityHeadPos: continue
        
        entityHeadPosx = WorldToScreenPoint(entityHeadPos)
        if entityHeadPosx.z <= 0.0: continue
        
        entities.append((entityHeadPosx[0], entityHeadPosx[1], 1.0 if IsVisible(Space._instance.camera.position, entityHeadPos, entity.id) else 0.0))
    
    # SENDING ESP DATA TO CPP

    count = len(entities)
    data = struct.pack(f"=I{count*3}f", count, *(c for vec in entities for c in vec))
    
    with open(FIFO_PATH, "wb", buffering=0) as fifo: fifo.write(data)
    
from gclient.framework.util.story_tick import StoryTick
StoryTick._instance.Add(EspUpdate, 60) # fps = 60
