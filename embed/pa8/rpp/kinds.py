"""Kinds of c-blocks in (R'') instances and the Gamma/Delta adjacency between kinds."""
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
def rel(E, p, sp):
    """relation of a set E to projection p: 'in' (E subset supp p), 'N' (E is an N(p)-block), 'subN' (E inside an N(p)-block),
    'unionN', 'mixed'"""
    if E <= sp: return 'in'
    Nb=[t for t,tr in top_blocks(p,n) if not tr]
    if E in Nb: return 'N'
    if any(E < N for N in Nb): return 'subN'
    if any(N <= E for N in Nb) and all(any(N <= E for N in Nb) or ... for _ in [0]): pass
    inter = [N for N in Nb if N & E]
    if inter and frozenset().union(*inter) == E: return 'unionN'
    return 'mixed'
S = inst if len(sys.argv)<4 else random.sample(inst,int(sys.argv[3]))
GE=set(); DE=set(); kinds=set(); samples={}
for I in S:
    a,c,b,x,y=I
    sa,sb,sc,sx,sy=[supp(p,n) for p in (a,b,c,x,y)]
    Gamma=join_classes([a,c],n); Delta=join_classes([b,c],n)
    def kind(E,tr):
        k=('T' if tr else 'N', 'x:'+rel(E,x,sx), 'y:'+rel(E,y,sy), 'a' if E&sa else '-', 'b' if E&sb else '-')
        return k
    cb=[(E,kind(E,tr)) for E,tr in top_blocks(c,n)]
    for E,k in cb: kinds.add(k); samples.setdefault(k,I)
    for cls,ES in ((Gamma,GE),(Delta,DE)):
        for K in cls:
            ks=[k for E,k in cb if E<=K]
            for k1,k2 in itertools.combinations(ks,2): ES.add(tuple(sorted((k1,k2))))
print(len(kinds),'kinds:'); 
for k in sorted(kinds): print('  ',k)
print(len(GE),'Gamma-adjacencies;',len(DE),'Delta-adjacencies')
pickle.dump((kinds,GE,DE,samples),open('kinds.pkl','wb'))
# T-blocks: which kinds share Gamma / Delta with a T(c) block?
for name,ES in (('Gamma',GE),('Delta',DE)):
    print(name,'neighbours of T(c)-blocks:')
    for k1,k2 in sorted(ES):
        if k1[0]=='T' or k2[0]=='T': print('   ',k1,'--',k2)
