import sys, os, time
sys.path.insert(0, '/home/claude/pa8w')
from indep import mace_search
wd = '/home/claude/pa8w/m4indep2'; os.makedirs(wd, exist_ok=True)
jobs = [(['Q1', 'Q'], Y) for Y in ['Q1', 'Tri', 'S', 'V', 'P1', 'P2', 'E6', 'E1']] + \
       [(['Q1', 'E1'], Y) for Y in ['Q1', 'Tri', 'R', "R'", 'V', 'P1']] + \
       [(['Q1', "R'"], 'R'), (['Q1', 'P2'], 'S'), (['Q1', 'E6'], 'S'), (['Q1', 'S', 'R', 'Q'], 'P2'), (['Q1', 'S', 'R', 'P2'], 'Q'), (['Q1', 'S', 'R', 'E6'], 'Q'), (['Q1', 'S', 'R', 'Q'], 'E6')]
maxn = int(sys.argv[1]); secs = int(sys.argv[2])
for Xs, Y in jobs:
    t = time.time(); n, st = mace_search(Xs, Y, range(2, maxn + 1), secs, wd)
    print(f"{' + '.join(Xs)} => {Y}: countermodel of order {n} ({st}) [{time.time()-t:.0f}s]", flush=True)
