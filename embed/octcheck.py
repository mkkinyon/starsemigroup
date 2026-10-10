"""Sanity checks for octagon.in.
1. The ground (negated) octagon block is the instance x_i -> a_i, y_i -> b_i of the
   positive-form octagon clause in the comment.
2. The positive-form hexagon clause fails in P_3/mu at the known assignment
   (so the translation is faithful), and holds throughout P(P_3/mu)? -- no: it fails there.
3. Backtracking search for counterexamples to the hexagon and octagon clauses in the
   projection algebras of P_2, P_3 (and P_4 for the octagon if time permits):
   assign variables in order, prune as soon as an assigned hypothesis fails.
"""
import re, sys, time, itertools, pickle
from pmon import Pn, projections, partition_monoid, mul, star as pstar, canon
from congr import quotient
from termeval import make_eval

src = open("octagon.in").read()

def parse_clause(text):
    """'l1 | l2 | ... | ln.' -> list of (lhs, rhs, negated)"""
    text = text.strip().rstrip(".")
    lits = []
    for lit in text.split("|"):
        lit = lit.strip()
        if "!=" in lit:
            l, r = lit.split("!="); lits.append((l.strip(), r.strip(), True))
        else:
            l, r = lit.split("="); lits.append((l.strip(), r.strip(), False))
    return lits

# positive-form clauses
body = src.split("formulas(assumptions).")[1].split("end_of_list.")[0]
body_nc = re.sub(r"%.*", "", body)
stmts = [s.strip() for s in body_nc.split(".") if s.strip()]
hex_clause = [s for s in stmts if "|" in s][0]
hexlits = parse_clause(hex_clause)
tail = src.split("end_of_list.")[1]
oct_text = " ".join(ln.lstrip("% ").strip() for ln in tail.splitlines() if ln.startswith("% ") and ("*" in ln))
octlits = parse_clause(oct_text)
print("hexagon clause:", len(hexlits), "literals; octagon clause:", len(octlits), "literals")

# 1. ground block vs positive clause
ground = [s for s in stmts if "|" not in s and re.search(r"[ab]\d", s)]
subst = lambda t: re.sub(r"x(\d)", r"a\1", re.sub(r"y(\d)", r"b\1", t))
def norm(l, r): return frozenset([l.replace(" ", ""), r.replace(" ", "")])
inst = set()
for l, r, neg in octlits:
    inst.add((norm(subst(l), subst(r)), neg))
grd = set()
for s in ground:
    if "!=" in s:
        l, r = s.split("!="); grd.add((norm(l, r), False))   # negated conclusion <-> positive literal
    else:
        l, r = s.split("="); grd.add((norm(l, r), True))
print("ground block == instance of positive clause:", inst == grd, len(grd))

# 2. hexagon clause on P_3/mu at the witness
n3 = 3
elems3 = partition_monoid(n3); idx3 = {e: i for i, e in enumerate(elems3)}
T3 = [[idx3[mul(p, q, n3)] for q in elems3] for p in elems3]
st3 = [idx3[pstar(p, n3)] for p in elems3]
congs = pickle.load(open("congs_P3.pkl", "rb"))
c103 = [c for c in congs if len(set(c)) == 103][0]
Tq, sq = quotient(T3, st3, c103)
classes = sorted(set(c103)); qidx = {cl: i for i, cl in enumerate(classes)}
q_of = lambda e: qidx[c103[idx3[e]]]
opQ = lambda x, y: Tq[Tq[y][x]][y]
def a(i):
    others = [j for j in range(3) if j != i]
    return canon([[i, 3 + i], others + [3 + j for j in others]])
def b(i):
    others = [j for j in range(3) if j != i]
    return canon([[j, 3 + j] for j in others] + [[i], [3 + i]])
env = {f"x{i+1}": q_of(a(i)) for i in range(3)}; env.update({f"y{i+1}": q_of(b(i)) for i in range(3)})
ev = make_eval(opQ)
def clause_value(lits, env, ev):
    return any((ev(l, env) != ev(r, env)) if neg else (ev(l, env) == ev(r, env)) for l, r, neg in lits)
print("hexagon clause at the witness in P_3/mu:", clause_value(hexlits, env, ev), "(expected False)")

# 3. counterexample search in P(P_n)
def search(lits, projs, op, limit_time=None):
    ev = make_eval(op)
    vars_ = []
    for l, r, _ in lits:
        for v in re.findall(r"[xy]\d", l + " " + r):
            if v not in vars_: vars_.append(v)
    vars_.sort()
    hyps = [(l, r) for l, r, neg in lits if neg]
    concl = [(l, r) for l, r, neg in lits if not neg]
    # which hypotheses become checkable after assigning the k-th variable
    stage = [[] for _ in vars_]
    for l, r in hyps:
        vs = set(re.findall(r"[xy]\d", l + " " + r))
        stage[max(vars_.index(v) for v in vs)].append((l, r))
    found = []
    t0 = time.time()
    def rec(k, env):
        if limit_time and time.time() - t0 > limit_time:
            raise TimeoutError
        if k == len(vars_):
            if all(ev(l, env) != ev(r, env) for l, r in concl):
                found.append(dict(env))
            return
        for p in projs:
            env[vars_[k]] = p
            if all(ev(l, env) == ev(r, env) for l, r in stage[k]):
                rec(k + 1, env)
            if found: return
        del env[vars_[k]]
    try:
        rec(0, {})
    except TimeoutError:
        return "timeout"
    return found

for n in (2, 3, 4):
    P = Pn(n); projs = projections(n)
    op = lambda x, y, P=P: P.prod(y, x, y)
    for name, lits in (("hexagon", hexlits), ("octagon", octlits)):
        t = time.time()
        res = search(lits, projs, op, limit_time=1500)
        print(f"P_{n} ({len(projs)} projections), {name}: counterexamples = {res if res == 'timeout' else len(res)}  ({time.time()-t:.0f}s)", flush=True)
