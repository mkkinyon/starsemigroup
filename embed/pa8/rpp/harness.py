"""Structural test harness on (R'') instances."""
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
    sa,sb,sc,sx,sy,sr,sv,sw,su=[supp(p,n) for p in (a,b,c,x,y,r,v,w,u)]
    G=join_classes([a,c],n); D=join_classes([b,c],n); R=join_classes([a,b],n)
    ABC=join_classes([a,b,c],n); CBX=join_classes([c,b,x],n); CBY=join_classes([c,b,y],n); CAY=join_classes([c,a,y],n); CAX=join_classes([c,a,x],n)
    CBM=join_classes([c,b,mm],n); CAM=join_classes([c,a,mm],n); CBR=join_classes([c,b,r],n); CAR=join_classes([c,a,r],n)
    XB=join_classes([x,b],n); YA=join_classes([y,a],n); XA=join_classes([x,a],n); YC=join_classes([y,c],n); YB=join_classes([y,b],n); XC=join_classes([x,c],n)
    cT=[E for E,t in top_blocks(c,n) if t]; cN=[E for E,t in top_blocks(c,n) if not t]
    Nx=[E for E,t in top_blocks(x,n) if not t]; Ny=[E for E,t in top_blocks(y,n) if not t]; Nb=[E for E,t in top_blocks(b,n) if not t]; Na=[E for E,t in top_blocks(a,n) if not t]
    for J,name in ((ABC,'abc'),(CBX,'cbx'),(CBY,'cby'),(CAY,'cay'),(CAX,'cax'),(CBM,'cbm'),(CAM,'cam'),(CBR,'cbr'),(CAR,'car')):
        for K in J: check(f'J1 {name}: class has <=1 T(c)', sum(1 for C in cT if C<=K)<=1, I)
    for C in cT:
        Gi=cls(G,C); Di=cls(D,C)
        for E in cN:
            if E<=Gi: check('S1 N(c) in Gamma_i is N(x),N(y),N(b)', E in Nx and E in Ny and E in Nb, I)
            if E<=Di:
                check('S2a N(c) in Delta_i is a-free', not E&sa, I)
                check('S2b Gamma(E) a-free', not cls(G,E)&sa, I)
                check('S3 E in Sx or E in Sy', E<=sx or E<=sy, I)
                check('S3b E in Sx or E is N(x)', E<=sx or E in Nx, I)
                check('S3c E in Sy or E is N(y)', E<=sy or E in Ny, I)
                check('S3d E in Sx∪Sy', E<=sx|sy, I)
                check('S4 E ∩ supp r = ∅', not E&sr, I)
                check('S4b E ∩ supp v = ∅', not E&sv, I)
                check('S4c E ∩ supp u = ∅', not E&su, I)
                check('S4d E ∩ supp w = ∅', not E&sw, I)
                # the class of ε_x∨ε_b of E (if E in Sx): b-free?
                if E<=sx: check('S5 E in Sx => XB-class of E is Delta-related: cls(XB,E) ∩ supp b', True, I)
        check('S6 C_i in Sx or C_i in N(x)-block', C<=sx or any(C<=N for N in Nx), I)
        check('S6b C_i in Sy or C_i in N(y)-block', C<=sy or any(C<=N for N in Ny), I)
        check('S7 C_i in Sx', C<=sx, I)
        check('S7b C_i meets Sx', bool(C&sx), I)
        check('S7c C_i meets Sy', bool(C&sy), I)
        check('S7d C_i meets supp r', bool(C&sr), I)
        check('S7e C_i meets supp v', bool(C&sv), I)
        Ai=next(A for A,t in top_blocks(a,n) if t and A<=Gi); Bi=next(B for B,t in top_blocks(b,n) if t and B<=Di)
        check('S8 A_i meets Sy', bool(Ai&sy), I); check('S8b A_i meets Sx', bool(Ai&sx), I); check('S8c A_i meets supp u', bool(Ai&su), I)
        check('S9 B_i meets Sy', bool(Bi&sy), I); check('S9b B_i meets Sx', bool(Bi&sx), I); check('S9c B_i meets supp w', bool(Bi&sw), I)
        check('S10 Delta_i ∩ Sx ⊆ cls(XC,C_i)', (Di&sx)<=cls(XC,C), I)
        check('S10b Delta_i ∩ Sy ⊆ cls(YB,B_i)', (Di&sy)<=cls(YB,Bi), I)
        check('S10c Gamma_i ∩ Sx ⊆ cls(XC,C_i)', (Gi&sx)<=cls(XC,C), I)
        check('S10d Gamma_i ∩ Sy ⊆ cls(YA,A_i)', (Gi&sy)<=cls(YA,Ai), I)
        check('S10e Gamma_i ∩ Sy ⊆ cls(YC,C_i)', (Gi&sy)<=cls(YC,C), I)
        check('S10f Delta_i ∩ Sy ⊆ cls(YC,C_i)', (Di&sy)<=cls(YC,C), I)
        check('S10g Delta_i ∩ Sx ⊆ cls(XB,B_i)', (Di&sx)<=cls(XB,Bi), I)
print(f"{len(S)} instances")
for k in sorted(fails): print(f"  FAIL {fails[k]:6d}  {k}")
allnames=set(fails)
pickle.dump(ex,open('harness_ex.pkl','wb'))
