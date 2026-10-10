"""Structure of the order-8 candidates: which one-point deletions are projection algebras of graph semigroups Q(G, bot),
and how the deleted element x sits relative to them."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cand8 import subalg_delete

def graphsg_structure(A):
    """if A is the projection algebra of a graph semigroup: return (V, B, edges, bot) else None"""
    N = len(A); th = lambda p, q: A[q][p]
    B = [p for p in range(N) if all(th(p, q) == p for q in range(N))]
    V = [p for p in range(N) if p not in B]
    if not B: return None
    # every b in B is matched to every other b'
    if any(not (th(b, c) == b and th(c, b) == c) for b in B for c in B if b != c): return None
    bot = {}
    for p in V:
        below = [b for b in B if th(p, b) == b]
        if len(below) != 1: return None
        bot[p] = below[0]
        if any(th(p, b) != bot[p] for b in B): return None
    edges = set()
    for p in V:
        for q in V:
            if p == q: continue
            if th(p, q) == p: edges.add(frozenset((p, q)))
            elif th(p, q) != bot[p]: return None
    for e in edges:
        p, q = tuple(e)
        if not (th(p, q) == p and th(q, p) == q): return None
    return V, B, sorted(tuple(sorted(e)) for e in edges), bot

if __name__ == "__main__":
    recs = [json.loads(l) for l in open("post8.log")]
    cands = [r["A"] for r in recs if r["embeds"] is None]
    for k, A in enumerate(cands):
        N = len(A); th = lambda p, q: A[q][p]
        print(f"=== candidate {k} ===")
        for x in range(N):
            Bx = subalg_delete(A, x)
            if Bx is None: continue
            keep = [p for p in range(N) if p != x]
            g = graphsg_structure(Bx)
            if g is None: continue
            V, B, E, bot = g
            V = [keep[p] for p in V]; B = [keep[p] for p in B]; E = [(keep[p], keep[q]) for p, q in E]; bot = {keep[p]: keep[b] for p, b in bot.items()}
            print(f"  delete x={x}: graph semigroup, top {V}, bottom {B}, edges {E}, bot {bot}")
            print(f"     x above {[q for q in keep if th(x, q) == q]};  theta_x(p) for top p: {{{', '.join(f'{p}:{th(x,p)}' for p in V)}}};  theta_p(x): {{{', '.join(f'{p}:{th(p,x)}' for p in V)}}};  theta_x(b) for bottom b: {{{', '.join(f'{b}:{th(x,b)}' for b in B)}}}")
