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
fails={}; ex={}
def check(name, cond, I):
    if not cond:
        fails[name]=fails.get(name,0)+1; ex.setdefault(name,I)
def traces(J, Sup, Sq):
    """set of (trace on Sup, meets Sq) for classes of J meeting Sup"""
    return {(K&Sup, bool(K&Sq)) for K in J if K&Sup}
for I in S:
    a,c,b,x,y=I; mm=m(x,y)
    sa,sb,sc,sx,sy,sm=[supp(p,n) for p in (a,b,c,x,y,mm)]
    XYA=join_classes([x,y,a],n); XYC=join_classes([x,y,c],n); XYB=join_classes([x,y,b],n)
    check('J1 traces of x∨y∨a and x∨y∨c on Sx∪Sy agree', traces(XYA,sx|sy,sa)==traces(XYC,sx|sy,sc), I)
    check('J2 traces on Sx agree', traces(XYA,sx,sa)==traces(XYC,sx,sc), I)
    check('J3 traces on Sy agree', traces(XYA,sy,sa)==traces(XYC,sy,sc), I)
    check('J4 traces on supp m agree', traces(XYA,sm,sa)==traces(XYC,sm,sc), I)
    XA=join_classes([x,a],n); YC=join_classes([y,c],n); YA=join_classes([y,a],n); XC=join_classes([x,c],n)
    # does x∨y∨a = (x∨a) joined with (y∨a) trivially; test: x∨a classes vs y∨c classes on Sx∩Sy
    check('J5 traces of x∨a and y∨c on Sx∩Sy agree', traces(XA,sx&sy,sa)==traces(YC,sx&sy,sc), I)
    check('J6 traces of x∨a and y∨a on Sx∩Sy agree', traces(XA,sx&sy,sa)==traces(YA,sx&sy,sa), I)
    check('J7 traces of x∨c and y∨c on Sx∩Sy agree', traces(XC,sx&sy,sc)==traces(YC,sx&sy,sc), I)
print(f"{len(S)} instances")
for k in sorted(fails): print(f"  FAIL {fails[k]:6d}  {k}")
