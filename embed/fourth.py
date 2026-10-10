"""The fourth obstruction.  The 7-element projection algebra P7 = {a,c,b,x,u,v,w} (found by the order-7 census
pa7_driver.sh / pa7_post.py: the only algebra of order 7 with Q1 and (S) that does not embed in P(P_m), m <= 8):
  a ~ c ~ b (path), bottom band {u,v,w} pairwise matched, u <= a,x; v <= c,x; w <= b;
  x commutes with a (product u) and with c (product v); theta_x(b) = v, theta_b(x) = w; all other values fall to
  the bottom of the subscript.  It satisfies Q1, the triangle condition and (S), but violates
  (R):  a ~ c, b ~ c, xa = ax, xc = cx, theta_x(b) = theta_x(c)  ==>  a ~ b,
which holds in P(P_m) for m <= 5 (all instances) and m <= 6 (SAT on the partial table).
T19: a 19-element regular *-semigroup with projection algebra P7 (the graph semigroup of the path with injective
colouring, plus the element x).  Usage: python3 fourth.py"""
import itertools, json, os
from graphsg import is_rss
from layered import proj_algebra
from layered_search import canon

NAMES = ['a', 'c', 'b', 'x', 'u', 'v', 'w']
# theta_p(q) (rows p, columns q)
THETA = {
 'a': 'a a u u u u u', 'c': 'c c c v v v v', 'b': 'w b b w w w w', 'x': 'u v v x u v v',
 'u': 'u u u u u u u', 'v': 'v v v v v v v', 'w': 'w w w w w w w'}
TH = {p: dict(zip(NAMES, THETA[p].split())) for p in NAMES}
def table():
    """A[x][y] = theta_y(x) with elements indexed as in NAMES"""
    return [[NAMES.index(TH[q][p]) for q in NAMES] for p in NAMES]

def T19():
    top = ['a', 'c', 'b']; bot = ['u', 'v', 'w']
    B = {'a': 'u', 'c': 'v', 'b': 'w'}                   # bottom of a top element
    L = {'a': 'u', 'c': 'v', 'b': 'v', 'u': 'u', 'v': 'v', 'w': 'v'}   # x-side view: x p x (as bottom element)
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

def R_violations(A):
    """A[x][y] = theta_y(x); instances (a,b,c,x) of the hypotheses of (R) with a, b not matched"""
    N = len(A); th = lambda p, q: A[q][p]
    mt = lambda p, q: th(p, q) == p and th(q, p) == q
    out = []
    for a, b, c, x in itertools.product(range(N), repeat=4):
        if mt(a, c) and mt(b, c) and th(x, a) == th(a, x) and th(x, c) == th(c, x) and th(x, b) == th(x, c) and not mt(a, b):
            out.append((a, b, c, x))
    return out

def R_in_PPm(m):
    from pa_embed2 import PPm
    D = PPm(m); N = D.N; tab = D.tab; th = lambda p, q: tab[q][p]
    mt = lambda p, q: th(p, q) == p and th(q, p) == q
    matched = {p: [q for q in range(N) if mt(p, q)] for p in range(N)}
    comm = {p: [q for q in range(N) if th(p, q) == th(q, p)] for p in range(N)}
    inst = viol = 0
    for c in range(N):
        for a in matched[c]:
            ca = set(comm[a])
            for b in matched[c]:
                for x in comm[c]:
                    if x in ca and th(x, b) == th(x, c):
                        inst += 1
                        if not mt(a, b): viol += 1
    return inst, viol

if __name__ == "__main__":
    A = table()
    from graphsg import q1
    from graphsg_survey import s_violations
    from pa7_post import triangle_ok
    print("P7: Q1", q1(A), "| (S) violations", s_violations(A), "| triangle", triangle_ok(A), "| (R) violations", [tuple(NAMES[i] for i in t) for t in R_violations(A)])
    elems, T, st = T19()
    print("T19:", len(elems), "elements, regular *-semigroup:", is_rss(T, st))
    P, B = proj_algebra(elems, T, st)
    print("   projection algebra = P7:", canon(B) == canon(A))
    here = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(os.path.join(here, "cand7.json")):
        print("   = the census algebra cand7.json:", canon(json.load(open(os.path.join(here, "cand7.json")))) == canon(A))
    for m in (3, 4, 5):
        print("(R) in P(P_%d): instances %d, violations %d" % ((m,) + R_in_PPm(m)))
