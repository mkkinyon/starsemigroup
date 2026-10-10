import sys, json
from pa_sat import solve, M172
from pmon import mul, canon
def to_partition(blocks, m):
    out = []
    for b, lab in blocks:
        if lab == 'T': out.append(list(b) + [x + m for x in b])
        else: out.append(list(b)); out.append([x + m for x in b])
    return canon(out)
def verify(T, sol, m):
    P = [to_partition(b, m) for b in sol]
    if len(set(P)) != len(P): return "not injective"
    for x in range(len(T)):
        for y in range(len(T)):
            if mul(mul(P[y], P[x], m), P[y], m) != P[T[x][y]]: return f"product {x},{y} wrong"
    return "OK"
sub = [0,1,2,3,5]
T5 = [[sub.index(M172[x][y]) for y in sub] for x in sub]
for m in (3, 4, 5):
    sol = solve(T5, m, verbose=False)
    print(m, "SAT" if sol else "UNSAT", verify(T5, sol, m) if sol else "")
    if sol:
        for p, b in enumerate(sol): print("  ", p, b)
