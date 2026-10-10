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
stats=collections.Counter(); shown=0
for I in S:
    a,c,b,x,y=I
    sy=supp(y,n); sx=supp(x,n)
    aB=[E for E,t in top_blocks(a,n)]; bB=[E for E,t in top_blocks(b,n)]
    special=[Z for Z in bB if Z&sy]
    adjB={Z:[N for N in aB if N&Z] for Z in bB}; adjA={N:[Z for Z in bB if N&Z] for N in aB}
    for Z0 in special:
        # BFS recording shortest paths (interior b-blocks not special)
        prev={Z0:None}; q=collections.deque([Z0])
        while q:
            Z=q.popleft()
            for N in adjB[Z]:
                for Z2 in adjA[N]:
                    if Z2 in prev: continue
                    prev[Z2]=(Z,N)
                    if Z2 in special:
                        # path length
                        L=0; cur=Z2
                        while prev[cur]: cur=prev[cur][0]; L+=1
                        stats[L]+=1
                        if L>=2 and shown<4 and Z2!=Z0:
                            shown+=1; path=[]; cur=Z2
                            while prev[cur]: path.append(cur); path.append(prev[cur][1]); cur=prev[cur][0]
                            path.append(Z0); path.reverse()
                            print('chain (b,a,b,...):', [set(B) for B in path])
                            for nm,p in zip('a c b x y'.split(),(a,c,b,x,y)): print(f"  {nm}={fmt(p)}")
                    else: q.append(Z2)
print(stats)
