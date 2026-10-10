import sys, time
sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import valid
P=[('mt','a','c'),('mt','c','b')]
def rpn(n):
    xs=['x','y','z','t','s'][:n]
    H=P+[('comm',xs[0],'c'),('comm',xs[-1],'a'),('eq',(xs[0],'a'),(xs[0],'c'))]+[('comm',u,v) for u,v in zip(xs,xs[1:])]+[('eq',(u,'b'),(v,'b')) for u,v in zip(xs,xs[1:])]
    return H
for n in (2,3,4):
    for m in (4,5):
        t=time.time(); print(f"(R'_{n}) m={m}: {valid(rpn(n),('mt','a','b'),m)} ({time.time()-t:.0f}s)", flush=True)
