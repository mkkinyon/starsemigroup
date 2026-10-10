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
random.seed(2); S=random.sample(inst,int(sys.argv[3])); shown=0
for I in S:
    a,c,b,x,y=I; sx=supp(x,n); sy=supp(y,n)
    Ny=[E for E,t in top_blocks(y,n) if not t]
    aB=[E for E,t in top_blocks(a,n)]; yB=[E for E,t in top_blocks(y,n)]
    for E,t in top_blocks(c,n):
        if not E<=sx or not E&sy: continue
        for M in Ny:
            if not (M&E) or M<=E: continue
            # shortest a/y chain from M to a T(y)-block meeting E
            targets=[Y for Y,ty in top_blocks(y,n) if ty and Y&E]
            prev={M:None}; q=collections.deque([M]); found=None
            while q and not found:
                B=q.popleft()
                nxt = aB if B in yB else yB
                for B2 in nxt:
                    if B2&B and B2 not in prev:
                        prev[B2]=B
                        if B2 in targets: found=B2; break
                        q.append(B2)
            path=[]; cur=found
            while cur is not None: path.append(set(cur)); cur=prev[cur]
            print(f"E={set(E)} (c-block ⊆ Sx, meets Sy), M={set(M)} (N(y)⊆Sx, meets E, not ⊆ E); chain M->E∩Sy (y/a blocks): {path[::-1]}")
            for nm,p in zip('a c x y'.split(),(a,c,x,y)): print(f"   {nm}={fmt(p)}")
            shown+=1
            if shown>=4: sys.exit()
