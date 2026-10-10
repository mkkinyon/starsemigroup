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
    a,c,b,x,y=I; mm=m(x,y); s=th(y,a); v=m(x,c); w=m(y,b)
    sa,sb,sc,sx,sy,sm,ss,sv,sw=[supp(p,n) for p in (a,b,c,x,y,mm,s,v,w)]
    G=join_classes([a,c],n); D=join_classes([b,c],n); R=join_classes([a,b],n)
    cT=[E for E,t in top_blocks(c,n) if t]
    Nx=[E for E,t in top_blocks(x,n) if not t]; Ny=[E for E,t in top_blocks(y,n) if not t]
    for C in cT:
        Gi=cls(G,C); Di=cls(D,C)
        Ai=next(A for A,t in top_blocks(a,n) if t and A<=Gi); Bi=next(B for B,t in top_blocks(b,n) if t and B<=Di)
        if not C<=sx:
            check('inv: C_i = B_i', C==Bi, I); check('inv: A_i = C_i', C==Ai, I)
            check('inv: A_i meets B_i', bool(Ai&Bi), I)
            check('inv: D(A_i) contains B_i', Bi<=cls(R,Ai), I)
            check('inv: D(A_i) = Gamma_i ∪ Delta_i ?', cls(R,Ai)==Gi|Di, I)
            check('inv: M (N(x)-block of C_i) = C_i', next(N for N in Nx if C<=N)==C, I)
        else:
            check('vis: A_i meets supp v', bool(Ai&sv), I)
            check('vis: B_i meets Sy', bool(Bi&sy), I)
            check('vis: B_i meets supp s', bool(Bi&ss), I)
            check('vis: C_i meets Sy', bool(C&sy), I)
            check('vis: C_i meets supp s', bool(C&ss), I)
print(f"{len(S)} instances")
for k in sorted(fails): print(f"  FAIL {fails[k]:6d}  {k}")
