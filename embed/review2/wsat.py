"""SAT validity of (W_n) in P(P_m) using the project's pa_sat.solve with a partial table (reviewer's harness).
Usage: python3 wsat.py n m [side]  (side: 'ba' refutes theta_a(b)=a, 'ab' refutes theta_b(a)=b)."""
import sys, time
sys.path.insert(0, '/home/claude/pa8w/review2/code')
from pa_sat import solve
n, m = int(sys.argv[1]), int(sys.argv[2]); side = sys.argv[3] if len(sys.argv) > 3 else 'ba'
names = ['a', 'c', 'b'] + [f'x{i}' for i in range(1, n + 1)] + [f'e{i}' for i in range(2, n + 1)] + [f'm{i}' for i in range(0, n + 1)] + ['ba', 'ab']
I = {s: i for i, s in enumerate(names)}; k = len(names)
T = [[None] * k for _ in range(k)]      # T[q][p] = theta_p(q)
def th(p, q, r): T[I[q]][I[p]] = I[r]   # theta_p(q) = r
for s in names: th(s, s, s)
th('a', 'c', 'a'); th('c', 'a', 'c')     # a |><| c : theta_a(c) = a, theta_c(a) = c
th('b', 'c', 'b'); th('c', 'b', 'c')     # b |><| c
chain = ['c'] + [f'x{i}' for i in range(1, n + 1)] + ['b']
for i in range(n + 1):                  # chain commutations: theta_p(q) = theta_q(p) = m_i
    p, q = chain[i], chain[i + 1]; th(p, q, f'm{i}'); th(q, p, f'm{i}')
noid = 'noid' in sys.argv
for i in range(1, n + 1):               # identifications
    if noid and i == n: continue
    e = 'm0' if i == 1 else f'e{i}'        # theta_{x1}(c) = theta_c(x1) = m0 already, so e1 = m0
    assert T[I['a']][I[f'x{i}']] is None and (i == 1 or T[I['c']][I[f'x{i}']] is None)
    th(f'x{i}', 'a', e); th(f'x{i}', 'c', e)
th('a', 'b', 'ba'); th('b', 'a', 'ab')
distinct = [(I['ba'], I['a'])] if side == 'ba' else [(I['ab'], I['b'])]
print(f'(W_{n}) in P(P_{m}), refuting {side}: {k} elements', flush=True)
t = time.time()
r = solve(T, m, distinct=distinct, verbose=True, symbreak=True)
print('result:', 'COUNTEREXAMPLE' if r else 'none (valid)', f'{time.time()-t:.0f}s', flush=True)
if r:
    for s, blocks in zip(names, r): print(s, blocks)
