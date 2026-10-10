import json, sys, os, itertools, time
os.environ['EMBED_DIR']='/home/claude/pa8w/embed'
sys.path.insert(0,'/home/claude/pa8w/embed'); sys.path.insert(0,'/home/claude/pa8w/embed/pa8/wn'); sys.path.insert(0,'/home/claude/pa8w/n4')
from pa_sat import solve
from iso import iso
n=int(sys.argv[1]); mmax=int(sys.argv[2]) if len(sys.argv)>2 else 7
d=json.load(open(f'R{n}.json')); T=d['T']; nm=d['names']; N=len(T); th=lambda p,q:T[p][q]
mt=lambda x,y: th(y,x)==x and th(x,y)==y
comm=lambda x,y: th(x,y)==th(y,x)
ident=lambda x,a,c: th(a,x)==th(c,x)
def rp(j):
    bad=[]
    for a,c,b in itertools.product(range(N),repeat=3):
        if not(mt(a,c) and mt(c,b) and not mt(a,b)): continue
        for xs in itertools.product(range(N),repeat=j):
            ch=[c]+list(xs)
            if all(comm(ch[i],ch[i+1]) for i in range(j)) and all(ident(x,a,c) for x in xs):
                for y in range(N):
                    if comm(y,a) and th(b,xs[-1])==th(b,y): bad.append(tuple(nm[i] for i in (a,c,b)+xs+(y,)))
    return bad
for j in range(1,n+2):
    v=rp(j); print(f"R{n}: (R'_{j}) violations: {len(v)} {v[:3]}",flush=True)
    if j>n: break
def wn(j):
    bad=0
    for a,c,b in itertools.product(range(N),repeat=3):
        if not(mt(a,c) and mt(c,b) and not mt(a,b)): continue
        for xs in itertools.product(range(N),repeat=j):
            ch=[c]+list(xs)+[b]
            if all(comm(ch[i],ch[i+1]) for i in range(j+1)) and all(ident(x,a,c) for x in xs): bad+=1
    return bad
print(f"R{n}: (W_j) violations j=1..{n+1}:",[wn(j) for j in range(1,n+2)],flush=True)
import subprocess
print(subprocess.run(['python3','/home/claude/pa8w/embed/pa8/w3/evalcond2.py',f'R{n}_T.json'],capture_output=True,text=True).stdout)
def gen(S):
    S=set(S); ch=True
    while ch:
        ch=False
        for x in list(S):
            for y in list(S):
                if T[x][y] not in S: S.add(T[x][y]); ch=True
    return S
def sub(S):
    S=sorted(S); idx={x:i for i,x in enumerate(S)}
    return [[idx[T[x][y]] for y in S] for x in S]
irr=[x for x in range(N) if x not in gen(set(range(N))-{x})]
print('irreducible:',[nm[i] for i in irr],flush=True)
for x in irr:
    S=gen(set(range(N))-{x})
    for m in range(4,mmax+2):
        t=time.time(); r=solve(sub(S),m,verbose=False)
        if r: print(f"maximal subalgebra omit {nm[x]} (order {len(S)}): embeds in P(P_{m}) ({time.time()-t:.0f}s)",flush=True); break
    else: print(f"maximal subalgebra omit {nm[x]}: NO embedding for m<={mmax+1}",flush=True)
for m in range(4,mmax+1):
    t=time.time(); r=solve(T,m,verbose=False); print(f"R{n} in P(P_{m}): {'EMBEDS' if r else 'no'} ({time.time()-t:.0f}s)",flush=True)
    if r: break
