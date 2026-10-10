import json, sys, os, time
os.environ['EMBED_DIR']='/home/claude/pa8w/embed'
sys.path.insert(0,'/home/claude/pa8w/embed')
from pa_sat import solve
T=json.load(open('mk10_T.json')); n=10
nm='a b c k p q 6 7 8 9'.split()
def sub(S):
    S=sorted(S); idx={x:i for i,x in enumerate(S)}
    return [[idx[T[x][y]] for y in S] for x in S]
def gen(S):
    S=set(S); ch=True
    while ch:
        ch=False
        for x in list(S):
            for y in list(S):
                if T[x][y] not in S: S.add(T[x][y]); ch=True
    return S
mode=sys.argv[1]
if mode=='full':
    for m in range(4,8):
        t=time.time(); r=solve(T,m,verbose=False); print(f"full algebra in P(P_{m}): {'EMBEDS' if r else 'no'} ({time.time()-t:.0f}s)",flush=True)
        if r: break
else:
    for x in (0,1,2,3,4):
        S=gen(set(range(n))-{x})
        for m in range(4,9):
            t=time.time(); r=solve(sub(S),m,verbose=False)
            if r: print(f"maximal subalgebra omit {nm[x]} (order {len(S)}): embeds in P(P_{m}) ({time.time()-t:.0f}s)",flush=True); break
            else: print(f"  omit {nm[x]}: no at m={m} ({time.time()-t:.0f}s)",flush=True)
