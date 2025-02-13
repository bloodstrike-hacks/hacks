import zlib, os

class DotDict:
    def __init__(self, dictionary=None): super().__setattr__('_attributes', dictionary or {})
    def __getattr__(self, name): return self._attributes.get(name)
    def __setattr__(self, name, value):
        if name == '_attributes': super().__setattr__(name, value)
        else: self._attributes[name] = value

def crc32(_):
    return zlib.crc32(open(_, 'rb').read()) & 0xffffffff

files = {}
def upd():
    for path, file in files.items():
        mtime = os.path.getmtime(path)
        if file.mtime == mtime: continue
        file.mtime = mtime
        
        crc = crc32(path)
        if file.crc == crc: continue
        file.crc = crc
        
        execp(path)

def liveupd(_):
    files[_] = DotDict()
