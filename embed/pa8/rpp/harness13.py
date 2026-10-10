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
                    if N2 in special: pairs.add((N0,N2)); continue
                    seen.add(N2); q.append(N2)
    return pairs
for I in S:
    a,c,b,x,y=I; mm=m(x,y); s=th(y,a); v=m(x,c); w=m(y,b); u=th(a,x)
    sa,sb,sc,sx,sy,sm,ss,sv,sw,su=[supp(p,n) for p in (a,b,c,x,y,mm,s,v,w,u)]
    G=join_classes([a,c],n); D=join_classes([b,c],n)
    aB=[E for E,t in top_blocks(a,n)]; bB=[E for E,t in top_blocks(b,n)]
    cT=[E for E,t in top_blocks(c,n) if t]
    GT={cls(G,C) for C in cT}; DT={cls(D,C) for C in cT}
    for name,spec in (('C8 a-blocks in T-Gamma-classes', [N for N in aB if cls(G,N) in GT]),
                      ('C8v a-blocks in T-Gamma-classes meeting Sx∪Sy', [N for N in aB if cls(G,N) in GT and N&(sx|sy)]),
                      ('C8u a-blocks meeting supp u', [N for N in aB if N&su]),
                      ('C8T T(a)-blocks', [N for N,t in top_blocks(a,n) if t]),
                      ('C8Tv T(a)-blocks + a-blocks meeting supp v', [N for N,t in top_blocks(a,n) if t or N&sv])):
        for N,N2 in consecutive(aB,bB,spec): check(name+' -> same Gamma', cls(G,N)==cls(G,N2), I)
    for name,spec in (('C9 b-blocks in T-Delta-classes', [Z for Z in bB if cls(D,Z) in DT]),
                      ('C9T T(b)-blocks', [Z for Z,t in top_blocks(b,n) if t]),
                      ('C9w T(b)-blocks + b-blocks meeting supp w', [Z for Z,t in top_blocks(b,n) if t or Z&sw]),
                      ('C9y T(b)-blocks + b-blocks meeting Sy', [Z for Z,t in top_blocks(b,n) if t or Z&sy])):
        for Z,Z2 in consecutive(bB,aB,spec): check(name+' -> same Delta', cls(D,Z)==cls(D,Z2), I)
print(f"{len(S)} instances")
for k in sorted(fails): print(f"  FAIL {fails[k]:6d}  {k}")
