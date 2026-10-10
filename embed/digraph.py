"""Digraph conditions.  For a digraph E on [k] (no loops) the hypotheses are:
  a_i a_j = a_j a_i = w, b_i b_j = b_j b_i = z (all i != j), a_i b_i = b_i a_i,
  a_i |><| b_j for (i,j) in E;  conclusion w = z.
Build the positive-form Prover9 clause (w, z eliminated) and search P_n for
counterexamples."""
import sys, re, time, itertools, pickle
from pmon import Pn, projections
from termeval import make_eval

def pair_orientation(k):
    """unordered pairs of [k], oriented so that every index occurs in the second slot:
    the cycle (1,2),(2,3),...,(k,1) followed by the remaining pairs (i,j), i<j."""
    cyc = [(i, i % k + 1) for i in range(1, k + 1)]
    rest = [(i, j) for i in range(1, k + 1) for j in range(i + 1, k + 1) if (i, j) not in cyc and (j, i) not in cyc]
    return cyc + rest

def clause(k, E):
    """positive-form clause of the matching-pattern condition for digraph E on [k];
    w = x1*x2 and z = y1*y2 eliminated."""
    lits = []
    pairs = pair_orientation(k)
    for (i, j) in pairs:
        if (i, j) != (1, 2):
            lits.append(f"x1 * x2 != x{i} * x{j}")
    for (i, j) in pairs:
        if (i, j) != (1, 2):
            lits.append(f"y1 * y2 != y{i} * y{j}")
    for i in range(1, k + 1):
        lits.append(f"x{i} * y{i} != y{i} * x{i}")
    for (i, j) in E:
        lits.append(f"y{j} * x{i} != x{i}"); lits.append(f"x{i} * y{j} != y{j}")
    lits.append("x1 * x2 = y1 * y2")
    return " |\n".join(lits) + "."

def parse_clause(text):
    lits = []
    for lit in text.strip().rstrip(".").split("|"):
        lit = lit.strip()
        if "!=" in lit: l, r = lit.split("!="); lits.append((l.strip(), r.strip(), True))
        else: l, r = lit.split("="); lits.append((l.strip(), r.strip(), False))
    return lits

def search(lits, dom, op, distinct=True, limit=None):
    ev = make_eval(op)
    vars_ = sorted({v for l, r, _ in lits for v in re.findall(r"[xy]\d", l + " " + r)})
    hyps = [(l, r) for l, r, neg in lits if neg]; concl = [(l, r) for l, r, neg in lits if not neg]
    stage = [[] for _ in vars_]
    for l, r in hyps:
        vs = set(re.findall(r"[xy]\d", l + " " + r)); stage[max(vars_.index(v) for v in vs)].append((l, r))
    out = []; t = time.time()
    def rec(k, env):
        if out: return
        if limit and time.time() - t > limit: raise TimeoutError
        if k == len(vars_):
            if all(ev(l, env) != ev(r, env) for l, r in concl): out.append(dict(env))
            return
        for p in dom:
            if distinct and p in env.values(): continue
            env[vars_[k]] = p
            if all(ev(l, env) == ev(r, env) for l, r in stage[k]): rec(k + 1, env)
        del env[vars_[k]]
    try:
        rec(0, {})
    except TimeoutError:
        return "timeout"
    return out

CONDS = {
    "hexagon (k=3, all pairs)": (3, [(i, j) for i in range(1, 4) for j in range(1, 4) if i != j]),
    "directed triangle (k=3)": (3, [(1, 2), (2, 3), (3, 1)]),
    "cyclic octagon (k=4, i->i+-1)": (4, [(i, j) for i in range(1, 5) for j in range(1, 5) if (i - j) % 4 in (1, 3)]),
    "directed 4-cycle (k=4)": (4, [(1, 2), (2, 3), (3, 4), (4, 1)]),
    "double 2-cycle (k=4)": (4, [(1, 2), (2, 1), (3, 4), (4, 3)]),
    "k=2 square (should FAIL)": (2, [(1, 2), (2, 1)]),
    "k=3, star at 1 (should FAIL?)": (3, [(1, 2), (2, 1), (1, 3), (3, 1)]),
}

if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    for name, (k, E) in CONDS.items():
        cl = clause(k, E)
        print(f"== {name}: {len(parse_clause(cl))} literals")
    for n in range(2, nmax + 1):
        P = Pn(n); projs = projections(n)
        op = lambda x, y, P=P: P.prod(y, x, y)
        for name, (k, E) in CONDS.items():
            t = time.time()
            res = search(parse_clause(clause(k, E)), projs, op, distinct=False, limit=3000)
            print(f"P_{n} ({len(projs)} proj.)  {name}: counterexamples = {res if res == 'timeout' else len(res)}  ({time.time()-t:.0f}s)", flush=True)
