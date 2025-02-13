def normalize(x, y, z):
    mag = (x**2 + y**2 + z**2) ** 0.5
    epsilon = 1e-8
    
    if mag < epsilon: return (x, y, z)
    
    return (x/mag, y/mag, z/mag)

def Distance(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    dz = b[2] - a[2]
    return (dx**2 + dy**2 + dz**2) ** 0.5

def v2Distance(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    return (dx**2 + dy**2) ** 0.5

import math
def Normalize2(_):
    mag = math.sqrt(_[0] * _[0] + _[1] * _[1])
    if mag == 0: return (0,0)
    return (_[0]/mag, _[1]/mag)

from gshare.formula import Distance2D, Normalize2D
from gshare.formula import Distance3D, Normalize3D, DirAndLen3D
