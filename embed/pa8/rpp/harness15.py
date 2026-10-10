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
    a,c,b,x,y=I; mm=m(x,y)
    sa,sc,sx,sy,sm=[supp(p,n) for p in (a,c,x,y,mm)]
    XA=join_classes([x,a],n); XC=join_classes([x,c],n); YA=join_classes([y,a],n); YC=join_classes([y,c],n)
    Ny=[E for E,t in top_blocks(y,n) if not t]; Nx=[E for E,t in top_blocks(x,n) if not t]
    for E,t in top_blocks(c,n):
        for M in Ny:
            if not M&E: continue
            if E<=sx:
                check('A1 E⊆Sx, N(y) M meets E => M ⊆ K(E) (x∨a class)', M<=cls(XA,E), I)
                check('A2 ... => M ⊆ x∨c class of E', M<=cls(XC,E), I)
                check('A3 ... => M ⊆ E', M<=E, I)
                check('A4 ... => M ⊆ Sx', M<=sx, I)
                check('A5 ... => M ∩ Sx ⊆ E', (M&sx)<=E, I)
        for M in Nx:
            if not M&E: continue
            if E<=sy:
                check('B1 E⊆Sy, N(x) M meets E => M ⊆ L(E) (y∨a class)', M<=cls(YA,E), I)
                check('B3 ... => M ⊆ E', M<=E, I)
        # T(y)-blocks meeting E: inside E? inside the x∨c class?
        for Y,ty in top_blocks(y,n):
            if ty and Y&E:
                check('A6 T(y)-block meeting E lies in x∨c class of E', Y<=cls(XC,E), I)
                check('A7 T(y)-block meeting E, E⊆Sx: Y ⊆ E', not E<=sx or Y<=E, I)
                check('A8 T(y)-block meeting E: Y ∩ Sx ⊆ E', (Y&sx)<=E, I)
print(f"{len(S)} instances")
for k in sorted(fails): print(f"  FAIL {fails[k]:6d}  {k}")
