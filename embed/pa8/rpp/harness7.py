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
    G=join_classes([a,c],n); D=join_classes([b,c],n); VW=join_classes([v,w],n); UV=join_classes([u,v],n); UW=join_classes([u,w],n)
    Rt=[E for E,t in top_blocks(r,n) if t]; V=[E for E,t in top_blocks(v,n) if t]; W=[E for E,t in top_blocks(w,n) if t]; U=[E for E,t in top_blocks(u,n) if t]
    Mt=[E for E,t in top_blocks(mm,n) if t]
    cT=[E for E,t in top_blocks(c,n) if t]; bT=[E for E,t in top_blocks(b,n) if t]; aT=[E for E,t in top_blocks(a,n) if t]
    for R in Rt:
        check('R1 T(r)-block meets <=1 V_k', sum(1 for Vk in V if R&Vk)<=1, I)
        check('R1b T(r)-block meets <=1 W_l', sum(1 for Wl in W if R&Wl)<=1, I)
        check('R1c T(r)-block meets <=1 U_j', sum(1 for Uj in U if R&Uj)<=1, I)
        check('R1d T(r)-block meets >=1 V_k', sum(1 for Vk in V if R&Vk)>=1, I)
        check('R1e T(r)-block meets >=1 W_l', sum(1 for Wl in W if R&Wl)>=1, I)
        check('R1f T(r)-block meets >=1 U_j', sum(1 for Uj in U if R&Uj)>=1, I)
        check('R2 T(r)-block ⊆ supp u ∪ supp v ∪ supp w', R<=su|sv|sw, I)
        check('R2b T(r)-block ⊆ supp v ∪ supp w', R<=sv|sw, I)
        check('R2c T(r)-block ⊆ supp a ∪ supp b ∪ supp c', R<=sa|sb|sc, I)
        Vs=[Vk for Vk in V if R&Vk]; Ws=[Wl for Wl in W if R&Wl]; Us=[Uj for Uj in U if R&Uj]
        if Vs and Ws: check('R3 V_k, W_l met by R are VW-matched', cls(VW,Vs[0])==cls(VW,Ws[0]), I)
        if Vs and Us: check('R3b U_j, V_k met by R are UV-matched', cls(UV,Us[0])==cls(UV,Vs[0]), I)
        check('R4 T(r)-block meets <=1 T(c)', sum(1 for C in cT if R&C)<=1, I)
        check('R4b T(r)-block meets <=1 T(b)', sum(1 for B in bT if R&B)<=1, I)
        check('R4c T(r)-block meets <=1 T(a)', sum(1 for A in aT if R&A)<=1, I)
    for Vk in V:
        check('R5 V_k meets <=1 T(r)-block', sum(1 for R in Rt if R&Vk)<=1, I)
        check('R5b V_k ∩ Sy ⊆ one T(r)-block', any((Vk&sy)<=R for R in Rt) or not Vk&sy, I)
        check('R5c V_k ∩ Sy ⊆ supp r', (Vk&sy)<=sr, I)
        check('R5d V_k ⊆ one T(m)-block', any(Vk<=M for M in Mt), I)
    for Wl in W:
        check('R6 W_l meets <=1 T(r)-block', sum(1 for R in Rt if R&Wl)<=1, I)
        check('R6c W_l ∩ Sx ⊆ supp r', (Wl&sx)<=sr, I)
    for Uj in U:
        check('R7 U_j meets <=1 T(r)-block', sum(1 for R in Rt if R&Uj)<=1, I)
    for C in cT:
        if C<=sx: check('R8 visible C_i meets exactly one T(r)-block', sum(1 for R in Rt if R&C)==1, I)
        if C<=sx: check('R8b visible C_i ⊆ one T(m)-block', any(C<=M for M in Mt), I)
    for B in bT:
        if B<=sy: check('R9 visible B_i meets exactly one T(r)-block', sum(1 for R in Rt if R&B)==1, I)
    for A in aT:
        if A<=su: check('R10 visible A_i meets exactly one T(r)-block', sum(1 for R in Rt if R&A)==1, I)
print(f"{len(S)} instances")
for k in sorted(fails): print(f"  FAIL {fails[k]:6d}  {k}")
pickle.dump(ex,open('harness7_ex.pkl','wb'))
