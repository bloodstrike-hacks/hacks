import time
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

def GetHitData(wp, entity, bone):
    startPos = Space._instance.camera.position
    bonePos = entity.model.GetBoneWorldPosition(bone['bone_name'])
    
    for _ in range(30):
        hitOffset = Vector3(randomHitOffset(), randomHitOffset(), randomHitOffset())
        hitPos = bonePos + hitOffset
        
        hitDir, distance = DirAndLen3D(startPos, hitPos)
        if distance > wp['damage_range']: break
        
        raycast = Space._instance.RawRaycast(startPos, wp['damage_range'], 19, with_trigger=False, to_pos=hitPos)
        
        if raycast.Body and getattr(raycast.Body, 'ownerid', None):
            if getattr(raycast.Body, 'ownerid', None) == entity.id: return raycast, distance, startPos, hitDir, hitPos, hitOffset
        else:
            if raycast.Flags == 7: return raycast, distance, startPos, hitDir, hitPos, hitOffset
    
    return 0, 0, 0, 0, 0, 0

def dropDamage(wp, dmg, distance):
    if distance > wp['damage_range']: return 0
    if distance < wp['damage_range_1']: return dmg
    if distance < wp['damage_range_2']: return dmg * wp['damage_dropoff_1']
    if distance < wp['damage_range_3']: return dmg * wp['damage_dropoff_2']
    return dmg * wp['damage_dropoff_3']

def GetTargetEntity():
    targetEntity, nearestDistance = None, float('inf')
    
    for entityId, entity in Space._instance.entities.copy().items():
        if not isinstance(entity, CombatAvatar): continue
        if not entity.is_alive: continue
        if IsPlayerTeammate(entityId): continue
        
        entityPosx = WorldToScreenPoint(Vector3(*entity.position))
        if entityPosx.z <= 0.0: continue
        
        distance = Distance2D((entityPosx.x, entityPosx.y), (2400/2, 1080/2))
        if distance < nearestDistance:
            nearestDistance = distance
            targetEntity = entity
    
    return targetEntity

