import sys, time, pickle
exec(open('goal2.py').read().split("t = time.time()")[0])
# hypotheses about y (rename x->y in the chain-invariant clauses)
Qx = pickle.load(open('invQ_m5.pkl', 'rb'))          # m=5-sound fixed point (20 clauses, about x)
ren = lambda cl: tuple((s, (a[0], 'y') if a[0] in ('E',) and a[1] == 'x' else ((a[0], 'y', a[2]) if a[0] == 'T' and a[1] == 'x' else ((a[0],) + tuple('y' if p == 'x' else p for p in a[1:]) if a[0] == 'J' else a))) for s, a in cl)
def normJ(cl):   # J atoms must have p<q
    out = []
    for s, a in cl:
        if a[0] == 'J' and a[1] > a[2]: a = ('J', a[2], a[1])
        out.append((s, a))
    return tuple(out)
Qy = [normJ(ren(cl)) for cl in Qx]
LemA = ((-1, ('E', 'c')), (1, ('J', 'a', 'y')))
G1 = ((-1, ('E', 'c')), (1, ('J', 'a', 'b')))
tests = {
 "weak + LemA => G1": (weak, [LemA], G1),
 "weak + LemA => GOAL": (weak, [LemA], GOAL),
 "weak + LemA + Qy => G1": (weak, [LemA] + Qy, G1),
 "weak + LemA + Qy => GOAL": (weak, [LemA] + Qy, GOAL),
 "(W2) => G1": (W2, [], G1),
 "(W2) => GOAL": (W2, [], GOAL),
}
for name, (H, hy, g) in tests.items():
    t = time.time(); print(f"m={m}: {name}: {holds(H, hy, g)} ({time.time()-t:.0f}s)", flush=True)
