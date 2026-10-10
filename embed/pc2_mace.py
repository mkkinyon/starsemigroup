"""Mace4 countermodel search (orders 2..MAXN) for two-auxiliary path-closing candidates, under Q1 (+S)(+R).
Usage: python3 pc2_mace.py n candidates.json MODE [MAXN]   (MODE in Q1, S, R, SR); results in pc2mace_<mode>_<base>/"""
import json, sys, os, subprocess
os.environ["PATH"] = "/home/claude/bin:" + os.environ["PATH"]
from pc_prover import AX, S_CL
R_CL = """z1 * x1 != x1 | x1 * z1 != z1 | z1 * y1 != y1 | y1 * z1 != z1 | x1 * x != x * x1 | z1 * x != x * z1 | y1 * x != z1 * x | y1 * x1 = x1.
z1 * x1 != x1 | x1 * z1 != z1 | z1 * y1 != y1 | y1 * z1 != z1 | x1 * x != x * x1 | z1 * x != x * z1 | y1 * x != z1 * x | x1 * y1 = y1.
"""
def a2s(at):
    P = ['a0', 'a1', 'a2', 'a3', 'a4', 'a5']
    if at[0] in ('x', 'y'):
        z = 'c' if at[0] == 'x' else 'd'; k = at[1]
        if k == 'comm': return f"{P[at[2]]} * {z} = {z} * {P[at[2]]}."
        if k == 'zle': return f"{z} * {P[at[2]]} = {z}."
        if k == 'lez': return f"{P[at[2]]} * {z} = {P[at[2]]}."
        if k == 'sees': return f"{P[at[2]]} * {z} = {P[at[3]]} * {z}."
        if k == 'seen': return f"{z} * {P[at[2]]} = {z} * {P[at[3]]}."
        if k == 'zeq': return f"{P[at[3]]} * {P[at[2]]} = {z}."
    k = at[1]; i = P[at[2]] if len(at) > 2 else None
    if k == 'comm': return "c * d = d * c."
    if k == 'xley': return "c * d = c."          # theta_d(c) = c
    if k == 'ylex': return "d * c = d."
    if k == 'sees': return f"{i} * c = {i} * d."   # theta_c(p) = theta_d(p)
    if k == 'seen': return f"c * {i} = d * {i}."   # theta_p(c) = theta_p(d)
    if k == 'x=th_y': return f"{i} * d = c."       # theta_d(p) = c
    if k == 'y=th_x': return f"{i} * c = d."
    if k == 'x=th_p_y': return f"d * {i} = c."     # theta_p(d) = c
    if k == 'y=th_p_x': return f"c * {i} = d."
n = int(sys.argv[1]); combos = json.load(open(sys.argv[2])); mode = sys.argv[3]; maxn = int(sys.argv[4]) if len(sys.argv) > 4 else 9
base = os.path.basename(sys.argv[2]).replace('.json', ''); d = f"pc2mace_{mode}_{base}"; os.makedirs(d, exist_ok=True)
for i, c in enumerate(combos):
    if os.path.exists(f"{d}/{i}.done"): continue
    hyps = "".join(f"a{k+1} * a{k} = a{k}. a{k} * a{k+1} = a{k+1}.\n" for k in range(n)) + "".join(a2s(tuple(a)) + "\n" for a in c)
    txt = AX + (S_CL if 'S' in mode else '') + (R_CL if 'R' in mode else '') + hyps + f"a{n} * a0 != a0 | a0 * a{n} != a{n}.\nend_of_list.\n"
    open(f"{d}/{i}.in", "w").write(txt)
    q = subprocess.run(['mace4', '-n', '2', '-N', str(maxn), '-m', '1', '-b', '2000', '-f', f"{d}/{i}.in"], capture_output=True, text=True)
    sz = q.stdout.split('interpretation(')[1].split(',')[0].strip() if 'interpretation(' in q.stdout else '0'
    open(f"{d}/{i}.done", "w").write(sz + "\n")
    print(i, c, 'countermodel of size' if sz != '0' else 'none', sz, flush=True)
