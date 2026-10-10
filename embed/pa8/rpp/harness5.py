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
stats={}
for I in S:
    a,c,b,x,y=I; r=th(x,b); v=m(x,c); w=m(y,b); u=th(a,x); mm=m(x,y)
    sa,sb,sc,sx,sy,sr,sv,sw,su,sm=[supp(p,n) for p in (a,b,c,x,y,r,v,w,u,mm)]
    G=join_classes([a,c],n); D=join_classes([b,c],n)
    cT=[E for E,t in top_blocks(c,n) if t]; cN=[E for E,t in top_blocks(c,n) if not t]
    U=[E for E,t in top_blocks(u,n) if t]; W=[E for E,t in top_blocks(w,n) if t]; Rt=[E for E,t in top_blocks(r,n) if t]
    DT={cls(D,C) for C in cT}; GT={cls(G,C) for C in cT}
    for K in G:
        if K in GT: continue
        adjD={cls(D,E) for E in cN if E<=K}
        if len(adjD)>=2:
            check('L6c a-free Gamma-class adjacent to >=2 Delta-classes meets supp w', bool(K&sw), I)
            check('L6d ... meets supp r', bool(K&sr), I)
            check('L6e ... meets supp y', bool(K&sy), I)
            check('L6f ... meets supp x', bool(K&sx), I)
            check('L6g ... meets supp b', bool(K&sb), I)
            check('L6h ... meets supp m', bool(K&sm), I)
            nT=len(adjD&DT); stats[('G',nT,len(adjD))]=stats.get(('G',nT,len(adjD)),0)+1
            check('L6i ... adjacent to <=1 T-Delta', nT<=1, I)
            check('L6j ... adjacent to a T-Delta', nT>=1, I)
    for K in D:
        if K in DT: continue
        adjG={cls(G,E) for E in cN if E<=K}
        if len(adjG)>=2:
            check('L7c T-free Delta-class adjacent to >=2 Gamma-classes meets supp u', bool(K&su), I)
            check('L7d ... meets supp a', bool(K&sa), I)
            check('L7e ... meets supp x', bool(K&sx), I)
            check('L7f ... meets supp y', bool(K&sy), I)
            check('L7g ... meets supp m', bool(K&sm), I)
            nT=len(adjG&GT); stats[('D',nT,len(adjG))]=stats.get(('D',nT,len(adjG)),0)+1
print(f"{len(S)} instances")
for k in sorted(fails): print(f"  FAIL {fails[k]:6d}  {k}")
print(stats)
pickle.dump(ex,open('harness5_ex.pkl','wb'))
