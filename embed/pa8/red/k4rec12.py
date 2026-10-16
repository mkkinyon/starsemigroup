import sys, pickle
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
INST = pickle.load(open('k4inst4.pkl', 'rb'))
stats = {}
def rec(name, val):
    s = stats.setdefault(name, [0, 0]); s[0] += 1; s[1] += val
def cls_of(J, S):
    for K in J:
        if K & S: return K
for I in INST:
    a, b, c, y, z = I['a'], I['b'], I['c'], I['y'], I['z']
    Jyc = join(y, c); Jay = join(a, y); Jzy = join(z, y)
    for O in z[0]:
        if O & z[1]: continue   # outer block (N(z)-block)
        rec('outer block inside one class of eps_y v eps_c', sum(1 for K in Jyc if K & O) == 1)
        rec('outer block: y-blocks meeting it all T or all N', len({bool(Y & y[1]) for Y in y[0] if Y & O}) == 1)
        rec('outer block: c-blocks meeting it all T or all N', len({bool(C & c[1]) for C in c[0] if C & O}) == 1)
        rec('outer block meets supp y => O subset supp y', (not (O & y[1])) or O & y[1] == O)
        rec('outer block meets supp c => O subset supp c', (not (O & c[1])) or O & c[1] == O)
    for Y in y[0]:
        rec('y-block inside one class of eps_a v eps_z', sum(1 for K in join(a, z) if K & Y) == 1)
    for B in b[0]:
        rec('b-block inside one class of eps_a v eps_y v eps_z', sum(1 for K in join((tuple(Jay), 0), z) if K & B) == 1)
    # M-classes vs c-blocks
    M = join((tuple(Jay), 0), z)
    for C in c[0]:
        rec('c-block inside one M-class (eps_a v eps_y v eps_z)', sum(1 for K in M if K & C) == 1)
        rec('c-block inside one class of eps_a v eps_y', sum(1 for K in Jay if K & C) == 1)
print(len(INST), 'instances')
for k, (tot, ok) in sorted(stats.items()): print('  %-56s %d/%d%s' % (k, ok, tot, '   ALWAYS' if ok == tot else ('   NEVER' if ok == 0 else '')))
