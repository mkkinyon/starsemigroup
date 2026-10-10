import sys, json, time
sys.path.insert(0,'/home/claude/pa8w/embed')
from pa_sat import solve
T=json.load(open('model11.json'))
for m in map(int, sys.argv[1:]):
    t=time.time(); r=solve(T, m, distinct=True, verbose=False)
    print(f"m={m}: {'EMBEDS' if r else 'no embedding'} ({time.time()-t:.0f}s)", flush=True)
    if r: json.dump(r, open(f'embed11_m{m}.json','w'))
