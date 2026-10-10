"""For sub-hypothesis sets, test ε_c <= ε_y∨ε_a on P_4 instances."""
import sys, itertools, random
sys.path.insert(0,'/home/claude/pa8w/embed'); sys.path.insert(0,'/home/claude/pa8w/embed/pa8/rp')
from pmon import projections, mul
from blocks import top_blocks, supp, join_classes
n=4; P=projections(n); memo={}
def m(p,q):
    k=(p,q)
    if k not in memo: memo[k]=mul(p,q,n)
    return memo[k]
th=lambda p,q: m(m(p,q),p)
matched=lambda p,q: th(p,q)==p and th(q,p)==q
comm=lambda p,q: m(p,q)==m(q,p)
def leq(Pc,Q): return all(any(C<=D for D in Q) for C in Pc)
random.seed(1)
pairs=[(a,c) for a in P for c in P if a!=c and matched(a,c)]
print(len(pairs),'matched pairs')
tests={'y id a=c only': lambda a,c,b,x,y: True,
       'y id a=c, y~b': lambda a,c,b,x,y: comm(y,b),
       'y id a=c, x~y, x id a=c': lambda a,c,b,x,y: comm(x,y) and th(x,a)==th(x,c),
       'y id a=c, x~y, x~c, x id a=c': lambda a,c,b,x,y: comm(x,y) and comm(x,c) and th(x,a)==th(x,c),
       'y id a=c, x~y, x~c': lambda a,c,b,x,y: comm(x,y) and comm(x,c),
       'W2': lambda a,c,b,x,y: comm(x,y) and comm(x,c) and th(x,a)==th(x,c) and comm(y,b)}
fails={k:0 for k in tests}; cnt={k:0 for k in tests}
for (a,c) in random.sample(pairs,60):
    Ys=[y for y in P if th(y,a)==th(y,c)]
    Bs=[b for b in P if matched(b,c)]
    for y in Ys:
        YA=join_classes([y,a],n); cb=[E for E,t in top_blocks(c,n)]
        ok=leq(cb,YA)
        for b in Bs:
            for x in random.sample(P,40):
                for k,f in tests.items():
                    if f(a,c,b,x,y):
                        cnt[k]+=1
                        if not ok: fails[k]+=1
for k in tests: print(f"{k:40} instances {cnt[k]:7d} fails {fails[k]}")
