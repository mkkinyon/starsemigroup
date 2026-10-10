import sys, pickle, random
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
fails={}
def check(name, cond):
    if not cond: fails[name]=fails.get(name,0)+1
def J(*ps): return frozenset(join_classes(list(ps),n))
for I in S:
    a,c,b,x,y=I; mm=m(x,y); s=th(y,a); v=m(x,c); w=m(y,b); u=th(a,x)
    tests={'y∨a∨b = y∨c∨b': J(y,a,b)==J(y,c,b), 'x∨a∨b = x∨c∨b': J(x,a,b)==J(x,c,b), 'x∨y∨a∨b = x∨y∨c∨b': J(x,y,a,b)==J(x,y,c,b),
           'm∨a = m∨c': J(mm,a)==J(mm,c), 'm∨a∨b = m∨c∨b': J(mm,a,b)==J(mm,c,b), 'y∨a = y∨c': J(y,a)==J(y,c), 'x∨a = x∨c': J(x,a)==J(x,c),
           'y∨a∨c = y∨a': J(y,a,c)==J(y,a), 'x∨a∨c = x∨a': J(x,a,c)==J(x,a), 'y∨a∨c = y∨c': J(y,a,c)==J(y,c),
           's∨a = s∨c': J(s,a)==J(s,c), 'v∨a = v∨c': J(v,a)==J(v,c), 'u∨c = u∨a': J(u,c)==J(u,a), 'w∨a = w∨c': J(w,a)==J(w,c),
           'a∨b∨x∨y = a∨c∨b∨x∨y': J(a,b,x,y)==J(a,b,c,x,y), 'a∨b∨y = a∨b∨c∨y': J(a,b,y)==J(a,b,c,y), 'a∨b∨x = a∨b∨c∨x': J(a,b,x)==J(a,b,c,x),
           'a∨b = a∨b∨c': J(a,b)==J(a,b,c), 'a∨b∨m = a∨b∨c∨m': J(a,b,mm)==J(a,b,c,mm), 'a∨b∨s = a∨b∨c∨s': J(a,b,s)==J(a,b,c,s), 'a∨b∨w = a∨b∨c∨w': J(a,b,w)==J(a,b,c,w)}
    for k,vv in tests.items(): check(k,vv)
print(f"{len(S)} instances")
for k in sorted(fails): print(f"  FAIL {fails[k]:6d}  {k}")