from gclient.gameplay.logic_base.entities.combat_avatar import PlayerCombatAvatar
@HOOK(PlayerCombatAvatar, 0)
def CallServerGameLogic(self, method, *args, **kwargs):
    if method == 'BatchDealSpellResult' and Space._instance.entities:
        if getattr(PlayerCombatAvatar, 'boneScales', None) == None: setattr(PlayerCombatAvatar, 'boneScales', {})
        
        for hit in args[0].copy():
            if 'caster' not in hit: continue
            
            localEntity = Space._instance.owner.combat_avatar
            if not localEntity: continue
            if localEntity.id != hit['caster']: continue
            
            probability = 0.70
            if 'damage_result' in hit:
                # if not trueChance(probability): continue
                
                # print(f"ENTER: HEAD({irepr(*args, **kwargs)})")
                
                for _, hitData in hit['damage_result'].items():
                    targetId = hitData.get('target_id', None)
                    if targetId not in PlayerCombatAvatar.boneScales: PlayerCombatAvatar.boneScales[targetId] = {}
                    if 'hit_part' in hitData and 'verify_bone_scale' in hitData: PlayerCombatAvatar.boneScales[targetId][hitData['hit_part']] = hitData['verify_bone_scale']
                    
                    if hitData.get('hit_part', 'Head') == 'Head': continue
                    
                    weapon_guid = hitData.get('weapon_guid') or hit.get('weapon_guid')
                    if not weapon_guid: continue
                    
                    curWeapon = localEntity.GetWeaponByGuid(weapon_guid)
                    if not curWeapon: continue
                    curWeaponProto = curWeapon.weapon_proto
                    
                    hitEntity = Space._instance.entities.get(_, None)
                    if not hitEntity: continue
                    if not isinstance(hitEntity, CombatAvatar): continue
                    if not hitEntity.is_alive: continue
                    if hitEntity.IsRobotCombatAvatar: continue
                    
                    bone = BONES['Head']
                    boneScale = PlayerCombatAvatar.boneScales.get(hitEntity.id, {}).get(bone['name'], bone['scale'])
                    
                    raycast, distance, startPos, hitDir, hitPos, hitOffset = GetHitData(curWeaponProto, hitEntity, bone)
                    if not raycast: continue
                    
                    damage = float(curWeaponProto[bone['dmg_name']])
                    damage = dropDamage(curWeaponProto, damage, distance)
                    if not damage: continue
                    
                    print(f"head delt {damage}")
                    
                    hitData['hit_dir'] = hitDir
                    hitData['hit_pos'] = V32T(hitPos)
                    hitData['hit_part'] = bone['name']
                    hitData['damage'] = damage
                    hitData['verify_hit_offset'] = V32T(hitOffset)
                    hitData['verify_bone_scale'] = boneScale
                    
                    for hitEffect in hit.get('hit_effect', ()):
                        hitEffect['hit_pos'] = hitData['hit_pos']
                        hitEffect['hit_normal'] = V32T(Space._instance.RawRaycast(Space._instance.camera.position, 300, 19, with_trigger=False, to_pos=hitPos).Normal)
                        hitEffect['hit_dir'] = hitData['hit_dir']
                
                # print(f"EXIIT: HEAD({irepr(*args, **kwargs)})")
            elif 'ballistic_effect' in hit or ('sound_result' in hit and 'make_ballistick_effect' in hit.get('extra', ())):
                # print(f"ENTER: FORCE({irepr(*args, **kwargs)})")
                
                if localEntity.is_ads: probability += 0.10
                # if not trueChance(probability): continue
                
                curWeapon = localEntity.GetCurWeapon()
                if not curWeapon: continue
                curWeaponProto = curWeapon.weapon_proto
                
                targetEntity = GetTargetEntity()
                if not targetEntity: continue
                if targetEntity.IsRobotCombatAvatar: continue
                if targetEntity.is_dying_state: continue
                
                bone = BONES['Head']
                boneScale = PlayerCombatAvatar.boneScales.get(targetEntity.id, {}).get(bone['name'], bone['scale'])
                
                raycast, distance, startPos, hitDir, hitPos, hitOffset = GetHitData(curWeaponProto, targetEntity, bone)
                if not raycast: continue
                
                damage = float(curWeaponProto[bone['dmg_name']])
                damage = dropDamage(curWeaponProto, damage, distance)
                if not damage: continue
                
                print(f"force delt {damage}")
                
                hitEffect = hit.get('hit_effect', [{}])[0]
                
                args[0][0] = {
                    'weapon_guid': hit['weapon_guid'],
                    'cost_ammo': hit.get('cost_ammo', False),
                    'spell_id': hit['spell_id'],
                    'level': hit['level'],
                    'caster': hit['caster'],
                    'caster_pos': hit['caster_pos'],
                    'damage_result': {
                        targetEntity.id: {
                            'weapon_id': curWeapon.equip_id,
                            'weapon_guid': curWeapon.guid,
                            'damage': damage,
                            'hit_part': bone['name'],
                            'hit_dir': hitDir,
                            'target_pos': targetEntity.position,
                            'shoot_idx': '',
                            'verify_bone_scale': boneScale,
                            'verify_hit_offset': V32T(hitOffset),
                            'hit_pos': V32T(hitPos),
                            'penetrate_power': 100.0, 'penetrate_materials': [1001, 1],
                            # 'hit_back': True
                        }
                    },
                    'hit_effect': [
                        {
                            'hit_pos': V32T(hitPos),
                            'hit_normal': V32T(raycast.Normal),
                            'hit_dir': hitDir,
                            'hit_material_type': 1001,
                            'weapon_id': curWeapon.equip_id,
                            'hit_effect_id': hitEffect.get('hit_effect_id', 0),
                            'target_id': targetEntity.id
                        }
                    ],
                    'verify_start_pos': V32T(startPos),
                    'extra': {
                        'gun_id': curWeapon.gun_id,
                        'make_ballistick_effect': {
                            'verify_timestamp': hit.get('verify_timestamp') or hit.get('extra', {}).get('make_ballistick_effect', {}).get('verify_timestamp') or time.time()
                        }
                    }
                }
                
                # args[0] = [Hit]
                
                # print(f"EXIIT: FORCE({irepr(*args, **kwargs)})")
        
    return self._CallServerGameLogic(method, *args, **kwargs)
