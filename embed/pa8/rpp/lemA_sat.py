"""SAT test of Lemma A (every c-block lies in one class of eps_y v eps_a) under sub-hypotheses, in P(P_m)."""
import sys, time
sys.path.append('/home/claude/pa8w/embed'); sys.path.insert(0,'/home/claude/pa8w/n4')
from qi import table
from pa_sat import solve
def refute(T, idx, m, p1, p2, q1, q2, verbose=False):
    """model where some block of p1 contains two points not joined in eps_q1 v eps_q2 (p2 unused)"""
    N=len(T)
    def extra(pool, E, Tl, J, cls, X):
        ors=[]
        for x in X:
            for y in X:
                if x<y:
                    w=pool.id(('lemA',x,y)); ors.append(w)
                    cls.append([-w, E(idx[p1],x,y)]); cls.append([-w, -J(idx[q1],idx[q2],x,y)])
        cls.append(ors)
    return solve(T, m, distinct=False, verbose=verbose, symbreak=False, extra=extra)
base=[('mt','a','c')]
hyps={'x~c':('comm','x','c'),'x id':('eq',('x','a'),('x','c')),'x~y':('comm','x','y'),'y id':('eq',('y','a'),('y','c')),'y~b':('comm','y','b'),'b~c':('mt','c','b')}
import itertools
m=int(sys.argv[1])
sets={'all4':['x~c','x id','x~y','y id'], 'all4+b':['x~c','x id','x~y','y id','y~b','b~c'],
      'drop x~c':['x id','x~y','y id'], 'drop x id':['x~c','x~y','y id'], 'drop x~y':['x~c','x id','y id'], 'drop y id':['x~c','x id','x~y']}
for name,S in sets.items():
    H=base+[hyps[h] for h in S]
    T,idx=table(H,('mt','a','c'))
    t=time.time(); r=refute(T,idx,m,'c',None,'y','a')
    print(f"m={m} {name}: Lemma A {'HOLDS' if r is None else 'FAILS'} ({time.time()-t:.0f}s)", flush=True)
