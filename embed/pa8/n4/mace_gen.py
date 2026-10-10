"""Mace4 input for a witness of a path-closing candidate: a projection algebra satisfying all conditions of
conditions.in (optionally minus some labels) in which the candidate fails.
Usage: python3 mace_gen.py n 'atoms-json' outfile [drop_label,...]"""
import sys, json, re
sys.path.insert(0, '/home/claude/pa8w/n4')
from pathclose4b import fmt
def mace_input(n, H, drop=()):
    src = open('/mnt/user-data/outputs/conditions.in').read()
    body = src[src.index('formulas(assumptions).'):src.index('end_of_list.')]
    if drop:
        # remove the formulas whose label is in drop (each formula ends at the line containing its label)
        out, buf = [], []
        for line in body.split('\n'):
            buf.append(line)
            m = re.search(r'# label\("(.*)"\)', line)
            if m or line.strip() == '' or line.startswith('%') or line.startswith('formulas'):
                if not (m and m.group(1) in drop): out += buf
                buf = []
        body = '\n'.join(out + buf)
    P = ['p%d' % i for i in range(n + 1)]; Z = {'x': 'x', 'y': 'y'}
    facts = []
    for i in range(n): facts += [f"{P[i+1]}*{P[i]} = {P[i]}", f"{P[i]}*{P[i+1]} = {P[i+1]}"]
    for at in H:
        if at[0] == 'ch': facts += [f"{P[at[2]]}*{P[at[1]]} = {P[at[1]]}", f"{P[at[1]]}*{P[at[2]]} = {P[at[2]]}"]
        elif at[0] in ('x', 'y'):
            z, k = Z[at[0]], at[1]
            if k == 'comm': facts.append(f"{z}*{P[at[2]]} = {P[at[2]]}*{z}")
            elif k == 'zle': facts.append(f"{z}*{P[at[2]]} = {z}")
            elif k == 'sees': facts.append(f"{P[at[2]]}*{z} = {P[at[3]]}*{z}")
            elif k == 'seen': facts.append(f"{z}*{P[at[2]]} = {z}*{P[at[3]]}")
        else:
            k = at[1]
            if k == 'comm': facts.append("x*y = y*x")
            elif k == 'xley': facts.append("x*y = x")
            elif k == 'ylex': facts.append("y*x = y")
            elif k == 'sees': facts.append(f"{P[at[2]]}*x = {P[at[2]]}*y")
            elif k == 'seen': facts.append(f"x*{P[at[2]]} = y*{P[at[2]]}")
            elif k == 'xsees': facts.append(f"{P[at[2]]}*x = {P[at[3]]}*y")
            elif k == 'xseen': facts.append(f"x*{P[at[2]]} = y*{P[at[3]]}")
    facts.append(f"{P[n]}*{P[0]} != {P[0]} | {P[0]}*{P[n]} != {P[n]}")
    head = "set(prolog_style_variables).\nop(400, infix, \"*\").\nassign(max_seconds, -1).\nassign(max_megs, 6000).\n\n"
    cand = "% candidate: " + ', '.join(fmt(tuple(a)) for a in H) + f"  =>  p0 ~ p{n}\n"
    return head + cand + body + "\n% --- negated candidate instance ---\n" + '\n'.join(f + '.' for f in facts) + "\n\nend_of_list.\n"
if __name__ == "__main__":
    n = int(sys.argv[1]); H = [tuple(a) for a in json.loads(sys.argv[2])]; out = sys.argv[3]
    drop = sys.argv[4].split(',') if len(sys.argv) > 4 else ()
    open(out, 'w').write(mace_input(n, H, drop)); print("wrote", out)

def prover_input(n, H, drop=(), secs=60):
    """Prover9 input: known conditions (conditions.in) as assumptions, the candidate (universally quantified) as goal."""
    src = open('/mnt/user-data/outputs/conditions.in').read()
    body = src[src.index('formulas(assumptions).'):src.index('end_of_list.')]
    if drop:
        out, buf = [], []
        for line in body.split('\n'):
            buf.append(line)
            m = re.search(r'# label\("(.*)"\)', line)
            if m or line.strip() == '' or line.startswith('%') or line.startswith('formulas'):
                if not (m and m.group(1) in drop): out += buf
                buf = []
        body = '\n'.join(out + buf)
    P = ['P%d' % i for i in range(n + 1)]; Z = {'x': 'X', 'y': 'Y'}
    hyps = []
    for i in range(n): hyps += [f"{P[i+1]}*{P[i]} = {P[i]}", f"{P[i]}*{P[i+1]} = {P[i+1]}"]
    for at in H:
        if at[0] == 'ch': hyps += [f"{P[at[2]]}*{P[at[1]]} = {P[at[1]]}", f"{P[at[1]]}*{P[at[2]]} = {P[at[2]]}"]
        elif at[0] in ('x', 'y'):
            z, k = Z[at[0]], at[1]
            if k == 'comm': hyps.append(f"{z}*{P[at[2]]} = {P[at[2]]}*{z}")
            elif k == 'zle': hyps.append(f"{z}*{P[at[2]]} = {z}")
            elif k == 'sees': hyps.append(f"{P[at[2]]}*{z} = {P[at[3]]}*{z}")
            elif k == 'seen': hyps.append(f"{z}*{P[at[2]]} = {z}*{P[at[3]]}")
        else:
            k = at[1]
            if k == 'comm': hyps.append("X*Y = Y*X")
            elif k == 'xley': hyps.append("X*Y = X")
            elif k == 'ylex': hyps.append("Y*X = Y")
            elif k == 'sees': hyps.append(f"{P[at[2]]}*X = {P[at[2]]}*Y")
            elif k == 'seen': hyps.append(f"X*{P[at[2]]} = Y*{P[at[2]]}")
            elif k == 'xsees': hyps.append(f"{P[at[2]]}*X = {P[at[3]]}*Y")
            elif k == 'xseen': hyps.append(f"X*{P[at[2]]} = Y*{P[at[3]]}")
    goal = "(" + " & ".join(hyps) + f") -> ({P[n]}*{P[0]} = {P[0]} & {P[0]}*{P[n]} = {P[n]})"
    head = f"set(prolog_style_variables).\nop(400, infix, \"*\").\nassign(max_seconds, {secs}).\nassign(max_megs, 2000).\n\n"
    return head + body + "end_of_list.\n\nformulas(goals).\n" + goal + ".\nend_of_list.\n"
