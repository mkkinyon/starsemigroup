"""Prover9/Mace4 tests of path-closing candidates: does axioms + Q1 (+ (S)) imply them?"""
import json, subprocess, sys, os
os.environ["PATH"] = "/home/claude/bin:" + os.environ["PATH"]
from pathclose import fmt
AX = """op(400, infix, "*").
formulas(assumptions).
x * x = x.
(y * x) * x = y * x.
(x * y) * x = y * x.
((z * x) * y) * x = z * (y * x).
(((z * x) * y) * x) * y = (z * x) * y.
z * x != z | z * y != z | x * y = y * x.
"""
S_CL = """v * x != x | x * v != v | v * y != y | y * v != v | w * y != y | y * w != w | w * v != v * w | (w * v) * x != (w * v) * y | w * x = x.
v * x != x | x * v != v | v * y != y | y * v != v | w * y != y | y * w != w | w * v != v * w | (w * v) * x != (w * v) * y | x * w = w.
"""
def atom_str(at):
    # constants a0..a3 and c (the auxiliary x is a variable letter in Prover9, so call it c);  p*q = theta_q(p)
    P = ['a0', 'a1', 'a2', 'a3', 'a4', 'a5']; k = at[0]
    if k == 'comm': return f"{P[at[1]]} * c = c * {P[at[1]]}."
    if k == 'xle': return f"c * {P[at[1]]} = c."          # theta_p(c) = c
    if k == 'lex': return f"{P[at[1]]} * c = {P[at[1]]}."  # theta_c(p) = p
    if k == 'sees': return f"{P[at[1]]} * c = {P[at[2]]} * c."   # theta_c(p)=theta_c(q)
    if k == 'seen': return f"c * {P[at[1]]} = c * {P[at[2]]}."   # theta_p(c)=theta_q(c)
    if k == 'xeq': return f"{P[at[2]]} * {P[at[1]]} = c."        # theta_p(q) = c  (q*p)
def run(combo, n, withS, mace_max=8):
    hyps = "".join(f"a{i} * a{i+1} = a{i+1}. a{i+1} * a{i} = a{i}.\n" for i in range(n))   # a_i ~ a_{i+1}: theta_{a_i}(a_{i+1}) = a_i ...
    # careful: p ~ q means theta_p(q) = p and theta_q(p) = q;  theta_p(q) = q * p.  So: a{i+1}*a{i} = a{i} and a{i}*a{i+1} = a{i+1}
    hyps = "".join(f"a{i+1} * a{i} = a{i}. a{i} * a{i+1} = a{i+1}.\n" for i in range(n))
    hyps += "".join(atom_str(at) + "\n" for at in combo)
    proved = True
    for goal in (f"a{n} * a0 = a0.", f"a0 * a{n} = a{n}."):
        txt = AX + (S_CL if withS else "") + hyps + "end_of_list.\nformulas(goals).\n" + goal + "\nend_of_list.\n"
        open('/tmp/pcp.in', 'w').write(txt)
        try:
            p = subprocess.run(['prover9', '-t', '15', '-f', '/tmp/pcp.in'], capture_output=True, text=True, timeout=30); proved = proved and ('THEOREM PROVED' in p.stdout)
        except subprocess.TimeoutExpired: proved = False
        if not proved: break
    goal = f"a{n} * a0 = a0 & a0 * a{n} = a{n}."
    txt = AX + (S_CL if withS else "") + hyps + "end_of_list.\nformulas(goals).\n" + goal + "\nend_of_list.\n"
    model = None
    if not proved:
        txt2 = txt.replace("formulas(goals).\n" + goal, "formulas(goals).\n").replace("end_of_list.\nformulas(goals).", f"a{n} * a0 != a0 | a0 * a{n} != a{n}.\nend_of_list.\nformulas(goals).")
        open('/tmp/pcm.in', 'w').write(txt2)
        try: q = subprocess.run(['mace4', '-t', '40', '-n', '2', '-N', str(mace_max), '-f', '/tmp/pcm.in'], capture_output=True, text=True, timeout=60)
        except subprocess.TimeoutExpired: return proved, None
        if 'interpretation(' in q.stdout:
            sz = q.stdout.split('interpretation(')[1].split(',')[0].strip(); model = int(sz)
    return proved, model
if __name__ == "__main__":
    n = int(sys.argv[1]); combos = json.load(open(sys.argv[2])); withS = '--S' in sys.argv
    lo, hi = [int(t) for t in sys.argv[3].split(':')] if len(sys.argv) > 3 and ':' in sys.argv[3] else (0, len(combos))
    combos = combos[lo:hi]
    V = ['p%d' % i for i in range(n + 1)]
    for c in combos:
        c = [tuple(a) for a in c]
        pr, md = run(c, n, withS)
        print([fmt(a, V) for a in c], '-> proved' if pr else f'-> not proved; Mace4 countermodel of size {md}' if md else '-> not proved, no countermodel up to size 8', flush=True)
