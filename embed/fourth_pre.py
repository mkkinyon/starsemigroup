"""A 26-element regular *-semigroup T26 with a *-congruence whose quotient is T19: the bottom band of T19 is
enlarged by splitting v into v (= xc) and v' (= xbx).  If T26 satisfies (R) (or embeds in a partition monoid),
then (R) defines a proper quasivariety."""
import itertools, json, sys
from graphsg import is_rss, q1
from layered import proj_algebra
from layered_search import canon
from fourth import T19, R_violations
from graphsg_survey import s_violations
from pa7_post import triangle_ok

def T26(lam_w):
    top = ['a', 'c', 'b']; bot = ['u', 'v', 'w', 'V']          # V = v'
    B = {'a': 'u', 'c': 'v', 'b': 'w'}
    L = {'a': 'u', 'c': 'v', 'b': 'V', 'u': 'u', 'v': 'v', 'V': 'V', 'w': lam_w}
    adj = {frozenset(['a', 'c']), frozenset(['c', 'b'])}
    def mt(p, q): return p == q or frozenset([p, q]) in adj
    elems = ['x'] + [(p, q) for p in top for q in top] + [(m, n) for m in bot for n in bot]
    def mul(s, t):
        if s == 'x' and t == 'x': return 'x'
        if s == 'x':
            p, q = t; return (L[p], q if p in bot else B[q])
        if t == 'x':
            p, q = s; return (p if p in bot else B[p], L[q])
        p, q = s; r, u = t
        if p in top and r in top: return (p, u) if mt(q, r) else (B[p], B[u])
        return (p if p in bot else B[p], u if u in bot else B[u])
    idx = {e: i for i, e in enumerate(elems)}
    T = [[idx[mul(s, t)] for t in elems] for s in elems]
    st = [idx['x' if s == 'x' else (s[1], s[0])] for s in elems]
    return elems, T, st

def quotient_is_T19(elems, T, st):
    """collapse V -> v and compare with T19"""
    e19, T19t, st19 = T19(); i19 = {e: i for i, e in enumerate(e19)}
    def f(e):
        if e == 'x': return 'x'
        return tuple('v' if z == 'V' else z for z in e)
    for s in range(len(elems)):
        for t in range(len(elems)):
            if i19[f(elems[T[s][t]])] != T19t[i19[f(elems[s])]][i19[f(elems[t])]]: return False
        if i19[f(elems[st[s]])] != st19[i19[f(elems[s])]]: return False
    return True

if __name__ == "__main__":
    for lam_w in ('V', 'v'):
        elems, T, st = T26(lam_w)
        ok = is_rss(T, st)
        print(f"lambda(w) = {lam_w}: {len(elems)} elements, regular *-semigroup: {ok}")
        if not ok: continue
        print("   collapsing v' to v is a *-homomorphism onto T19:", quotient_is_T19(elems, T, st))
        P, A = proj_algebra(elems, T, st)
        print("   projection algebra: order", len(P), "| Q1", q1(A), "| (S) viol", s_violations(A), "| triangle", triangle_ok(A), "| (R) viol", R_violations(A))
        json.dump(dict(names=[elems[p][0] if elems[p] != 'x' else 'x' for p in P], A=A), open(f"T26_{lam_w}.json", "w"))
