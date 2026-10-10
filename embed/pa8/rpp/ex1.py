import sys, pickle, random
sys.path.insert(0,'/home/claude/pa8w/embed'); sys.path.insert(0,'/home/claude/pa8w/embed/pa8/rp')
from pmon import mul
from blocks import top_blocks, supp, join_classes
n=4; inst=pickle.load(open('w2inst4.pkl','rb')); memo={}
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
random.seed(0); S=random.sample(inst,4000); found=0
for I in S:
    a,c,b,x,y=I
    G=join_classes([a,c],n); D=join_classes([b,c],n)
    cT=[E for E,t in top_blocks(c,n) if t]; cN=[E for E,t in top_blocks(c,n) if not t]
    for C in cT:
        Di=cls(D,C)
        for E in cN:
            if not E<=Di: continue
            Ge=cls(G,E)
            bad=[F for F in cN if F<=Ge and not (cls(D,F)==Di or len([F2 for F2 in cN+cT if F2<=cls(D,F)])==1)]
            if bad:
                r=th(x,b); v=m(x,c); w=m(y,b); u=th(a,x); mm=m(x,y); s=th(y,a)
                print('instance:'); [print(f"  {nm}={fmt(p)}") for nm,p in zip('a c b x y s v w u m'.split(),(a,c,b,x,y,s,v,w,u,mm))]
                print('  C_i',set(C),'Delta_i',set(Di),'E',set(E),'Gamma(E)',set(Ge),'bad F',[set(F) for F in bad],'Delta(F)',[set(cls(D,F)) for F in bad])
                print('  Gamma classes',[set(K) for K in G],' Delta classes',[set(K) for K in D])
                found+=1
    if found: break
