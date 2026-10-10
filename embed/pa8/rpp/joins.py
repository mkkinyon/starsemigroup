"""Which joins of partitions are below which, on (R'') instances."""
import sys, pickle, random, itertools
sys.path.insert(0,'/home/claude/pa8w/embed'); sys.path.insert(0,'/home/claude/pa8w/embed/pa8/rp')
from pmon import mul
from blocks import join_classes
n=int(sys.argv[1]); inst=pickle.load(open(sys.argv[2],'rb')); memo={}
def m(p,q):
    k=(p,q)
    if k not in memo: memo[k]=mul(p,q,n)
    return memo[k]
th=lambda p,q: m(m(p,q),p)
S = inst if len(sys.argv)<4 else random.sample(inst,int(sys.argv[3]))
names='a c b x y r v w u m'.split()
pairs=[(p,q) for p in itertools.combinations(names,2) for q in itertools.combinations(names,2) if p!=q]
singles=[((p,),q) for p in names for q in itertools.combinations(names,2) if p not in q]
tests=pairs+singles
def leq(P,Q):  # every class of P inside a class of Q
    return all(any(C<=D for D in Q) for C in P)
fails={t:0 for t in tests}
for I in S:
    a,c,b,x,y=I; r=th(x,b); v=m(x,c); w=m(y,b); u=th(a,x); mm=m(x,y)
    E=dict(zip(names,(a,c,b,x,y,r,v,w,u,mm)))
    J={}
    def jc(t):
        if t not in J: J[t]=join_classes([E[s] for s in t],n)
        return J[t]
    for t in tests:
        if fails[t]>0: continue
        if not leq(jc(t[0]),jc(t[1])): fails[t]+=1
for t,f in fails.items():
    if f==0 and not set(t[0])<=set(t[1]): print('∨'.join(t[0]),'<=','∨'.join(t[1]))
