"""Given a triangle configuration a1,a2,a3,b1,b2,b3 (a1|><|b2, a2|><|b3, a3|><|b1),
define the derived projections
    p_i = theta_{b_{i-1}}(a_i)   (below b_{i-1}),    q_i = theta_{a_i}(b_{i-1})  (below a_i)
i.e. p1 = b3 a1 b3, q1 = a1 b3 a1, p2 = b1 a2 b1, q2 = a2 b1 a2, p3 = b2 a3 b2, q3 = a3 b2 a3.
Conjecture (suggested by a 17-element Mace4 model): (p1,p3,p2 | q3,q2,q1) satisfies the
hexagon hypotheses with w' = z and z' = w.  In terms of x*y = y x y:
   p_i * p_j = z (all i != j),  q_i * q_j = w,
   p_i, q_{i+2} commute  [pairs (p1,q3),(p3,q2),(p2,q1)],
   matched: p_i |><| q_i, p1|><|q2, p3|><|q1, p2|><|q3.
Test this in every model available: the Mace4 model, P_n (n<=4) and quotients."""
import sys, re, itertools, time
from termeval import make_eval
from digraph import clause, parse_clause, search
from mace4parse import parse_models

def derived_equations():
    # names for evaluation: constants a1..a3,b1..b3; derived via *:
    # p1 = a1 * b3 (= b3 a1 b3), q1 = b3 * a1 (= a1 b3 a1), etc.
    d = {"p1": "(a1 * b3)", "q1": "(b3 * a1)", "p2": "(a2 * b1)", "q2": "(b1 * a2)",
         "p3": "(a3 * b2)", "q3": "(b2 * a3)"}
    P = [d["p1"], d["p3"], d["p2"]]; Q = [d["q3"], d["q2"], d["q1"]]
    eqs = []
    for i in range(3):
        for j in range(3):
            if i != j:
                eqs.append((f"{P[i]} * {P[j]}", "(b1 * b2)"))       # = z
                eqs.append((f"{Q[i]} * {Q[j]}", "(a1 * a2)"))       # = w
                eqs.append((f"{Q[j]} * {P[i]}", P[i]))              # p_i q_j p_i = p_i
                eqs.append((f"{P[i]} * {Q[j]}", Q[j]))              # q_j p_i q_j = q_j
        eqs.append((f"{P[i]} * {Q[i]}", f"{Q[i]} * {P[i]}"))         # commute
    return eqs

TRI = parse_clause(clause(3, [(1, 2), (2, 3), (3, 1)]))
TRI_HYPS = [(l, r) for l, r, neg in TRI if neg]

def test_model(N, op, label, limit=None):
    """for every triangle configuration (x1..x3,y1..y3) in the model, test the derived equations."""
    ev = make_eval(op)
    eqs = derived_equations()
    vars_ = ["x1", "x2", "x3", "y1", "y2", "y3"]
    stage = [[] for _ in vars_]
    for l, r in TRI_HYPS:
        vs = set(re.findall(r"[xy]\d", l + " " + r)); stage[max(vars_.index(v) for v in vs)].append((l, r))
    cnt = [0, 0]; bad = []
    t = time.time()
    def rec(k, env):
        if limit and time.time() - t > limit: raise TimeoutError
        if k == 6:
            cnt[0] += 1
            e2 = {"a1": env["x1"], "a2": env["x2"], "a3": env["x3"], "b1": env["y1"], "b2": env["y2"], "b3": env["y3"]}
            fails = [(l, r) for l, r in eqs if ev(l, e2) != ev(r, e2)]
            if fails:
                cnt[1] += 1
                if len(bad) < 3: bad.append((dict(env), fails[:3]))
            return
        for p in range(N):
            env[vars_[k]] = p
            if all(ev(l, env) == ev(r, env) for l, r in stage[k]): rec(k + 1, env)
        del env[vars_[k]]
    try:
        rec(0, {})
        print(f"{label}: {cnt[0]} triangle configurations, {cnt[1]} violate the derived-hexagon equations")
    except TimeoutError:
        print(f"{label}: timeout after {cnt[0]} configurations, {cnt[1]} violations")
    for env, fails in bad:
        print("   e.g.", env, fails)

if __name__ == "__main__":
    # 1. the Mace4 model
    for Nm, T, consts in parse_models(open("mace_tri17.out").read()):
        test_model(Nm, lambda x, y, T=T: T[x][y], f"Mace4 model of size {Nm}")
    # 2. P_n
    from pmon import Pn, projections
    for n in (2, 3, 4):
        P = Pn(n); projs = projections(n); idx = {p: i for i, p in enumerate(projs)}
        Tn = [[idx[P.prod(y, x, y)] for y in projs] for x in projs]
        test_model(len(projs), lambda x, y, Tn=Tn: Tn[x][y], f"P_{n} ({len(projs)} projections)", limit=2000)
