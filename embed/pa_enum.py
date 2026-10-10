"""Enumerate all projection algebras of order n satisfying (P1)'-(P5)', Q1 and the triangle condition,
up to isomorphism, with Mace4 + isofilter; write them to pa_n.out (standard interpformat).
Usage: python3 pa_enum.py n [extra options]   (needs mace4, interpformat, isofilter in PATH)
"""
import sys, subprocess, os

AXIOMS = """
op(400, infix, "*").
formulas(assumptions).
% projection algebra axioms (x * y = y x y)
x * x = x.
(y * x) * x = y * x.
(x * y) * x = y * x.
((z * x) * y) * x = z * (y * x).
(((z * x) * y) * x) * y = (z * x) * y.
% Q1:  r <= p & r <= q  ->  p q p = q p q
z * x != z | z * y != z | x * y = y * x.
% triangle condition
x1 * x2 != x2 * x3 | x1 * x2 != x3 * x1 | y1 * y2 != y2 * y3 | y1 * y2 != y3 * y1 |
x1 * y1 != y1 * x1 | x2 * y2 != y2 * x2 | x3 * y3 != y3 * x3 |
y2 * x1 != x1 | x1 * y2 != y2 | y3 * x2 != x2 | x2 * y3 != y3 | y1 * x3 != x3 | x3 * y1 != y1 |
x1 * x2 = y1 * y2.
end_of_list.
"""

def run(n, extra=""):
    inp = f"assign(domain_size, {n}).\nassign(max_models, -1).\nassign(max_seconds, -1).\n{extra}\n" + AXIOMS
    with open(f"pa_{n}.in", "w") as f: f.write(inp)
    cmd = f"mace4 -f pa_{n}.in 2>pa_{n}.err | interpformat standard | isofilter > pa_{n}.out 2>pa_{n}.iso"
    subprocess.run(cmd, shell=True, check=False)
    cnt = sum(1 for line in open(f"pa_{n}.out") if line.startswith("interpretation"))
    print(f"order {n}: {cnt} projection algebras with Q1 + triangle (up to isomorphism)", flush=True)
    return cnt

if __name__ == "__main__":
    for n in sys.argv[1:]:
        run(int(n))
