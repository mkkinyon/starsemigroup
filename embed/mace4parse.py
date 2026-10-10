"""Parse Mace4 interpretation blocks (raw, 'standard' or 'portable' interpformat) for a
binary operation * and constants, and test projection-algebra properties:
axioms (P1)'-(P5)', Q1, and the matching-pattern conditions (hexagon, triangle, ...).
Usage:  python3 mace4parse.py file.out
"""
import re, sys, itertools
from termeval import make_eval
from digraph import clause, parse_clause, search, CONDS

def parse_models(text):
    """yield (size, table[N][N], constants{name: value}) for each interpretation."""
    text = re.sub(r"%.*", "", text)
    # raw / standard:  interpretation( N, [...], [ function(*(_,_), [ ... ]), function(a1, [3]), ... ])
    for m in re.finditer(r"interpretation\(\s*(\d+)\s*,\s*\[[^\]]*\]\s*,\s*\[(.*?)\]\s*\)\s*\.", text, re.S):
        N = int(m.group(1)); body = m.group(2)
        table = None; consts = {}
        for f in re.finditer(r"function\(\s*([^\s,(]+)(\(_,_\)|\(_\))?\s*,\s*\[([^\]]*)\]\s*\)", body):
            name, arity, vals = f.group(1), f.group(2), [int(v) for v in re.findall(r"\d+", f.group(3))]
            if arity == "(_,_)":
                if name == "*" or table is None:
                    table = [vals[i * N:(i + 1) * N] for i in range(N)]
            elif arity is None:
                consts[name] = vals[0]
        if table is not None:
            yield N, table, consts
    # portable: [ N, [...], [ ["function", "*", 2, [ ... ]], ["function", "a1", 0, [3]] ] ]  (roughly)
    for m in re.finditer(r"\[\s*(\d+)\s*,\s*\[[^\]]*\]\s*,\s*\[(.*?)\]\s*\]\s*[,.]?\s*(?=\n|$)", text, re.S):
        body = m.group(2)
        if '"function"' not in body: continue
        N = int(m.group(1)); table = None; consts = {}
        for f in re.finditer(r'\[\s*"function"\s*,\s*"([^"]+)"\s*,\s*(\d+)\s*,\s*\[([^\]]*)\]', body):
            name, ar, vals = f.group(1), int(f.group(2)), [int(v) for v in re.findall(r"\d+", f.group(3))]
            if ar == 2 and (name == "*" or table is None):
                table = [vals[i * N:(i + 1) * N] for i in range(N)]
            elif ar == 0:
                consts[name] = vals[0]
        if table is not None:
            yield N, table, consts

AXIOMS = ["x * x = x", "(y * x) * x = y * x", "(x * y) * x = y * x",
          "((z * x) * y) * x = z * (y * x)", "(((z * x) * y) * x) * y = (z * x) * y"]

def analyse(N, T, consts):
    op = lambda x, y: T[x][y]; ev = make_eval(op)
    print(f"model of size {N}; constants {consts}")
    for a in AXIOMS:
        l, r = a.split("="); vs = sorted(set(re.findall(r"[xyz]", a)))
        bad = [v for v in itertools.product(range(N), repeat=len(vs))
               if ev(l, dict(zip(vs, v))) != ev(r, dict(zip(vs, v)))]
        print(f"  axiom {a}: {'OK' if not bad else f'FAILS at {bad[0]}'}")
    # Q1: r*p = r & r*q = r  ->  p*q = q*p
    q1 = [(p, q) for p in range(N) for q in range(N) if T[p][q] != T[q][p]
          and any(T[r][p] == r and T[r][q] == r for r in range(N))]
    print(f"  Q1: {'holds' if not q1 else f'fails, e.g. p,q = {q1[0]}'}")
    for name, (k, E) in CONDS.items():
        if "FAIL" in name: continue
        res = search(parse_clause(clause(k, E)), range(N), op, distinct=False, limit=600)
        if res == "timeout":
            print(f"  {name}: timeout")
        elif res:
            e = res[0]; w = T[e['x1']][e['x2']]; z = T[e['y1']][e['y2']]
            print(f"  {name}: FAILS at {dict(sorted(e.items()))}  (w={w}, z={z})")
        else:
            print(f"  {name}: holds")

if __name__ == "__main__":
    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    n = 0
    for N, T, consts in parse_models(text):
        n += 1; analyse(N, T, consts)
    if n == 0:
        print("no interpretation found in input")
