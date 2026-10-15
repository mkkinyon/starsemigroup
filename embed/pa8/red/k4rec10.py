import sys, pickle, itertools
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
INST = pickle.load(open('k4inst4.pkl', 'rb'))
stats = {}
def rec(name, val):
    s = stats.setdefault(name, [0, 0]); s[0] += 1; s[1] += val
def cls_of(J, S):
    for K in J:
        if K & S: return K
def meet_is(p, J1, J2):  # (eps_p v J1) ^ (eps_p v J2) == eps_p : no two p-blocks share a class in both joins
    blocks = p[0]
    for X, Y in itertools.combinations(blocks, 2):
        if cls_of(J1, X) & Y and cls_of(J2, X) & Y: return False
    return True
names = ['a', 'b', 'c', 'y', 'z']
for I in INST:
    for p in names:
        for q1, q2 in itertools.combinations([t for t in names if t != p], 2):
            J1 = join(I[p], I[q1]); J2 = join(I[p], I[q2])
            rec('(e_%s v e_%s) ^ (e_%s v e_%s) = e_%s' % (p, q1, p, q2, p), meet_is(I[p], J1, J2))
print(len(INST), 'instances')
for k, (tot, ok) in sorted(stats.items()): print('  %-40s %d/%d%s' % (k, ok, tot, '   ALWAYS' if ok == tot else ('   NEVER' if ok == 0 else '')))
