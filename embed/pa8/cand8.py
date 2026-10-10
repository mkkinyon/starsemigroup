"""Analysis of the order-8 candidates (post8.log records with embeds = None): structure, minimality, mutual relations.
Table convention: A[x][y] = x*y = theta_y(x);  x <= y iff A[x][y] == x;  x ~ y iff A[x][y] == y and A[y][x] == x."""
import sys, os, json, itertools
EMBED = os.environ.get("EMBED_DIR", "/mnt/user-data/outputs/starsemigroup/embed"); sys.path.insert(0, EMBED)
from layered_search import canon
from pa_sat import solve
from pa_embed2 import PPm, embed
from graphsg import q1
from graphsg_survey import s_violations
from fourth import R_violations

def th(A, p, q): return A[q][p]
def describe(A):
    N = len(A)
    le = lambda x, y: A[x][y] == x
    mt = lambda x, y: A[x][y] == y and A[y][x] == x
    comm = lambda x, y: A[x][y] == A[y][x]
    bottom = [p for p in range(N) if all(th(A, p, q) == p for q in range(N))]
    print("  bottom (theta_p constant):", bottom)
    for p in range(N):
        below = [q for q in range(N) if q != p and le(q, p)]
        above = [q for q in range(N) if q != p and le(p, q)]
        m = [q for q in range(N) if q != p and mt(p, q)]
        c = [(q, A[p][q]) for q in range(N) if q != p and comm(p, q) and not le(q, p) and not le(p, q)]
        nc = [(q, th(A, p, q), th(A, q, p)) for q in range(N) if q != p and not comm(p, q) and not mt(p, q)]
        print(f"  {p}: below={below} above={above} matched={m} comm(q,prod)={c} noncomm(q,th_p(q),th_q(p))={nc}")

def subalg_delete(A, e):
    """table of A \\ {e} if it is a subalgebra, else None"""
    N = len(A); keep = [p for p in range(N) if p != e]
    if any(A[x][y] == e for x in keep for y in keep): return None
    pos = {p: i for i, p in enumerate(keep)}
    return [[pos[A[x][y]] for y in keep] for x in keep]

if __name__ == "__main__":
    recs = [json.loads(l) for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "post8.log"))]
    cands = [r["A"] for r in recs if r["embeds"] is None]
    print(len(cands), "candidates")
    for k, A in enumerate(cands):
        print(f"\n=== candidate {k} ===")
        for row in A: print("   ", row)
        assert q1(A) and s_violations(A) == 0 and not R_violations(A)
        describe(A)
        # minimality: every one-point deletion that is a subalgebra
        for e in range(len(A)):
            B = subalg_delete(A, e)
            if B is None: print(f"  delete {e}: not a subalgebra"); continue
            f = None
            for m in range(1, 7):
                if solve(B, m, verbose=False): f = m; break
            print(f"  delete {e}: subalgebra, embeds in P(P_{f})" if f else f"  delete {e}: subalgebra, NO embedding m<=6")
    # pairwise: does candidate k contain candidate l as a subalgebra?
    keys = [canon(A) for A in cands]
    print("\ndistinct up to iso:", len(set(keys)))
