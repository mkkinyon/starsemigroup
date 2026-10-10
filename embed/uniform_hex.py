"""Uniform candidate for hexagon => triangle.
Triangle: a_i |><| b_{i+1}; free pairs (a_i, b_{i-1}).  (indices mod 3, 1..3)
  q_i = theta_{a_i}(b_{i-1})  (= b_{i-1} * a_i),   p_i = theta_{b_{i-1}}(a_i)  (= a_i * b_{i-1})
  t_i = theta_{a_{i+1}}(p_i)  (= p_i * a_{i+1}),    s_i = theta_{b_{i+1}}(q_i)  (= q_i * b_{i+1})
Candidate hexagon:  A_i = theta_{q_i}(t_{i-1}) (= t_{i-1} * q_i),
                    B_j = theta_{p_{j+1}}(s_{j-1}) (= s_{j-1} * p_{j+1}),
with A_i, B_i commuting and A_i |><| B_j (i != j), products w and z.
Test over all triangle configurations with w != z in the Mace4 models."""
import re, sys
from termeval import make_eval
from mace4parse import parse_models
from digraph import clause, parse_clause

TRI = parse_clause(clause(3, [(1, 2), (2, 3), (3, 1)]))
TRI_HYPS = [(l, r) for l, r, neg in TRI if neg]

def nxt(i): return i % 3 + 1
def prv(i): return (i - 2) % 3 + 1

def candidate_terms():
    q = {i: f"(b{prv(i)} * a{i})" for i in (1, 2, 3)}
    p = {i: f"(a{i} * b{prv(i)})" for i in (1, 2, 3)}
    t = {i: f"({p[i]} * a{nxt(i)})" for i in (1, 2, 3)}
    s = {i: f"({q[i]} * b{nxt(i)})" for i in (1, 2, 3)}
    A = {i: f"({t[prv(i)]} * {q[i]})" for i in (1, 2, 3)}
    B = {j: f"({s[prv(j)]} * {p[nxt(j)]})" for j in (1, 2, 3)}
    return A, B

def hex_equations(A, B):
    eqs = []
    for i in (1, 2, 3):
        for j in (1, 2, 3):
            if i != j:
                eqs.append((f"{A[i]} * {A[j]}", "(a1 * a2)"))
                eqs.append((f"{B[i]} * {B[j]}", "(b1 * b2)"))
                eqs.append((f"{B[j]} * {A[i]}", A[i]))
                eqs.append((f"{A[i]} * {B[j]}", B[j]))
        eqs.append((f"{A[i]} * {B[i]}", f"{B[i]} * {A[i]}"))
    return eqs

def configurations(N, ev, only_wz=True):
    vars_ = ["x1", "x2", "x3", "y1", "y2", "y3"]
    stage = [[] for _ in vars_]
    for l, r in TRI_HYPS:
        vs = set(re.findall(r"[xy]\d", l + " " + r)); stage[max(vars_.index(v) for v in vs)].append((l, r))
    out = []
    def rec(k, env):
        if k == 6:
            e = {"a1": env["x1"], "a2": env["x2"], "a3": env["x3"], "b1": env["y1"], "b2": env["y2"], "b3": env["y3"]}
            if not only_wz or ev("a1 * a2", e) != ev("b1 * b2", e): out.append(e)
            return
        for pp in range(N):
            env[vars_[k]] = pp
            if all(ev(l, env) == ev(r, env) for l, r in stage[k]): rec(k + 1, env)
        del env[vars_[k]]
    rec(0, {})
    return out

if __name__ == "__main__":
    A, B = candidate_terms()
    eqs = hex_equations(A, B)
    for fn in sys.argv[1:] or ["mace_tri17.out", "mace_tri15.out"]:
        for N, T, c in parse_models(open(fn).read()):
            ev = make_eval(lambda x, y: T[x][y])
            confs = configurations(N, ev)
            bad = 0; ex = None
            for e in confs:
                f = [(l, r) for l, r in eqs if ev(l, e) != ev(r, e)]
                if f:
                    bad += 1
                    if ex is None: ex = (e, f[:3])
            print(f"{fn}: {len(confs)} triangle configurations with w != z; candidate hexagon fails in {bad}")
            if ex: print("   e.g.", ex)
