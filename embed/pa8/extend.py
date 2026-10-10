"""Census of projection algebras with (Q1), (S), (R) by one-point extensions.

Every finite projection algebra has a maximal element e (natural order), and A \\ {e} is then a subalgebra
(p*q = theta_q(p) = e forces e <= q, i.e. q = e).  Since (Q1), (S), (R) are universal, the algebras of order n+1
satisfying them are exactly the extensions of the algebras of order n satisfying them by a new maximal element.
For each base algebra B (table B[x][y] = x*y = theta_y(x)) Mace4 is given the base table as ground facts and finds
all values of theta_e(q), theta_q(e) (q in B) with e = n maximal; results are reduced by canonical forms.

Usage: python3 extend.py n            # reads ord<n>.json (list of tables), writes ord<n+1>.json
       python3 extend.py 1 7          # chain from ord1 = the one-element algebra up to order 7 (validation)
       python3 extend.py 7 8 P K      # only the bases i = P mod K (parallel runs, checkpoint ext7_P.ckpt)
       python3 extend.py 7 8 -1 K     # merge the K finished parts into ord8.json"""
import sys, os, json, subprocess, time, pickle
HERE = os.path.dirname(os.path.abspath(__file__)); EMBED = os.environ.get("EMBED_DIR", os.path.dirname(HERE))
sys.path.insert(0, EMBED)
from mace4parse import parse_models
from layered_search import canon

CLAUSES = """op(400, infix, "*").
formulas(assumptions).
x * x = x.
(y * x) * x = y * x.
(x * y) * x = y * x.
((z * x) * y) * x = z * (y * x).
(((z * x) * y) * x) * y = (z * x) * y.
% Q1
z * x != z | z * y != z | x * y = y * x.
% (S)
v * x != x | x * v != v | v * y != y | y * v != v | w * y != y | y * w != w | w * v != v * w | (w * v) * x != (w * v) * y | w * x = x.
v * x != x | x * v != v | v * y != y | y * v != v | w * y != y | y * w != w | w * v != v * w | (w * v) * x != (w * v) * y | x * w = w.
% (R)
z1 * x1 != x1 | x1 * z1 != z1 | z1 * y1 != y1 | y1 * z1 != z1 | x1 * x != x * x1 | z1 * x != x * z1 | y1 * x != z1 * x | y1 * x1 = x1.
z1 * x1 != x1 | x1 * z1 != z1 | z1 * y1 != y1 | y1 * z1 != z1 | x1 * x != x * x1 | z1 * x != x * z1 | y1 * x != z1 * x | x1 * y1 = y1.
"""

def extensions(B, workdir, tag):
    n = len(B); e = n
    inp = f"assign(domain_size, {n+1}).\nassign(max_models, -1).\nassign(max_seconds, -1).\n" + CLAUSES
    inp += f"% e = {e} is maximal\n{e} * x != {e} | x = {e}.\n"
    for x in range(n):
        for y in range(n): inp += f"{x} * {y} = {B[x][y]}.\n"
    inp += "end_of_list.\n"
    fin = os.path.join(workdir, f"ext_{tag}.in"); open(fin, "w").write(inp)
    env = dict(os.environ, PATH="/home/claude/bin:" + os.environ.get("PATH", ""))
    p = subprocess.run(f"mace4 -b 1000 -f {fin} 2>/dev/null | interpformat standard | isofilter 2>/dev/null",
                       shell=True, capture_output=True, text=True, env=env)
    os.remove(fin)
    return [T for N, T, c in parse_models(p.stdout)]

def step(n, workdir, part=0, nparts=1):
    """process the bases i = part, part+nparts, ... (checkpoint ext<n>_<part>.ckpt); when nparts == 1 or part == -1
    (merge only) write ord<n+1>.json from all parts"""
    bases = json.load(open(os.path.join(HERE, f"ord{n}.json")))
    if part >= 0:
        ck = os.path.join(HERE, f"ext{n}_{part}.ckpt")          # checkpoint (resumable after a restart)
        out, start, nlab = pickle.load(open(ck, "rb")) if os.path.exists(ck) else ({}, part, 0)
        t0 = time.time(); todo = list(range(start, len(bases), nparts))
        for j, i in enumerate(todo):
            for T in extensions(bases[i], workdir, f"{n}_{i}"):
                nlab += 1; key = canon(T)
                if key not in out: out[key] = T
            if (j + 1) % 25 == 0 or j + 1 == len(todo):
                pickle.dump((out, i + nparts, nlab), open(ck + ".tmp", "wb")); os.replace(ck + ".tmp", ck)
                print(f"  order {n} part {part}: base {i+1}/{len(bases)}, {nlab} extensions, {len(out)} classes of order {n+1} ({time.time()-t0:.0f}s)", flush=True)
        if nparts > 1: return
    out = {}; nlab = 0
    for p in range(max(nparts, 1)):
        ck = os.path.join(HERE, f"ext{n}_{p}.ckpt"); o, s, nl = pickle.load(open(ck, "rb"))
        assert s >= len(bases), f"part {p} incomplete ({s}/{len(bases)})"
        out.update(o); nlab += nl
    res = [[list(r) for r in k] for k in out]
    json.dump(res, open(os.path.join(HERE, f"ord{n+1}.json"), "w"))
    print(f"order {n+1}: {len(res)} algebras with Q1, (S), (R) up to isomorphism ({nlab} labelled extensions)", flush=True)
    return res

if __name__ == "__main__":
    a = int(sys.argv[1]); b = int(sys.argv[2]) if len(sys.argv) > 2 else a + 1
    if not os.path.exists(os.path.join(HERE, "ord1.json")): json.dump([[[0]]], open(os.path.join(HERE, "ord1.json"), "w"))
    workdir = os.environ.get("EXT_TMP", HERE)
    part = int(sys.argv[3]) if len(sys.argv) > 3 else 0; nparts = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    for n in range(a, b): step(n, workdir, part, nparts)
