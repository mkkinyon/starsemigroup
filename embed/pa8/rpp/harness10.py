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
def mkproj(classes, Tset):
    """projection of P_n with upper blocks = classes, transversal iff in Tset (pmon format)"""
    blocks=[]
    for K in classes:
        if K in Tset: blocks.append(tuple(sorted(list(K)+[i+n for i in K])))
        else: blocks.append(tuple(sorted(K))); blocks.append(tuple(sorted(i+n for i in K)))
    return tuple(sorted(blocks))
S = inst if len(sys.argv)<4 else random.sample(inst,int(sys.argv[3]))
fails={}
def check(name, cond):
    if not cond: fails[name]=fails.get(name,0)+1
for I in S:
    a,c,b,x,y=I
    sa,sb,sc,sx,sy=[supp(p,n) for p in (a,b,c,x,y)]
    XY=join_classes([x,y],n)
    cands={'j1 (T iff meets Sx∪Sy)': mkproj(XY,{K for K in XY if K&(sx|sy)}),
           'j2 (T iff meets Sx)': mkproj(XY,{K for K in XY if K&sx}),
           'j3 (T iff meets Sy)': mkproj(XY,{K for K in XY if K&sy}),
           'j4 (T iff meets Sx∩Sy)': mkproj(XY,{K for K in XY if K&sx&sy}),
           'm': m(x,y)}
    for nm,z in cands.items():
        check(f'{nm}: z~c', m(z,c)==m(c,z)); check(f'{nm}: z~b', m(z,b)==m(b,z)); check(f'{nm}: th_z(a)=th_z(c)', th(z,a)==th(z,c))
        check(f'{nm}: z~x', m(z,x)==m(x,z)); check(f'{nm}: z~y', m(z,y)==m(y,z))
print(f"{len(S)} instances")
for k in sorted(fails): print(f"  FAIL {fails[k]:6d}  {k}")
