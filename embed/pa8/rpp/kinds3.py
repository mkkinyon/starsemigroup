"""Richer kinds of c-blocks on W_2 instances and the abstract alternating-walk search (both starting moves)."""
import sys, pickle, random, itertools, collections
sys.path.insert(0,'/home/claude/pa8w/embed'); sys.path.insert(0,'/home/claude/pa8w/embed/pa8/rp')
from pmon import mul
from blocks import top_blocks, supp, join_classes
n=int(sys.argv[1]); inst=pickle.load(open(sys.argv[2],'rb')); memo={}
def m(p,q):
    k=(p,q)
    if k not in memo: memo[k]=mul(p,q,n)
    return memo[k]
th=lambda p,q: m(m(p,q),p)
def rel(E, p, sp):
    if E <= sp: return 'in'
    Nb=[t for t,tr in top_blocks(p,n) if not tr]
    if E in Nb: return 'N'
    if any(E < N for N in Nb): return 'subN'
    inter=[N for N in Nb if N & E]
    if inter and frozenset().union(*inter) == E: return 'unionN'
    return 'mixed'
S = inst if len(sys.argv)<4 else random.sample(inst,int(sys.argv[3]))
GE=set(); DE=set(); kinds=set()
for I in S:
    a,c,b,x,y=I; mm=m(x,y); s=th(y,a); r=th(x,b); v=m(x,c); w=m(y,b); u=th(a,x)
    sa,sb,sx,sy,sm,ss,sr,sv,sw,su=[supp(p,n) for p in (a,b,x,y,mm,s,r,v,w,u)]
    Gamma=join_classes([a,c],n); Delta=join_classes([b,c],n)
    cb=top_blocks(c,n)
    GT={K for K in Gamma if any(tr and E<=K for E,tr in cb)}; DT={K for K in Delta if any(tr and E<=K for E,tr in cb)}
    def kind(E,tr):
        G=next(K for K in Gamma if E<=K); D=next(K for K in Delta if E<=K)
        return ('T' if tr else 'N', 'x:'+rel(E,x,sx), 'y:'+rel(E,y,sy), 'm:'+rel(E,mm,sm),
                'a' if E&sa else '-', 'b' if E&sb else '-', 's' if E&ss else '-', 'r' if E&sr else '-',
                'GT' if G in GT else 'g0', 'DT' if D in DT else 'd0')
    kb=[(E,kind(E,tr)) for E,tr in cb]
    for E,k in kb: kinds.add(k)
    for cls_,ES in ((Gamma,GE),(Delta,DE)):
        for K in cls_:
            ks=[k for E,k in kb if E<=K]
            for k1,k2 in itertools.combinations(ks,2): ES.add((k1,k2)); ES.add((k2,k1))
print(len(kinds),'kinds;',len(GE)//2,'Gamma-adj;',len(DE)//2,'Delta-adj', flush=True)
pickle.dump((kinds,GE,DE),open(sys.argv[4] if len(sys.argv)>4 else 'kinds3.pkl','wb'))
