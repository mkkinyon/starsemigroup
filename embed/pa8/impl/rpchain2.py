import sys, time
sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import valid
P = [('mt','a','c'), ('mt','c','b')]
def fam(n):   # c ~ x1 ~ ... ~ xn, x1 identifies a with c, y ~ a, th_{xn}(b) = th_y(b)
    xs = ['x','z','t','s'][:n]
    return P + [('comm',xs[0],'c'), ('eq',(xs[0],'a'),(xs[0],'c'))] + [('comm',u,v) for u,v in zip(xs,xs[1:])] + [('comm','y','a'), ('eq',(xs[-1],'b'),('y','b'))]
def fam2(n):  # all x_i identify a with c
    xs = ['x','z','t','s'][:n]
    return P + [('comm',xs[0],'c')] + [('eq',(u,'a'),(u,'c')) for u in xs] + [('comm',u,v) for u,v in zip(xs,xs[1:])] + [('comm','y','a'), ('eq',(xs[-1],'b'),('y','b'))]
for name, f in (('fam',fam), ('fam2',fam2)):
    for n in (1,2,3):
        for m in (4,5):
            t = time.time(); r = valid(f(n), ('mt','a','b'), m); print(f"{name} n={n} m={m}: {r} ({time.time()-t:.0f}s)", flush=True)
            if not r: break
