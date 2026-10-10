import sys
from graphsg import semigroup, proj_algebra
from pa_sat import solve
V=[0,1,2]; E=[(0,1),(0,2),(1,2)]; B=['m0','m1','m2']; bot={0:'m0',1:'m1',2:'m2'}
elems,T,st = semigroup(V,E,bot,B); P,A = proj_algebra(elems,T,st)
print("projection algebra size", len(A)); print(A)
for m in range(2, int(sys.argv[1])+1):
    r = solve(A, m)
    if r:
        for p,b in enumerate(r): print(p, b)
        break
