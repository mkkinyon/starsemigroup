import sys, time, pickle
from collections import Counter
sys.argv = ["x", "6"]
src = open("octsub6.py").read()
src = src[:src.index("class Mul:")]
exec(src)
from pmon import rank
t = time.time(); cnt = 0; stats = Counter(); examples = []
for cand in candidates():
    cnt += 1
    g = [projs[i] for i in cand]
    A, B = g[:4], g[4:]
    pa = {rawmul(A[i], A[j], n) for i in range(4) for j in range(4) if i != j}
    pb = {rawmul(B[i], B[j], n) for i in range(4) for j in range(4) if i != j}
    key = (rank(A[0], n), len(pa), len(pb), tuple(sorted(rank(x, n) for x in pa)), tuple(sorted(rank(x, n) for x in pb)))
    stats[key] += 1
    if len(examples) < 3 or (len(pa) == 1 and len(pb) == 1 and len(examples) < 6):
        examples.append((key, cand))
    if cnt >= 200000: break
print(cnt, "candidates", f"({time.time()-t:.0f}s)")
for k, v in sorted(stats.items(), key=lambda kv: -kv[1])[:20]:
    print(v, "rank", k[0], "| #a-products", k[1], "ranks", k[3], "| #b-products", k[2], "ranks", k[4])
pickle.dump(examples, open("octdiag6.pkl", "wb"))
for k, c in examples: print(k, [projs[i] for i in c])
