from gclient.framework.entities.space import Space
from gclient.gameplay.util.replay_util import IsPlayerTeammate
from gclient.gameplay.logic_base.entities.combat_avatar import CombatAvatar

BONES = {
    'Head': {
        'name': 'Head',
        'scale': (1.1000000124848068, 1.099999922508427, 1.0999998395187762), # CHANGES DEPENDING ON HERO/SKIN
        'bone_name': 'biped Head',
        'dmg_name': 'head_damage'
    },
    'UpperTop': {
        'name': 'UpperTop',
        'scale': (1.100007990904212, 1.1001234035373453, 1.1001123001942972),
        'bone_name': 'biped Spine',
        'dmg_name': 'uppertop_damage'
    },
}

from gclient.framework.util.gyroscope import GyroscopePoseCombat
@HOOK(GyroscopePoseCombat, 0)
def GyroscopeTick(self, *_, **__):
    localEntity = Space._instance.owner.combat_avatar
    if not localEntity: return self._GyroscopeTick(*_, **__)
    if not localEntity.is_shooting and not localEntity.is_ads: return self._GyroscopeTick(*_, **__)
    
    curWeapon = localEntity.GetCurWeapon()
    if not curWeapon: return self._GyroscopeTick(*_, **__)
    
    targetEntity = targetEntityPos = targetEntityPosx = None
    targetDistance = 100
    
    for entityId, entity in Space._instance.entities.copy().items():
        if not isinstance(entity, CombatAvatar): continue
        if not entity.is_alive: continue
        if IsPlayerTeammate(entityId): continue
        
        entityPos = entity.model.GetBoneWorldPosition('biped Head')
        if not entityPos: continue
        
        entityPosx = WorldToScreenPoint(entityPos)
        if entityPosx.z <= 0.0: continue
        
        distance = Distance2D((entityPosx.x, entityPosx.y), (2400/2, 1080/2))
        if distance < targetDistance:
            targetDistance = distance
            targetEntity, targetEntityPos, targetEntityPosx = entity, entityPos, entityPosx
    
    if not targetEntity: return self._GyroscopeTick(*_, **__)
    # if targetEntity.IsRobotCombatAvatar: return self._GyroscopeTick(*_, **__)
    if targetEntity.is_dying_state: return self._GyroscopeTick(*_, **__)
    if IsVisible(Space._instance.camera.position, targetEntityPos) != targetEntity.id: return self._GyroscopeTick(*_, **__)
    
    # Screen3 = Vector3(2400, 1080, 0)
    Screen3_2 = Vector3(localEntity.window_width_2, localEntity.window_height_2, 0)
    hitDir = [targetEntityPosx.x - Screen3_2.x, targetEntityPosx.y - Screen3_2.y]
    
    smoothing=0.00001

    fov = Space._instance.camera.engine_camera.FieldOfView
    hitDir = Normalize2(hitDir)
    x = hitDir[0] * targetDistance * fov * smoothing
    y = hitDir[1] * targetDistance * fov * smoothing
    
    if abs(x + y) > 0.0001: self.MoveCamera(x, -y)
    
    return self._GyroscopeTick(*_, **__)
