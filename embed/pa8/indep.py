"""Independence of the obstruction quasi-identities: Q1, Tri, S, R, R', V, P1, P2, Q, E6, E1.
(1) Python evaluators (violating instance or None) on given tables; (2) Mace4 inputs for 'Q1 + X => Y ?'.
Prover9 notation: x*y = theta_y(x) = y x y; variables start with u..z, constants with a..k."""
import sys, os, json, itertools, subprocess, time
EMBED = '/mnt/user-data/outputs/starsemigroup/embed'; sys.path.insert(0, EMBED); sys.path.insert(0, '/home/claude/pa8w')
from newconds import Rprime, V, P1, P2, Q, E6, E1
from graphsg import q1
from graphsg_survey import s_violations
from fourth import R_violations
from pa7_post import triangle_ok

def Q1v(A): return None if q1(A) else ('Q1',)
def Triv(A): return None if triangle_ok(A) else ('Tri',)
def Sv(A): return ('S',) if s_violations(A) else None
def Rv(A):
    r = R_violations(A); return ('R',) + tuple(r[0]) if r else None
EVAL = {'Q1': Q1v, 'Tri': Triv, 'S': Sv, 'R': Rv, "R'": Rprime, 'V': V, 'P1': P1, 'P2': P2, 'Q': Q, 'E6': E6, 'E1': E1}
NAMES = list(EVAL)

def violated_set(A):
    return [n for n, f in EVAL.items() if f(A) is not None]

AX = """x * x = x.
(y * x) * x = y * x.
(x * y) * x = y * x.
((z * x) * y) * x = z * (y * x).
(((z * x) * y) * x) * y = (z * x) * y.
"""
CLAUSE = {
 'Q1': ["z * x != z | z * y != z | x * y = y * x."],
 'S': ["v * x != x | x * v != v | v * y != y | y * v != v | w * y != y | y * w != w | w * v != v * w | (w * v) * x != (w * v) * y | w * x = x.",
       "v * x != x | x * v != v | v * y != y | y * v != v | w * y != y | y * w != w | w * v != v * w | (w * v) * x != (w * v) * y | x * w = w."],
 'R': ["z1 * x1 != x1 | x1 * z1 != z1 | z1 * y1 != y1 | y1 * z1 != z1 | x1 * x != x * x1 | z1 * x != x * z1 | y1 * x != z1 * x | y1 * x1 = x1.",
       "z1 * x1 != x1 | x1 * z1 != z1 | z1 * y1 != y1 | y1 * z1 != z1 | x1 * x != x * x1 | z1 * x != x * z1 | y1 * x != z1 * x | x1 * y1 = y1."],
 "R'": ["z1 * x1 != x1 | x1 * z1 != z1 | z1 * y1 != y1 | y1 * z1 != z1 | z1 * x != x * z1 | x1 * x != z1 * x | x1 * y != y * x1 | y1 * x != y1 * y | y1 * x1 = x1.",
        "z1 * x1 != x1 | x1 * z1 != z1 | z1 * y1 != y1 | y1 * z1 != z1 | z1 * x != x * z1 | x1 * x != z1 * x | x1 * y != y * x1 | y1 * x != y1 * y | x1 * y1 = y1."],
 'V': ["z1 * y1 != y1 | (w * x1) * y1 != w * x1 | (w * z1) * x1 != w * z1 | (w * x1) * (w * y1) = w * x1."],
 'P1': ["v1 * v0 != v0 | v0 * v1 != v1 | v2 * v1 != v1 | v1 * v2 != v2 | v3 * v2 != v2 | v2 * v3 != v3 | v0 * x != x * v0 | v1 * x != x * v1 | x * v0 != x * v2 | v1 * x != v3 * x | v3 * v0 = v0.",
        "v1 * v0 != v0 | v0 * v1 != v1 | v2 * v1 != v1 | v1 * v2 != v2 | v3 * v2 != v2 | v2 * v3 != v3 | v0 * x != x * v0 | v1 * x != x * v1 | x * v0 != x * v2 | v1 * x != v3 * x | v0 * v3 = v3."],
 'P2': ["v1 * v0 != v0 | v0 * v1 != v1 | v2 * v1 != v1 | v1 * v2 != v2 | v3 * v2 != v2 | v2 * v3 != v3 | v0 * x != x * v0 | v2 * x != x * v2 | v1 * x != v2 * x | x * v1 != x * v3 | v3 * v0 = v0.",
        "v1 * v0 != v0 | v0 * v1 != v1 | v2 * v1 != v1 | v1 * v2 != v2 | v3 * v2 != v2 | v2 * v3 != v3 | v0 * x != x * v0 | v2 * x != x * v2 | v1 * x != v2 * x | x * v1 != x * v3 | v0 * v3 = v3."],
 'Q': ["v1 * v0 != v0 | v0 * v1 != v1 | v2 * v1 != v1 | v1 * v2 != v2 | v3 * v2 != v2 | v2 * v3 != v3 | v0 * x != x * v0 | x * v1 != x * v3 | v0 * y != y * v0 | v2 * y != y * v2 | v1 * y != v2 * y | v3 * v0 = v0.",
       "v1 * v0 != v0 | v0 * v1 != v1 | v2 * v1 != v1 | v1 * v2 != v2 | v3 * v2 != v2 | v2 * v3 != v3 | v0 * x != x * v0 | x * v1 != x * v3 | v0 * y != y * v0 | v2 * y != y * v2 | v1 * y != v2 * y | v0 * v3 = v3."],
 'E6': ["y * w != w | z * x != x | w * x != x | u * z != u | u * w != u | z * y != u * x | u * x = x."],
 'E1': ["z * y != z | y * x != z | y * w != w | u * v != z | u * x != x | u * y != y | v1 * v != v1 | v1 * w != v1 | w * x != x | y * x = x."],
}
# ground negations: hypotheses as facts on constants, conclusion negated
NEG = {
 'Q1': ["c * a = c.", "c * b = c.", "a * b != b * a."],
 'Tri': ["a1 * a2 = cw.", "a2 * a3 = cw.", "a3 * a1 = cw.", "b1 * b2 = cz.", "b2 * b3 = cz.", "b3 * b1 = cz.",
         "a1 * b1 = b1 * a1.", "a2 * b2 = b2 * a2.", "a3 * b3 = b3 * a3.",
         "b2 * a1 = a1.", "a1 * b2 = b2.", "b3 * a2 = a2.", "a2 * b3 = b3.", "b1 * a3 = a3.", "a3 * b1 = b1.", "cw != cz."],
 'S': ["c * a = a.", "a * c = c.", "c * b = b.", "b * c = c.", "d * b = b.", "b * d = d.", "d * c = c * d.", "(d * c) * a = (d * c) * b.", "d * a != a | a * d != d."],
 'R': ["c * a = a.", "a * c = c.", "c * b = b.", "b * c = c.", "a * e = e * a.", "c * e = e * c.", "b * e = c * e.", "b * a != a | a * b != b."],
 "R'": ["c * a = a.", "a * c = c.", "c * b = b.", "b * c = c.", "c * e = e * c.", "a * e = c * e.", "a * f = f * a.", "b * e = b * f.", "b * a != a | a * b != b."],
 'V': ["c * b = b.", "(d * a) * b = d * a.", "(d * c) * a = d * c.", "(d * a) * (d * b) != d * a."],
 'P1': ["a1 * a0 = a0.", "a0 * a1 = a1.", "a2 * a1 = a1.", "a1 * a2 = a2.", "a3 * a2 = a2.", "a2 * a3 = a3.", "a0 * e = e * a0.", "a1 * e = e * a1.", "e * a0 = e * a2.", "a1 * e = a3 * e.", "a3 * a0 != a0 | a0 * a3 != a3."],
 'P2': ["a1 * a0 = a0.", "a0 * a1 = a1.", "a2 * a1 = a1.", "a1 * a2 = a2.", "a3 * a2 = a2.", "a2 * a3 = a3.", "a0 * e = e * a0.", "a2 * e = e * a2.", "a1 * e = a2 * e.", "e * a1 = e * a3.", "a3 * a0 != a0 | a0 * a3 != a3."],
 'Q': ["a1 * a0 = a0.", "a0 * a1 = a1.", "a2 * a1 = a1.", "a1 * a2 = a2.", "a3 * a2 = a2.", "a2 * a3 = a3.", "a0 * e = e * a0.", "e * a1 = e * a3.", "a0 * f = f * a0.", "a2 * f = f * a2.", "a1 * f = a2 * f.", "a3 * a0 != a0 | a0 * a3 != a3."],
 'E6': ["b * d = d.", "c * a = a.", "d * a = a.", "k * c = k.", "k * d = k.", "c * b = k * a.", "k * a != a."],
 'E1': ["g * b = g.", "b * a = g.", "b * d = d.", "c * e = g.", "c * a = a.", "c * b = b.", "f * e = f.", "f * d = f.", "d * a = a.", "b * a != a."],
}

