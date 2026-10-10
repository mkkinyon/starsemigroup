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
def fmt(p):
    out=[]
    for bl in p:
        top=[i for i in bl if i<n]; bot=[i-n for i in bl if i>=n]
        if top: out.append(''.join(map(str,top))+('T' if bot else ''))
    return '|'.join(out)
def cls(J,E): return next(K for K in J if E<=K)
S = inst if len(sys.argv)<4 else random.sample(inst,int(sys.argv[3]))
best=[]
for I in S:
    a,c,b,x,y=I
    if len(set(I))<5: continue
    G=join_classes([a,c],n); D=join_classes([b,c],n)
    cb=[E for E,t in top_blocks(c,n)]; cT=[E for E,t in top_blocks(c,n) if t]
    for C in cT:
        # BFS over (block, next move) with class-distinctness along the path (track used classes)
        q=collections.deque([(C,'D',[C],frozenset([cls(G,C)]),frozenset())]); depth=0; path=None
        while q:
            E,mv,p,usedG,usedD=q.popleft()
            if len(p)-1>depth: depth=len(p)-1; path=p
            if mv=='D':
                K=cls(D,E)
                if K in usedD: continue
                for E2 in cb:
                    if E2<=K and E2!=E: q.append((E2,'G',p+[E2],usedG,usedD|{K}))
            else:
                K=cls(G,E)
                if K in usedG: continue
                for E2 in cb:
                    if E2<=K and E2!=E: q.append((E2,'D',p+[E2],usedG|{K},usedD))
        best.append((depth,I,path))
best.sort(key=lambda t:-t[0])
print('depth distribution', collections.Counter(d for d,_,_ in best).most_common())
for depth,I,path in best[:4]:
    a,c,b,x,y=I; r=th(x,b); v=m(x,c); w=m(y,b); u=th(a,x)
    print(f"\ndepth {depth}: path {[set(E) for E in path]}")
    for nm,p in zip('a c b x y r v w u'.split(),(a,c,b,x,y,r,v,w,u)): print(f"  {nm}={fmt(p)}")
