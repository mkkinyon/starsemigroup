import sys, time, random
from qi2 import test_qi
names = {0:'w',1:'a',2:'b',3:'z',4:'d',5:'c'}
T = [[0,0,0,3,3,3],[0,1,0,3,3,5],[0,0,2,3,4,5],[0,0,0,3,3,3],[0,0,2,3,4,3],[0,1,2,3,3,5]]
hyps = sorted({(names[y]+names[x]+names[y], names[T[x][y]]) for x in range(6) for y in range(6) if x != y})
n = int(sys.argv[1]); seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
random.seed(seed); order = list(hyps); random.shuffle(order)
cur = list(hyps)
for h in order:
    trial = [g for g in cur if g != h]
    r = test_qi(n, "abcdwz", trial, ("w","z"), limit=600)
    if r == []: cur = trial
print(f"P_{n}, seed {seed}: minimal set ({len(cur)}):", cur, flush=True)
