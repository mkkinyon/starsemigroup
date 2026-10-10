import sys, pickle, random, collections
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
def consecutive(Ablocks, Bblocks, special):
    """pairs (N,N') of special A-blocks joined by an alternating chain (A,B,A,...) whose interior A-blocks are not special"""
    # graph: A-blocks and B-blocks adjacent if they meet
    adjA={N:[Z for Z in Bblocks if N&Z] for N in Ablocks}
    adjB={Z:[N for N in Ablocks if N&Z] for Z in Bblocks}
    pairs=set()
    for N0 in special:
        seen={N0}; q=collections.deque([N0])
        while q:
            N=q.popleft()
            for Z in adjA[N]:
                for N2 in adjB[Z]:
                    if N2 in seen: continue
                    if N2 in special: pairs.add((N0,N2)); continue   # don't pass through special
                    seen.add(N2); q.append(N2)
    return pairs
for I in S:
    a,c,b,x,y=I; mm=m(x,y); s=th(y,a); v=m(x,c); w=m(y,b)
    sa,sb,sc,sx,sy,sm,ss,sv,sw=[supp(p,n) for p in (a,b,c,x,y,mm,s,v,w)]
    G=join_classes([a,c],n); D=join_classes([b,c],n); YC=join_classes([y,c],n); YA=join_classes([y,a],n); XA=join_classes([x,a],n)
    aB=[E for E,t in top_blocks(a,n)]; bB=[E for E,t in top_blocks(b,n)]
    for name,spec,J in (('C1 a-blocks meeting Sx -> same Gamma', [N for N in aB if N&sx], G),
                        ('C2 a-blocks meeting Sy -> same Gamma', [N for N in aB if N&sy], G),
                        ('C3 a-blocks meeting Sx∪Sy -> same Gamma', [N for N in aB if N&(sx|sy)], G),
                        ('C2y a-blocks meeting Sy -> same YA-class', [N for N in aB if N&sy], YA),
                        ('C1x a-blocks meeting Sx -> same XA-class', [N for N in aB if N&sx], XA),
                        ('C5 a-blocks meeting supp m -> same Gamma', [N for N in aB if N&sm], G),
                        ('C6 a-blocks meeting supp v -> same Gamma', [N for N in aB if N&sv], G),
                        ('C7 a-blocks meeting supp s -> same Gamma', [N for N in aB if N&ss], G)):
        for N,N2 in consecutive(aB,bB,spec):
            check(name, cls(J,N)==cls(J,N2), I)
    for name,spec,J in (('C4 b-blocks meeting Sy -> same Delta', [Z for Z in bB if Z&sy], D),
                        ('C4x b-blocks meeting Sx -> same Delta', [Z for Z in bB if Z&sx], D),
                        ('C4w b-blocks meeting supp w -> same Delta', [Z for Z in bB if Z&sw], D),
                        ('C4s b-blocks meeting supp s -> same Delta', [Z for Z in bB if Z&ss], D),
                        ('C4m b-blocks meeting supp m -> same Delta', [Z for Z in bB if Z&sm], D),
                        ('C4yc b-blocks meeting Sy -> same YC-class', [Z for Z in bB if Z&sy], YC)):
        for Z,Z2 in consecutive(bB,aB,spec):
            if J is YC: check(name, any(Z<=K and Z2<=K for K in YC), I)
            else: check(name, cls(J,Z)==cls(J,Z2), I)
print(f"{len(S)} instances")
for k in sorted(fails): print(f"  FAIL {fails[k]:6d}  {k}")
pickle.dump(ex,open('harness11_ex.pkl','wb'))
