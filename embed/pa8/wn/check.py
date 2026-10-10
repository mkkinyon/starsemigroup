"""Check a chain-witness model: all labelled conditions, the chain words, embeddability, minimality."""
import sys, json, time, itertools
sys.path.insert(0,'/home/claude/pa8w/embed'); sys.path.insert(0,'/home/claude/pa8w/n4')
from pa_sat import solve
from qi import violated_in
d = json.load(open(sys.argv[1])); T = d['T']; n = len(T); mmax = int(sys.argv[2]) if len(sys.argv) > 2 else 6
json.dump(T, open(sys.argv[1].replace('.json','_T.json'),'w'))
import subprocess
print(subprocess.run(['python3','/home/claude/pa8w/embed/pa8/w3/evalcond2.py', sys.argv[1].replace('.json','_T.json')], capture_output=True, text=True).stdout)
P=[('mt','a','c'),('mt','c','b')]
def chain(k):
    nm=['x%d'%i for i in range(1,k+1)]
    H=P+[('comm',nm[0],'c'),('comm',nm[-1],'b')]+[('comm',u,v) for u,v in zip(nm,nm[1:])]+[('eq',(u,'a'),(u,'c')) for u in nm]
    return H
for k in range(1,7):
    A=violated_in(T,chain(k),('mt','a','b'))
    print(f"(W_{k}): {'VIOLATED '+str(A) if A else 'satisfied'}", flush=True)
for m in range(4, mmax+1):
    t=time.time(); r=solve(T,m,distinct=True,verbose=False); print(f"embed m={m}: {'EMBEDS' if r else 'no'} ({time.time()-t:.0f}s)", flush=True)
    if r: break
st=lambda x,y: T[x][y]
def closure(S):
    S=set(S)
    while True:
        new={st(x,y) for x in S for y in S}|S
        if new==S: return frozenset(S)
        S=new
subs={closure(S) for k in range(1,n) for S in itertools.combinations(range(n),min(k,2))} | {closure(set(range(n))-{x}) for x in range(n)}
subs={S for S in subs if len(S)<n}
maxsubs=[S for S in subs if not any(S<S2 for S2 in subs)]
for S in maxsubs:
    S=sorted(S); idx={x:i for i,x in enumerate(S)}; Ts=[[idx[T[x][y]] for y in S] for x in S]
    for m in range(4, mmax+1):
        r=solve(Ts,m,distinct=True,verbose=False)
        if r: print(f"maximal subalgebra (omit {sorted(set(range(n))-set(S))}): embeds in P(P_{m})", flush=True); break
    else: print(f"maximal subalgebra (omit {sorted(set(range(n))-set(S))}): NO embedding for m <= {mmax}", flush=True)
