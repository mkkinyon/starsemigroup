"""(1) violated-condition sets of the witnesses and of the census; (2) Mace4 pairwise 'Q1 + X => Y ?'."""
import sys, os, json, glob, pickle, time
sys.path.insert(0, '/home/claude/pa8w'); sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed')
from indep import EVAL, NAMES, violated_set, mace_search, CLAUSE, NEG
from pa_sat import M172
from fourth import table as P7table
from collections import Counter
mode = sys.argv[1]
if mode == "witnesses":
    W = [('P (order 6)', M172), ('P7', P7table())]
    P9names = 'a b c d m n k w z'.split()
    rows = '''a m a m m m m w w
m b b b m m m w w
c c c z n n z z z
k d z d k z k z z
m m m m m m m w w
n n n z n n z z z
k k z k k z k z z
w w w w w w w w w
z z z z z z z z z'''.split('\n')
    thP9 = {p: dict(zip(P9names, r.split())) for p, r in zip(P9names, rows)}
    W.append(('P9', [[P9names.index(thP9[q][p]) for q in P9names] for p in P9names]))
    os.chdir('/mnt/user-data/outputs/starsemigroup/embed')
    Tq, sq, A2 = pickle.load(open('hex_smallest.pkl', 'rb'))
    from layered import proj_algebra
    P, A = proj_algebra(list(range(len(Tq))), Tq, sq); W.append(('P(Q0)', A))
    recs = [json.loads(l) for l in open('/home/claude/pa8w/post8.log')]
    for k, A in enumerate([r["A"] for r in recs if r["embeds"] is None]): W.append((f'P8^{k+1}', A))
    for k, A in enumerate(json.load(open('/home/claude/pa8w/cand9.json'))): W.append((f'cand9-{k}', A))
    for name, A in W:
        print(f"{name:12s} order {len(A)}: violates {violated_set(A)}", flush=True)
elif mode == "census":
    # violated sets over the census (orders 2..9); only the algebras violating something new are interesting
    out = Counter(); examples = {}
    t0 = time.time()
    for k in range(2, 10):
        for A in json.load(open(f'/home/claude/pa8w/ord{k}.json')):
            v = tuple(n for n in NAMES if n not in ('Q1', 'S', 'R', 'Tri') and EVAL[n](A) is not None)
            out[(k, v)] += 1
            if v and (k, v) not in examples: examples[(k, v)] = A
        print("order", k, "done", f"({time.time()-t0:.0f}s)", flush=True)
    for key in sorted(out): print(key, out[key])
    json.dump({str(k): v for k, v in examples.items()}, open('/home/claude/pa8w/indep_census_examples.json', 'w'))
elif mode == "mace":
    Xs = sys.argv[2].split(',') if len(sys.argv) > 2 else NAMES
    Ys = sys.argv[3].split(',') if len(sys.argv) > 3 else list(NEG)
    maxn = int(sys.argv[4]) if len(sys.argv) > 4 else 8; secs = int(sys.argv[5]) if len(sys.argv) > 5 else 120
    wd = '/home/claude/pa8w/m4indep'; os.makedirs(wd, exist_ok=True)
    for X in Xs:
        for Y in Ys:
            if X == Y or X == 'Tri': continue
            t = time.time(); n, st = mace_search(['Q1', X] if X != 'Q1' else ['Q1'], Y, range(2, maxn + 1), secs, wd)
            print(f"Q1 + {X} => {Y}: countermodel of order {n} ({st}) [{time.time()-t:.0f}s]", flush=True)
