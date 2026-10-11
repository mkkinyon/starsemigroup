"""Candidate chain invariants (3-point language), propagation fixed point, and the end step.  Usage: python3 invfam.py m"""
import sys, time, pickle
sys.path.append('/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import table
from pa_sat import solve
exec(open('inv4.py').read().split("def run(H, hyps, goal):")[0].split("class Ctx: pass")[1])   # make_J3
m = int(sys.argv[1])
idf = lambda v: ('eq', (v, 'a'), (v, 'c'))
# a predicate: name, arity (2 or 3), function(ctx, p, u, v, w) -> list of literals (clause, universally quantified)
# ctx has E, Tl, J, J3(p) (join a,c,p), idx
def J3(c, p, u, v): return c.J3s[p](u, v)
PRED = {
 'a_Gamma':  (3, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), c.Tl(c.i['c'], u), -c.Tl(c.i['a'], w), c.E(c.i[p], u, v)] + ([-c.J(c.i['a'], c.i['c'], u, w)] if w != u else [])),
 'A':        (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), c.J(c.i['a'], c.i[p], u, v)]),
 'M':        (2, lambda c, p, u, v, w: [c.E(c.i['c'], u, v), -c.J(c.i['a'], c.i['c'], u, v), -c.J(c.i['c'], c.i[p], u, v)]),
 "G2'":      (2, lambda c, p, u, v, w: [-J3(c, p, u, v), -c.Tl(c.i['c'], u), -c.Tl(c.i['c'], v), c.J(c.i['c'], c.i[p], u, v)]),
 "G2'a":     (2, lambda c, p, u, v, w: [-J3(c, p, u, v), -c.Tl(c.i['a'], u), -c.Tl(c.i['a'], v), c.J(c.i['a'], c.i[p], u, v)]),
 'N1':       (2, lambda c, p, u, v, w: [-c.E(c.i[p], u, v), c.Tl(c.i[p], u), -c.Tl(c.i['a'], u), c.Tl(c.i['c'], u), c.J(c.i['a'], c.i['c'], u, v)]),
 'N2':       (2, lambda c, p, u, v, w: [-c.E(c.i[p], u, v), c.Tl(c.i[p], u), -c.Tl(c.i['a'], u), c.Tl(c.i['c'], u), c.Tl(c.i['c'], v), c.E(c.i['c'], u, v)]),
 'S':        (2, lambda c, p, u, v, w: [-c.Tl(c.i[p], u), -c.Tl(c.i['a'], u), c.Tl(c.i['c'], u)]),
 'Cin':      (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), -c.Tl(c.i['c'], u), c.Tl(c.i[p], u), c.E(c.i[p], u, v)]),
 'Nin':      (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), c.Tl(c.i['c'], u), c.Tl(c.i[p], u), c.E(c.i[p], u, v)]),
 'Tc_in_p':  (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), -c.Tl(c.i['c'], u), -c.Tl(c.i[p], u), c.Tl(c.i[p], v)]),   # T(c)-block meeting supp p inside it
 'ac_le_ap': (2, lambda c, p, u, v, w: [-c.J(c.i['a'], c.i['c'], u, v), c.J(c.i['a'], c.i[p], u, v)]),
 'cp_le_ap': (2, lambda c, p, u, v, w: [-c.J(c.i['c'], c.i[p], u, v), c.J(c.i['a'], c.i[p], u, v)]),
 'Ma':       (2, lambda c, p, u, v, w: [c.E(c.i['a'], u, v), -c.J(c.i['a'], c.i['c'], u, v), -c.J(c.i['a'], c.i[p], u, v)]),
 'Mp':       (2, lambda c, p, u, v, w: [c.E(c.i[p], u, v), -c.J(c.i['a'], c.i[p], u, v), -c.J(c.i['c'], c.i[p], u, v)]),
 'pAC':      (2, lambda c, p, u, v, w: [c.E(c.i['c'], u, v), -c.E(c.i[p], u, v), -c.J(c.i['a'], c.i['c'], u, v)]),
 'aCP':      (2, lambda c, p, u, v, w: [c.E(c.i['c'], u, v), -c.E(c.i['a'], u, v), -c.J(c.i['c'], c.i[p], u, v)]),
}
class Ctx: pass
def run(H, hyps, goal):
    """hyps: list of (predname, element); goal: (predname, element) to refute"""
    T, idx = table(H, ('mt', 'a', 'c'))
    def extra(pool, E, Tl, J, cls, X):
        c = Ctx(); c.E, c.Tl, c.J = E, Tl, J; c.i = {k: idx[k] for k in idx if isinstance(k, str)}; c.J3s = {}
        for (_, p) in hyps + [goal]:
            if p not in c.J3s: c.J3s[p] = make_J3(pool, cls, E, X, tuple(sorted((idx['a'], idx['c'], idx[p]))), p)
        for name, p in hyps:
            ar, f = PRED[name]
            for u in X:
                for v in X:
                    if u == v: continue
                    for w in (X if ar == 3 else [u]):
                        cls.append(f(c, p, u, v, w))
        name, p = goal; ar, f = PRED[name]; ors = []
        for u in X:
            for v in X:
                if u == v: continue
                for w in (X if ar == 3 else [u]):
                    s = pool.id(('neg', u, v, w)); ors.append(s)
                    for l in f(c, p, u, v, w): cls.append([-s, -l])
        cls.append(ors)
    return solve(T, m, distinct=False, verbose=False, symbreak=False, extra=extra) is None
if __name__ == '__main__':
    base1 = [('mt','a','c'), ('comm','x','c'), idf('x')]
    base2 = base1 + [('comm','x','y'), idf('y')]
    base3 = base2 + [('comm','y','z'), idf('z')]
    t0 = time.time(); valid = []
    for name in PRED:
        r = (run(base1, [], (name, 'x')), run(base2, [], (name, 'y')), run(base3, [], (name, 'z')))
        print(f"m={m} {name:9s}: positions 1,2,3: {r}", flush=True)
        if all(r): valid.append(name)
    print(f"chain-valid: {valid} ({time.time()-t0:.0f}s)", flush=True)
    step = [('mt','a','c'), idf('y'), ('comm','y','z'), idf('z')]
    Q = list(valid)
    while True:
        good = [nm for nm in Q if run(step, [(q, 'y') for q in Q], (nm, 'z'))]
        print(f"propagation: {len(good)} of {len(Q)}: {good} ({time.time()-t0:.0f}s)", flush=True)
        if len(good) == len(Q): break
        Q = good
    print("fixed point:", Q)
    end = [('mt','a','c'), ('mt','c','b'), ('comm','y','b')]
    for nm in ['a_Gamma', 'A', 'M', "G2'", 'Cin', 'Nin']:
        print(f"end step: I(y) + y~b + b|><|c => {nm}(b): {run(end, [(q, 'y') for q in Q], (nm, 'b'))}", flush=True)
