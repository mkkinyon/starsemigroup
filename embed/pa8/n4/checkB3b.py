import sys, json, time
E = '/home/claude/pa8w/embed/pa8/'
def viol_B3(T):
    N = len(T); th = lambda p, q: T[q][p]
    mt = lambda p, q: th(p, q) == p and th(q, p) == q
    for a in range(N):
        for d in range(N):
            if not mt(a, d): continue
            for b in range(N):
                if not mt(d, b) or mt(a, b): continue
                for h in range(N):
                    if th(h, d) != th(d, h) or th(h, a) != th(h, d): continue
                    for i in range(N):
                        if th(i, b) == th(b, i) and th(h, b) == th(i, a): return (a, d, b, h, i)
    return None
algs = []
for k in range(1, 8): algs += json.load(open(E + f'ord{k}.json'))
for f in ['post8.log', 'post9_0.log', 'post9_1.log', 'post9_3.log']:
    for line in open(E + f):
        d = json.loads(line)
        if d.get('embeds') is not None: algs.append(d['A'])
t = time.time(); bad = 0
for j, T in enumerate(algs):
    v = viol_B3(T)
    if v: bad += 1; print("  VIOLATED by embeddable algebra", j, v, T, flush=True)
print(f"census check: {len(algs)} embeddable algebras, {bad} violate B3  [{time.time()-t:.0f}s]", flush=True)
C9 = json.load(open(E + 'cand9.json')); print("order-9 candidates violating:", [k for k, T in enumerate(C9) if viol_B3(T)])
