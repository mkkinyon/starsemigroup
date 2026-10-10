import sys, time
from hexmin import *
n = int(sys.argv[1])
groups = {}
for w in ws_all: groups.setdefault(val_all[w], []).append(w)
classes = list(groups.values())
# greedy: try to remove nontrivial classes (largest first), keep removal if still 'none'
current = classes[:]
order_idx = sorted([i for i, c in enumerate(current) if len(c) > 1], key=lambda i: -len(current[i]))
removed = []
for i in order_idx:
    cl = current[i]
    trial = [c for j, c in enumerate(current) if j != i and c is not None] + [[w] for w in cl]
    trial_marked = [c if (j != i) else None for j, c in enumerate(current)]
    s = search_with(n, [c for c in trial if c])
    if not s:
        current[i] = None; removed.append(cl)
        # singletons for its words
        for w in cl: current.append([w])
        print(f"removed [{wname(cl[0])}...] (now {sum(1 for c in current if c and len(c)>1)} nontrivial classes)", flush=True)
    else:
        print(f"keep    [{wname(cl[0])} = ...]", flush=True)
final = [c for c in current if c and len(c) > 1]
print("\nMINIMAL RELATION SET (P_%d):" % n)
for cl in final:
    print("  ", " = ".join(wname(w) for w in sorted(cl, key=len)))
import pickle; pickle.dump(final, open(f"hexmin_{n}.pkl", "wb"))
