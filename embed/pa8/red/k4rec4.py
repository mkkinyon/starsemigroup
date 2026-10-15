import sys, pickle, itertools
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
n = 4; P = projections(n)
INST = pickle.load(open('k4inst4.pkl', 'rb'))
stats = {}
def rec(name, val):
    s = stats.setdefault(name, [0, 0]); s[0] += 1; s[1] += val
def refines(p, J):  # every block of p inside a class of J
    return all(any(K & B == B for K in J) for B in p[0])
def refines_T(p, J): return all(any(K & B == B for K in J) for B in p[0] if B & p[1])
def refines_N(p, J): return all(any(K & B == B for K in J) for B in p[0] if not (B & p[1]))
names = ['a', 'b', 'c', 'y', 'z']
for I in INST:
    for x in names:
        for p, q in itertools.combinations([t for t in names if t != x], 2):
            J = join(I[p], I[q])
            rec('eps_%s <= eps_%s v eps_%s' % (x, p, q), refines(I[x], J))
            rec('T(%s)-blocks inside classes of eps_%s v eps_%s' % (x, p, q), refines_T(I[x], J))
            rec('N(%s)-blocks inside classes of eps_%s v eps_%s' % (x, p, q), refines_N(I[x], J))
print(len(INST), 'instances')
for k, (tot, ok) in sorted(stats.items()): 
    if ok == tot or ok == 0: print('  %-48s %d/%d%s' % (k, ok, tot, '   ALWAYS' if ok == tot else '   NEVER'))
