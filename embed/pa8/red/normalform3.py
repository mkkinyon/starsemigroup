import sys, time, random
exec(open('normalform.py').read().split("random.seed(0); t0 = time.time()")[0])
le = lambda p, q: th(q, p) == p      # p <= q  (q p q = p)
random.seed(0); t0 = time.time()
pairs = [(a, c) for a in P for c in P if a != c and mt(a, c) and rank(a) >= 1]
if n >= 5: pairs = random.sample(pairs, 200)
keys = ['c<=x1', 'z<=x2', 'x2<=z', 'c<=x1 & z<=x2', 'c<=x1 & x2<=z', 'c<=x1 & x1 in Split(c)', 'x1<=c']
tot = hard_tot = 0; st = {k: 0 for k in keys}; sth = {k: 0 for k in keys}
for a, c in pairs:
    ident = lambda p: th(p, a) == th(p, c)
    I = [p for p in P if ident(p)]
    E1 = [x for x in I if comm(x, c)]; E2 = set(y for y in I if any(comm(x, y) for x in E1)); E3 = set(z for z in I if any(comm(y, z) for y in E2))
    E1ge = [x for x in E1 if le(c, x)]; E1le = [x for x in E1 if le(x, c)]; E1sp = [x for x in E1 if in_split(x, c)]
    for z in E3:
        tot += 1; hard = z not in E2; hard_tot += hard
        Y2 = [y for y in I if comm(y, z)]; Y2ge = [y for y in Y2 if le(z, y)]; Y2le = [y for y in Y2 if le(y, z)]
        r = {'c<=x1': any(comm(x, y) for x in E1ge for y in Y2), 'z<=x2': any(comm(x, y) for x in E1 for y in Y2ge), 'x2<=z': any(comm(x, y) for x in E1 for y in Y2le),
             'c<=x1 & z<=x2': any(comm(x, y) for x in E1ge for y in Y2ge), 'c<=x1 & x2<=z': any(comm(x, y) for x in E1ge for y in Y2le),
             'c<=x1 & x1 in Split(c)': any(comm(x, y) for x in E1sp for y in Y2), 'x1<=c': any(comm(x, y) for x in E1le for y in Y2)}
        for k in keys: st[k] += r[k]; sth[k] += (r[k] and hard)
print(f"n={n}: {tot} (a,c,z), {hard_tot} hard ({time.time()-t0:.0f}s)")
for k in keys: print(f"   {k:28s}: {st[k]}/{tot}  hard {sth[k]}/{hard_tot}")