def mace_input(Xs, Y, n, secs):
    s = f"assign(domain_size, {n}).\nassign(max_models, 1).\nassign(max_seconds, {secs}).\nassign(max_megs, 3000).\nop(400, infix, \"*\").\nformulas(assumptions).\n" + AX
    for X in Xs:
        for cl in CLAUSE[X]: s += cl + "\n"
    for g in NEG[Y]: s += g + "\n"
    return s + "end_of_list.\n"

def mace_search(Xs, Y, orders, secs, workdir):
    """min order with a countermodel for (Q1 +) Xs => Y, or None; returns (order|None, status)"""
    env = dict(os.environ, PATH="/home/claude/bin:" + os.environ.get("PATH", ""))
    for n in orders:
        f = os.path.join(workdir, f"m_{'_'.join(x.replace(chr(39), 'p') for x in Xs)}_{Y.replace(chr(39), 'p')}_{n}.in")
        open(f, "w").write(mace_input(Xs, Y, n, secs))
        p = subprocess.run(["mace4", "-f", f], capture_output=True, text=True, env=env)
        out = p.stdout
        if "interpretation(" in out: return n, "model"
        if "exit (max_seconds)" in out or "exit (max_sec" in out: return None, f"timeout at {n}"
        if "exit (exhausted)" not in out: return None, f"unexpected exit at {n}: " + out[-200:].replace(chr(10), ' ')
    return None, f"none <= {orders[-1]}"

if __name__ == "__main__":
    pass
