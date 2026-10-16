"""Several structure-first minimal hypothesis sets for candidate 1's diagram (SAT m=5), different priorities/seeds."""
import json, sys, itertools, time, random
sys.path.insert(0, '/home/claude/pa8w/n4'); sys.path.append('/home/claude/pa8w/embed')
from qi import valid
exec(open('diag1.py').read().split("print(len(A)")[0])
path = [('mt', 'a', 'c'), ('mt', 'c', 'b')]; concl = ('mt', 'a', 'b')
PRIOS = [{'eq': 0, 'ident': 1, 'comm': 2, 'order': 3, 'half': 4}, {'eq': 0, 'ident': 1, 'half': 2, 'comm': 3, 'order': 4},
         {'eq': 0, 'comm': 1, 'ident': 2, 'order': 3, 'half': 4}, {'eq': 0, 'half': 1, 'ident': 2, 'comm': 3, 'order': 4},
         {'eq': 0, 'ident': 1, 'order': 2, 'comm': 3, 'half': 4}, {'eq': 0, 'ident': 1, 'comm': 2, 'order': 3, 'half': 4}]
seed = int(sys.argv[1]); random.seed(seed); prio = PRIOS[seed % len(PRIOS)]
order = sorted(range(len(A)), key=lambda i: (prio[A[i][0].split()[0]], random.random()))
keep = set(range(len(A)))
for i in order:
    if valid(path + [A[j][1] for j in sorted(keep - {i})], concl, 5): keep.discard(i)
print('seed %d prio %s: %d atoms:' % (seed, prio, len(keep)), ' | '.join(A[i][0] for i in sorted(keep, key=lambda i: prio[A[i][0].split()[0]])), flush=True)
t0 = time.time(); print('   valid at m=6:', valid(path + [A[i][1] for i in keep], concl, 6), '(%.0fs)' % (time.time() - t0), flush=True)
