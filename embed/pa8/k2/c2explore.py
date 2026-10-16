"""Candidate 2 configuration: a><a', b><b', a~b, a~b', a'~b. Always-true relations among derived elements in P_4,
and which of them fail in candidate 2 (elements 2,4,3,5)."""
import sys, json, itertools
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
n = 4; P = projections(n)
names = ['a', 'a1', 'b', 'b1', 'ab', 'ab1', 'a1b', 't', 't1', 'tt', 'tt1']
def derived(a, a1, b, b1, th):
    return {'a': a, 'a1': a1, 'b': b, 'b1': b1, 'ab': th(a, b), 'ab1': th(a, b1), 'a1b': th(a1, b),
            't': th(a1, b1), 't1': th(b1, a1), 'tt': th(a, th(a1, b1)), 'tt1': th(b, th(b1, a1))}
def rels(D, th):
    R = {}
    for e, f in itertools.permutations(names, 2):
        R['%s<=%s' % (e, f)] = th(D[f], D[e]) == D[e]
        R['th_%s(%s)=%s' % (e, f, e)] = th(D[e], D[f]) == D[e]
    for e, f in itertools.combinations(names, 2):
        R['%s=%s' % (e, f)] = D[e] == D[f]; R['%s~%s' % (e, f)] = th(D[e], D[f]) == th(D[f], D[e])
        R['%s><%s' % (e, f)] = th(D[e], D[f]) == D[e] and th(D[f], D[e]) == D[f]
    return R
always = None; cnt = 0
for a in P:
    A1 = [x for x in P if matched(a, x)]
    for b in P:
        if not commute(a, b): continue
        B1 = [x for x in P if matched(b, x) and commute(a, x)]
        for a1 in A1:
            if not commute(a1, b): continue
            for b1 in B1:
                cnt += 1
                R = rels(derived(a, a1, b, b1, theta), theta)
                if always is None: always = {k for k, v in R.items() if v}
                else: always &= {k for k, v in R.items() if v}
print(cnt, 'instances in P_4;', len(always), 'always-true relations')
T = json.load(open('../cand9.json'))[2]; th2 = lambda p, q: T[q][p]
R2 = rels(derived(2, 4, 3, 5, th2), th2)
print('always true in P_4 but FALSE in candidate 2:')
for k in sorted(always):
    if not R2[k]: print('  ', k)
