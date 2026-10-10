"""Square hypotheses in P_n: test candidate identities for the modified third pair
a3' = a3 b1 a3 = b1*a3,  b3' = b3 a1 b3 = a1*b3,  u = a3 z a3 = (y1*y2)*x3."""
import sys, time
from pmon import Pn, projections
from digraph import clause, parse_clause, search
E=[(1,2),(2,1)]
lits=[l for l in parse_clause(clause(3,E)) if l[2]]
A3="(y1 * x3)"; B3="(x1 * y3)"; U="((y1 * y2) * x3)"
tests={
 "a3'b3' = b3'a3'": (f"{A3} * {B3}", f"{B3} * {A3}"),
 "a3'b3'a3' = u":   (f"{B3} * {A3}", U),
 "b3'a3'b3' = u":   (f"{A3} * {B3}", U),
 "a3 b1 a3 = a3 b2 a3": ("y1 * x3","y2 * x3"),
 "u = b3 w b3":     (U, "(x1 * x2) * y3"),
 "z a3 z = z":      ("x3 * (y1 * y2)","y1 * y2"),
 "a3' z a3' = u":   (f"(y1 * y2) * {A3}", U),
 "a3 b1 a3 b3 a3 b1 a3 = u": (f"y3 * {A3}", U),
}
for n in range(2, (int(sys.argv[1]) if len(sys.argv)>1 else 3)+1):
    P=Pn(n); projs=projections(n); op=lambda x,y,P=P: P.prod(y,x,y)
    for name,(l,r) in tests.items():
        t=time.time(); res=search(lits+[(l,r,False)], projs, op, distinct=False, limit=3000)
        print(f"P_{n}: {name}: counterexamples = {res if res=='timeout' else len(res)} ({time.time()-t:.0f}s)", flush=True)
        if res and res!='timeout': print("   e.g.", res[0])
