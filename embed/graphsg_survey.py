"""Survey of the graph semigroups Q(G, bot): for every graph G on k <= K vertices (up to isomorphism) and every
colouring bot: V -> B up to graph automorphisms and renaming of colours, record
  |Q|, Q1, triangle condition, number of violations of (S), and the least m with P(Q) embeddable in P(P_m) (m <= M).
Results are appended to graphsg_survey.log (one line per case, keyed by (k, E, bot)); cases already in the log
are skipped, so the script can be restarted.  Usage: python3 graphsg_survey.py K M [--sat]"""
import sys, itertools, time, os, json
from graphsg import semigroup, proj_algebra, is_rss, q1, graphs
from pa_embed2 import PPm, embed
from digraph import clause, parse_clause, search

LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graphsg_survey.log")

def s_violations(A):
    """A[x][y] = theta_y(x); count (a,b,c,d) violating (S)."""
    N = len(A); th = lambda p, q: A[q][p]
    bad = 0
    for a, b, c, d in itertools.product(range(N), repeat=4):
        if not (th(a, c) == a and th(c, a) == c and th(b, c) == b and th(c, b) == c and th(b, d) == b and th(d, b) == d): continue
        z = th(c, d)
        if z != th(d, c) or th(a, z) != th(b, z): continue
        if not (th(a, d) == a and th(d, a) == d): bad += 1
    return bad

def colourings(k, E):
    """colourings V -> {0..nb-1}, nb <= k, up to automorphisms of (V,E) and renaming of colours"""
    Es = sorted(E)
    auts = [perm for perm in itertools.permutations(range(k)) if sorted(tuple(sorted((perm[u], perm[v]))) for u, v in E) == Es]
    seen = set()
    for nb in range(1, k + 1):
        for col in itertools.product(range(nb), repeat=k):
            if len(set(col)) != nb: continue
            keys = []
            for perm in auts:
                c2 = tuple(col[perm[i]] for i in range(k)); ren = {}
                keys.append(tuple(ren.setdefault(c, len(ren)) for c in c2))
            key = min(keys)
            if key in seen: continue
            seen.add(key); yield key

def done_keys():
    out = set()
    if os.path.exists(LOG):
        for line in open(LOG):
            try: d = json.loads(line); out.add((d["k"], tuple(map(tuple, d["E"])), tuple(d["bot"])))
            except Exception: pass
    return out

if __name__ == "__main__":
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    M = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    use_sat = "--sat" in sys.argv
    done = done_keys(); Ds = {}
    for k in range(1, K + 1):
        V = list(range(k))
        for E in graphs(k):
            for key in colourings(k, E):
                if (k, tuple(map(tuple, E)), key) in done: continue
                nb = len(set(key)); B = [f"m{c}" for c in range(nb)]; bot = {v: f"m{key[v]}" for v in V}
                elems, T, st = semigroup(V, E, bot, B)
                assert is_rss(T, st)
                P, A = proj_algebra(elems, T, st)
                ok1 = q1(A)
                t0 = time.time()
                try:
                    tri = [] if len(A) < 6 else search(parse_clause(clause(3, [(1, 2), (2, 3), (3, 1)])), range(len(A)), lambda x, y: A[x][y], limit=600)
                    tri = "ok" if tri == [] else "FAILS"
                except TimeoutError: tri = "timeout"
                sv = s_violations(A)
                found = None if ok1 else "skipped(noQ1)"
                for m in (range(1, M + 1) if ok1 else []):
                    if m not in Ds: Ds[m] = PPm(m)
                    r = embed(A, Ds[m], limit=900)
                    if r == "timeout": found = f"timeout@{m}"; break
                    if r is not None: found = m; break
                if found is None and use_sat:
                    from pa_sat import solve
                    for m in range(M + 1, M + 3):
                        r = solve(A, m, verbose=False, timeout=1800)
                        if r == "timeout": found = f"timeout@{m}"; break
                        if r: found = m; break
                rec = dict(k=k, E=E, bot=list(key), Q=len(elems), P=len(P), Q1=ok1, triangle=tri, S_viol=sv, embeds=found, secs=round(time.time() - t0, 1))
                with open(LOG, "a") as f: f.write(json.dumps(rec) + "\n")
                print(rec, flush=True)
