from gclient.framework.entities.space import Space

from gclient.gameplay.logic_base.entities.cdrone import DRONE_CAMERA_OFFSET
Vector3 = type(DRONE_CAMERA_OFFSET)

def WorldToScreenPoint(worldpos):
    return Space._instance.camera.engine_camera.GetScreenPointFromWorldPoint(worldpos)

def IsVisible(local, target, targetId, distance=300):
    raycast = Space._instance.RawRaycast(local, distance, 19, with_trigger=False, to_pos=target)
    
    if raycast.Body and getattr(raycast.Body, 'ownerid', None): # FIND A BETTER SOLUTION
        if getattr(raycast.Body, 'ownerid', None) == targetId: return True
    elif raycast.Flags == 7: return True

def igetattr(*_, **__):
    try: return getattr(*_, **__)
    except: return 'igetattr.error'

def idir(obj): return {k: igetattr(obj, k, 'undefined') for k in dir(obj)}

import inspect
def stacktrace():
    for frame_info in reversed(inspect.stack()):
        print(f"File: {frame_info.filename}, Line: {frame_info.lineno}, Function: {frame_info.function}")

def trace_handler(frame, event, arg): # sys.settrace
    if event == 'call':
        with open('kk.log', 'a') as w:
            w.write(f'Calling function: {frame.f_code.co_name} at line {frame.f_lineno}\n')
    elif event == 'line':
        with open('kk.log', 'a') as a:
            a.write(f'Executing line {frame.f_lineno} in {frame.f_code.co_name}\n')
    elif event == 'return':
        with open('kk.log', 'a') as a:
            a.write(f'Returning from function: {frame.f_code.co_name} with value {arg}\n')
    return trace_handler

import random
def trueChance(probability): return random.random() < probability

def randomHitOffset():
    return random.uniform(0.05, 0.1) * random.choice([1, -1])

def V3Minus(a, b): return (a.x - b.x, a.y - b.y, a.z - b.z)
def V32T(v):
    try: return v.x, v.y, v.z
    except: return v[0], v[1], v[2]
