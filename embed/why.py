import sys, time
from qsub4 import gen_sub, a0, a1, a2, b0, b1, b2, Tq, sq
from embed import PnData, find_embedding, check_embedding
from pmon import projections, rank
n = 3
D = PnData(n); P = D.P
Ts, ss, S = gen_sub([a0, a1, a2, b0, b1])
loc = {x: i for i, x in enumerate(S)}
sols = find_embedding(Ts, ss, D, all_solutions=True, limit=50, use_symmetry=True)
print(len(sols), "embeddings of <a0,a1,a2,b0,b1> into P_3 (with a0 fixed to an orbit rep)")
def show(p): return p
for sol in sols[:6]:
    A0, A1, A2, B0, B1 = (sol[loc[x]] for x in (a0, a1, a2, b0, b1))
    print("\n a0 =", A0, "\n a1 =", A1, "\n a2 =", A2, "\n b0 =", B0, "\n b1 =", B1)
    # candidates for b2: projections q with a0 q a0 = a0, q a0 q = q, a1 q a1 = a1, q a1 q = q
    cands = [q for q in projections(n) if P.prod(A0, q, A0) == A0 and P.prod(q, A0, q) == q and P.prod(A1, q, A1) == A1 and P.prod(q, A1, q) == q]
    print("  candidates q with a0 ~ q ~ a1:", len(cands))
    Z = P.mul(B0, B1); W = P.mul(A0, A1); M2 = None
    for q in cands:
        fails = []
        if P.mul(B0, q) != Z: fails.append("b0 q != z")
        if P.mul(q, B0) != Z: fails.append("q b0 != z")
        if P.mul(B1, q) != Z: fails.append("b1 q != z")
        if P.mul(A2, q) != P.mul(q, A2): fails.append("a2 q != q a2")
        if P.prod(A0, q, A2) != P.prod(A0, A2, q): pass
        # theta relations: q W q should be m2 = a2 q ; a2 z a2 = m2...
        m2 = P.mul(A2, q)
        if P.prod(q, W, q) != m2: fails.append("theta_q(w) != m2")
        if P.prod(A2, Z, A2) != m2: fails.append("theta_a2(z) != m2")
        print("   q =", q, "rank", rank(q, n), "fails:", fails if fails else "NONE?!")
