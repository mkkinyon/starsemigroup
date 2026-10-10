import sys, json, time
sys.path.insert(0,'/home/claude/pa8w/embed')
from pa_sat import solve
T=json.load(open('model11.json')); n=11
names={0:'a',1:'b',2:'c',3:'k',4:'p',5:'q'}
for drop in range(6):
    S=[x for x in range(n) if x!=drop]; idx={x:i for i,x in enumerate(S)}
    Ts=[[idx[T[x][y]] for y in S] for x in S]
    for m in (4,5,6,7):
        t=time.time(); r=solve(Ts, m, distinct=True, verbose=False)
        print(f"drop {names[drop]}: m={m} {'EMBEDS' if r else 'no'} ({time.time()-t:.0f}s)", flush=True)
        if r: break
