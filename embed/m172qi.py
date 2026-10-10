import sys, time, itertools
from qi2 import test_qi
# letters: a=a1, b=a2, c=b1, d=b2, w, z ;  hypotheses  y x y = T[x][y]
names = {0:'w',1:'a',2:'b',3:'z',4:'d',5:'c'}
T = [[0,0,0,3,3,3],[0,1,0,3,3,5],[0,0,2,3,4,5],[0,0,0,3,3,3],[0,0,2,3,4,3],[0,1,2,3,3,5]]
hyps = []
for x in range(6):
    for y in range(6):
        if x == y: continue
        hyps.append((names[y]+names[x]+names[y], names[T[x][y]]))
hyps = sorted(set(hyps))
print(len(hyps), "hypotheses")
n = int(sys.argv[1])
t = time.time(); s = test_qi(n, "abcdwz", hyps, ("w","z"))
print(f"P_{n}: full hypotheses: {'NOT forced' if s else 'w = z FORCED'} ({time.time()-t:.0f}s)", flush=True)
if s: print(s[0])
# greedy minimisation: drop hypotheses one at a time while w=z stays forced
if not s and len(sys.argv) > 2:
    cur = list(hyps)
    for h in list(cur):
        trial = [g for g in cur if g != h]
        if not test_qi(n, "abcdwz", trial, ("w","z")):
            cur = trial
    print("minimal set:", cur)
