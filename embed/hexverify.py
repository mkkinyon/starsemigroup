import sys, time, pickle
from hexmin4 import sat, names, wname
final = pickle.load(open("hexmin4_4_03.pkl", "rb"))
for n in range(3, int(sys.argv[1]) + 1):
    for pair in [(0, 3)]:
        t = time.time(); s = sat(n, final, pair)
        print(f"n={n}: minimal set & {names[pair[0]]}!={names[pair[1]]}: {'SAT' if s else 'UNSAT'} ({time.time()-t:.0f}s)", flush=True)
        if s: print("   ", {names[i]: s[0][i] for i in range(6)})
