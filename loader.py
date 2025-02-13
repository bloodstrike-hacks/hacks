# open(f"/data/data/com.netease.newspike/python/touch", 'w').close()
import sys, traceback, time, os
from datetime import datetime

class LoggerClient:
    def __init__(self, dir):
        self.logs = f"{dir}/logs/{time.time()}"
        os.makedirs(self.logs, exist_ok=True)
        self.f = open(self.logs + '/log.log', 'a')
    
    def write(self, data):
        if (data := str(data).rstrip('\n')):
            self.f.write(f"[{datetime.now().strftime("%I:%M:%S")}]: {data}\n")
            self.f.flush()

    def flush(self): self.f.flush()
    def close(self): self.f.close()

cwd = '/data/data/com.netease.newspike/python'
os.makedirs(f"{cwd}/cwd", exist_ok=True)
os.chdir(f"{cwd}/cwd")
# sys.path.append(cwd)

client = LoggerClient(cwd)

sys.stdout = client
sys.stderr = client

def execp(path):
    try: return exec(open(path).read(), globals(), globals())
    except: print(traceback.format_exc())

print('\033c', end='')

for file in os.scandir('imp'):
    if file.is_file(): execp(file.path)

# execp(f"{cwd}/hacks/testing.py")
# execp(f"{cwd}/hacks/aimbot.py") # BAN
execp(f"{cwd}/hacks/skin.py") # IDK
# execp(f"{cwd}/hacks/bt.py") # IT WAS PRETTY SAFE BUT NOW IT'S BANNED!, ALSO SOME HITS ARENT REGISTERED IN HIGHER RANKS??
# execp(f"{cwd}/hacks/highdmg.py") # DOESNT WORK ON REAL PLAYERS
execp(f"{cwd}/hacks/esp.py") # SAFE
# execp(f"{cwd}/hacks/norecoil.py") # BAN

print('loaded!')
