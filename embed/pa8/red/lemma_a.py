"""(a_k): every N(c)-block lying in a class Gamma_i (class of eps_a v eps_c containing T-blocks) is an N(x_k)-block.
Test along chains and the induction step.  Usage: python3 lemma_a.py m"""
import sys, time
sys.path.append('/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import table
from pa_sat import solve
m = int(sys.argv[1])
idf = lambda v: ('eq', (v, 'a'), (v, 'c'))
def gamma_pred(E, Tl, J, idx, u, v, w, p):
    """literals of: ~E(c,u,v) | T(c,u) | ~J(a,c,u,w) | ~T(a,w) | E(p,u,v)   (u != v, w != u)"""
    lits = [-E(idx['c'], u, v), Tl(idx['c'], u), -Tl(idx['a'], w), E(idx[p], u, v)]
    if w != u: lits.append(-J(idx['a'], idx['c'], u, w))
    return lits
def run(H, hyp_ps, goal_p):
    """hyp_ps: chain elements for which (a) is assumed; goal_p: element for which (a) is refuted"""
    T, idx = table(H, ('mt', 'a', 'c'))
    def extra(pool, E, Tl, J, cls, X):
        for p in hyp_ps:
            for u in X:
                for v in X:
                    for w in X:
                        if u != v: cls.append(gamma_pred(E, Tl, J, idx, u, v, w, p))
        ors = []
        for u in X:
            for v in X:
                for w in X:
                    if u != v:
                        s = pool.id(('neg', u, v, w)); ors.append(s)
                        for l in gamma_pred(E, Tl, J, idx, u, v, w, goal_p): cls.append([-s, -l])
        cls.append(ors)
    return solve(T, m, distinct=False, verbose=False, symbreak=False, extra=extra) is None
base1 = [('mt','a','c'), ('comm','x','c'), idf('x')]
base2 = base1 + [('comm','x','y'), idf('y')]
base3 = base2 + [('comm','y','z'), idf('z')]
print(f"m={m}: (a) at positions 1,2,3: {run(base1, [], 'x')} {run(base2, [], 'y')} {run(base3, [], 'z')}", flush=True)
# with a commuting end b (not identifying): is (a) true for b?  and with b|><|c?
print(f"m={m}: (a) for b with y~b (no id): {run(base2 + [('comm','y','b')], [], 'b')};  with b|><|c: {run(base2 + [('comm','y','b'), ('mt','c','b')], [], 'b')}", flush=True)
# induction step: (a) for y, y~z, z id => (a) for z ?   (no chain below y assumed)
step = [('mt','a','c'), idf('y'), ('comm','y','z'), idf('z')]
print(f"m={m}: induction step (a)(y) + y~z + z id => (a)(z): {run(step, ['y'], 'z')}", flush=True)
step2 = [('mt','a','c'), ('comm','y','b'), ('mt','c','b')]
print(f"m={m}: end step (a)(y) + y~b + b|><|c => (a)(b): {run(step2, ['y'], 'b')}", flush=True)
