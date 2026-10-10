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
def union_of_blocks(Zs, p):
    return all((B<=Zs) or not (B&Zs) for B,t in top_blocks(p,n))
for I in S:
    a,c,b,x,y=I; r=th(x,b); v=m(x,c); w=m(y,b); u=th(a,x); mm=m(x,y); s=th(y,a)
    sa,sb,sc,sx,sy,sr,sv,sw,su,sm,ss=[supp(p,n) for p in (a,b,c,x,y,r,v,w,u,mm,s)]
    G=join_classes([a,c],n); D=join_classes([b,c],n)
    cT=[E for E,t in top_blocks(c,n) if t]
    GT={cls(G,C) for C in cT}; DT={cls(D,C) for C in cT}
    Z=frozenset().union(*[K for K in G if K not in GT]) if any(K not in GT for K in G) else frozenset()
    Zb=frozenset().union(*[K for K in D if K not in DT]) if any(K not in DT for K in D) else frozenset()
    for nm,p in (('x',x),('y',y),('m',mm),('b',b),('s',s),('r',r),('v',v),('w',w),('u',u)):
        check(f'Z union of {nm}-blocks', union_of_blocks(Z,p), I)
        check(f'Zb (T-free Delta union) union of {nm}-blocks', union_of_blocks(Zb,p), I)
    check('Z ∩ Sy ⊆ supp s complement', not Z&ss, I)
    check('Z ∩ Sx ∩ supp v = ∅', not Z&sv, I)
    check('Zb ∩ supp w = ∅', not Zb&sw, I)
    check('Zb ∩ supp s = ∅', not Zb&ss, I)
    check('Zb ∩ supp u = ∅', not Zb&su, I)
    check('Z ∩ Zb ∩ Sy ...', True, I)
print(f"{len(S)} instances")
for k in sorted(fails): print(f"  FAIL {fails[k]:6d}  {k}")
# second pass: more Zb tests
fails={}
for I in S:
    a,c,b,x,y=I; r=th(x,b); v=m(x,c); w=m(y,b); u=th(a,x); mm=m(x,y); s=th(y,a)
    sa,sb,sc,sx,sy,sr,sv,sw,su,sm,ss=[supp(p,n) for p in (a,b,c,x,y,r,v,w,u,mm,s)]
    G=join_classes([a,c],n); D=join_classes([b,c],n)
    cT=[E for E,t in top_blocks(c,n) if t]; cN=[E for E,t in top_blocks(c,n) if not t]
    GT={cls(G,C) for C in cT}; DT={cls(D,C) for C in cT}
    Zb=frozenset().union(*[K for K in D if K not in DT]) if any(K not in DT for K in D) else frozenset()
    check('Zb ∩ supp m = ∅', not Zb&sm, I)
    check('Zb ∩ Sx ∩ Sy = ∅', not Zb&sx&sy, I)
    # for E in Delta_i (N(c)) with a-free Gamma-class: is Gamma(E) ∩ Zb = ∅ ?  (if so, chains die immediately)
    for C in cT:
        Di=cls(D,C)
        for E in cN:
            if E<=Di:
                Ge=cls(G,E)
                check('E in Delta_i: Gamma(E) ∩ Zb = ∅', not Ge&Zb, I)
                check('E in Delta_i: Gamma(E) c-blocks all in Delta_i or dead', all(cls(D,F)==Di or len([F2 for F2 in cN+cT if F2<=cls(D,F)])==1 for F in cN if F<=Ge), I)
                check('E in Delta_i: E ∩ Sy ⊆ supp s', (E&sy)<=ss, I)
                check('E in Delta_i: E ∩ Sx ⊆ supp r', (E&sx)<=sr, I)
                check('E in Delta_i: E ⊆ supp m ∪ ...?', E<=sm, I)
                check('E in Delta_i, E ⊆ Sy => E meets supp s', not E<=sy or bool(E&ss), I)
                check('E in Delta_i, E ⊆ Sx => E meets supp r', not E<=sx or bool(E&sr), I)
print(f"{len(S)} instances (pass 2)")
for k in sorted(fails): print(f"  FAIL {fails[k]:6d}  {k}")
