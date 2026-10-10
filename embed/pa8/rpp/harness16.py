import sys, pickle, random, itertools
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
fails={}; cnt=0
def check(name, cond):
    global fails
    if not cond: fails[name]=fails.get(name,0)+1
def cls(J,E): return next(K for K in J if E<=K)
for I in S:
    a,c,b,x,y=I; w=m(y,b); v=m(x,c); u=th(a,x); s=th(y,a); mm=m(x,y)
    G=join_classes([a,c],n); D=join_classes([b,c],n); YC=join_classes([y,c],n); YA=join_classes([y,a],n); XA=join_classes([x,a],n); XC=join_classes([x,c],n)
    YB=join_classes([y,b],n); XB=join_classes([x,b],n); MA=join_classes([mm,a],n); MC=join_classes([mm,c],n); MB=join_classes([mm,b],n)
    cT=[E for E,t in top_blocks(c,n) if t]
    W=[E for E,t in top_blocks(w,n) if t]
    trip=[]
    for C in cT:
        Gi=cls(G,C); Di=cls(D,C)
        A=next(A for A,t in top_blocks(a,n) if t and A<=Gi); B=next(B for B,t in top_blocks(b,n) if t and B<=Di)
        trip.append((A,C,B))
    for (A1,C1,B1),(A2,C2,B2) in itertools.combinations(trip,2):
        same_W = any(B1<=Wl and B2<=Wl for Wl in W)
        if same_W:
            cnt+=1
            check('W1 same W_l => C_i,C_j in different y∨c classes', cls(YC,C1)!=cls(YC,C2))
            check('W2 same W_l => A_i,A_j in different y∨a classes', cls(YA,A1)!=cls(YA,A2))
            check('W3 same W_l => A_i,A_j in different x∨a classes', cls(XA,A1)!=cls(XA,A2))
            check('W4 same W_l => C_i,C_j in different x∨c classes', cls(XC,C1)!=cls(XC,C2))
            check('W5 same W_l => C_i,C_j in different m∨c classes', cls(MC,C1)!=cls(MC,C2))
            check('W6 same W_l => B_i,B_j in different x∨b classes', cls(XB,B1)!=cls(XB,B2))
            check('W7 same W_l => B_i,B_j in different m∨b classes', cls(MB,B1)!=cls(MB,B2))
        same_V = any(C1<=Vk and C2<=Vk for Vk,t in top_blocks(v,n) if t)
        if same_V:
            check('V1 same V_k => B_i,B_j in different y∨b classes', cls(YB,B1)!=cls(YB,B2))
            check('V2 same V_k => A_i,A_j in different y∨a classes', cls(YA,A1)!=cls(YA,A2))
            check('V3 same V_k => C_i,C_j in different y∨c classes', cls(YC,C1)!=cls(YC,C2))
            check('V4 same V_k => B_i,B_j in different m∨b classes', cls(MB,B1)!=cls(MB,B2))
print(f"{len(S)} instances, {cnt} pairs in a common W_l")
for k in sorted(fails): print(f"  FAIL {fails[k]:6d}  {k}")
