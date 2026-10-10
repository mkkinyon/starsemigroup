"""check a 2-path quasi-identity (qi.py atoms over a,c,b + auxiliaries) against the census and the candidates"""
import sys, json, itertools, time
sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import violated_in, valid
E = '/home/claude/pa8w/embed/pa8/'
def census():
    algs = []
    for k in range(1, 8): algs += json.load(open(E + f'ord{k}.json'))
    for f in ['post8.log', 'post9_0.log', 'post9_1.log', 'post9_3.log']:
        for line in open(E + f):
            d = json.loads(line)
            if d.get('embeds') is not None: algs.append(d['A'])
    return algs
def fast_viol(T, H, concl, vars_):
    """enumerate assignments with the path matched first (a,c,b), then the rest"""
    N = len(T); th = lambda p, q: T[q][p]; mt = lambda p, q: th(p, q) == p and th(q, p) == q
    aux = [v for v in vars_ if v not in ('a', 'c', 'b')]
    def ev(t, A): return th(A[t[0]], A[t[1]]) if isinstance(t, tuple) else A[t]
    for a in range(N):
        for c in range(N):
            if not mt(a, c): continue
            for b in range(N):
                if not mt(c, b) or mt(a, b): continue
                for vals in itertools.product(range(N), repeat=len(aux)):
                    A = dict(zip(aux, vals)); A.update(a=a, c=c, b=b); good = True
                    for at in H:
                        k = at[0]
                        if k == 'mt': good = mt(A[at[1]], A[at[2]])
                        elif k == 'le': good = th(A[at[2]], A[at[1]]) == A[at[1]]
                        elif k == 'fix': good = th(A[at[1]], A[at[2]]) == A[at[1]]
                        elif k == 'comm': good = th(A[at[1]], A[at[2]]) == th(A[at[2]], A[at[1]])
                        elif k == 'eq': good = ev(at[1], A) == ev(at[2], A)
                        if not good: break
                    if good: return A
    return None
if __name__ == '__main__':
    H = json.loads(sys.argv[1]); H = [tuple(tuple(x) if isinstance(x, list) else x for x in at) for at in H]
    vars_ = sorted({x for at in H for x in at[1:] for x in (x if isinstance(x, tuple) else (x,))} | {'a','c','b'})
    concl = ('mt', 'a', 'b'); t = time.time()
    C9 = json.load(open(E + 'cand9.json'))
    print("violated by order-9 candidates:", [k for k, T in enumerate(C9) if fast_viol(T, H, concl, vars_)], flush=True)
    P8 = [json.loads(l)['A'] for l in open(E + 'post8.log') if json.loads(l).get('embeds') is None]
    print("violated by P_8^k:", [k + 1 for k, T in enumerate(P8) if fast_viol(T, H, concl, vars_)], flush=True)
    bad = [j for j, T in enumerate(census()) if fast_viol(T, H, concl, vars_)]
    print(f"embeddable census algebras violating: {len(bad)} {bad[:5]}  [{time.time()-t:.0f}s]", flush=True)
    for m in (4, 5, 6):
        t = time.time(); print(f"valid m={m}: {valid(H, concl, m)} [{time.time()-t:.0f}s]", flush=True)
