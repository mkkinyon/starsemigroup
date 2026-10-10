import sys, time, pickle
from qsub4 import gen_sub, a0, a1, a2, b0, b1, b2, Tq, sq
from congr import congruence_closure, canon_part, quotient, all_congruences
from analyse import props
Ts, ss, S = gen_sub([a0,a1,a2,b0,b1,b2])
loc = {x: i for i, x in enumerate(S)}
A = [loc[x] for x in (a0,a1,a2,b0,b1,b2)]
print("|Q0| =", len(Ts))
def hex_hyps_hold(T, st, A):
    a = A[:3]; b = A[3:]
    mul = lambda x, y: T[x][y]
    w = mul(a[0], a[1]); z = mul(b[0], b[1])
    ok = True
    for i in range(3):
        for j in range(3):
            if i != j:
                ok &= mul(a[i], a[j]) == w and mul(b[i], b[j]) == z
                ok &= mul(mul(a[i], b[j]), a[i]) == a[i] and mul(mul(b[j], a[i]), b[j]) == b[j]
                m_j = mul(a[j], b[j])
                ok &= mul(mul(b[i], m_j), b[i]) == z and mul(mul(a[i], m_j), a[i]) == w
        m_i = mul(a[i], b[i])
        ok &= mul(b[i], a[i]) == m_i
        ok &= mul(mul(a[i], z), a[i]) == m_i and mul(mul(b[i], w), b[i]) == m_i
    return ok, (w != z)
print("hexagon hypotheses hold in Q0 and w != z:", hex_hyps_hold(Ts, ss, A))
# all *-congruences of Q0 and quotients where the hypotheses still hold with w != z
t = time.time(); congs = all_congruences(Ts, ss); print(len(congs), "congruences", f"({time.time()-t:.0f}s)")
best = None
for c in sorted(congs, key=lambda c: len(set(c))):
    Tq2, sq2 = quotient(Ts, ss, c)
    # images of the generators
    classes = sorted(set(c)); qidx = {cl: i for i, cl in enumerate(classes)}
    A2 = [qidx[c[x]] for x in A]
    ok, distinct = hex_hyps_hold(Tq2, sq2, A2)
    pr = props(Tq2, sq2)
    if ok and distinct:
        print(f"  quotient size {len(Tq2)}: hyps hold, w!=z, Q1={pr['Q1']}, nP={pr['nP']}, inverse={pr['inverse']}")
        if best is None: best = (Tq2, sq2, A2)
pickle.dump(best, open("hex_smallest.pkl", "wb"))
