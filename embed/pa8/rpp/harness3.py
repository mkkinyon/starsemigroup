import sys, pickle, random
sys.path.insert(0,'/home/claude/pa8w/embed'); sys.path.insert(0,'/home/claude/pa8w/embed/pa8/rp')
from pmon import mul
from blocks import top_blocks, supp, join_classes
n=int(sys.argv[1]); inst=pickle.load(open(sys.argv[2],'rb')); memo={}
def m(p,q):
    k=(p,q)
    if k not in memo: memo[k]=mul(p,q,n)
    return memo[k]
th=lambda p,q: m(m(p,q),p)
S = inst if len(sys.argv)<4 else random.sample(inst,int(sys.argv[3]))
fails={}; ex={}
def check(name, cond, I):
    if not cond:
        fails[name]=fails.get(name,0)+1; ex.setdefault(name,I)
def cls(J,E): return next(K for K in J if E<=K)
for I in S:
    a,c,b,x,y=I; r=th(x,b); v=m(x,c); w=m(y,b); u=th(a,x); mm=m(x,y)
    sa,sb,sc,sx,sy,sr,sv,sw,su,sm=[supp(p,n) for p in (a,b,c,x,y,r,v,w,u,mm)]
    G=join_classes([a,c],n); D=join_classes([b,c],n)
    cT=[E for E,t in top_blocks(c,n) if t]; cN=[E for E,t in top_blocks(c,n) if not t]
    DT={cls(D,C) for C in cT}; GT={cls(G,C) for C in cT}
    for K in G:
        if K in GT: continue
        for nm,s in (('u',su),('v',sv),('w',sw),('r',sr),('m',sm),('x',sx),('y',sy),('b',sb)):
            check(f'Z1 a-free Gamma-class avoids supp {nm}', not K&s, I)
    for K in D:
        if K in DT: continue
        for nm,s in (('u',su),('v',sv),('w',sw),('r',sr),('m',sm),('x',sx),('y',sy),('a',sa)):
            check(f'Z2 T-free Delta-class avoids supp {nm}', not K&s, I)
    for C in cT:
        Di=cls(D,C); Gi=cls(G,C)
        for nm,s in (('u',su),('v',sv),('w',sw),('r',sr),('m',sm)):
            check(f'Z3 Delta_i ∩ supp {nm} ⊆ C_i ∪ B_i', (Di&s)<=C|next(B for B,t in top_blocks(b,n) if t and B<=Di), I)
            check(f'Z4 Gamma_i ∩ supp {nm} ⊆ C_i ∪ A_i', (Gi&s)<=C|next(A for A,t in top_blocks(a,n) if t and A<=Gi), I)
print(f"{len(S)} instances")
for k in sorted(fails): print(f"  FAIL {fails[k]:6d}  {k}")
