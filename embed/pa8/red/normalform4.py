import sys, time, random
exec(open('normalform.py').read().split("random.seed(0); t0 = time.time()")[0])
le = lambda p, q: th(q, p) == p
random.seed(0); t0 = time.time()
pairs = [(a, c) for a in P for c in P if a != c and mt(a, c) and rank(a) >= 1]
if n >= 5: pairs = random.sample(pairs, 200)
keys = ['c<=x1<=x2>=z', 'c<=x1>=x2>=z', 'c<=x>=z (2 steps)', 'c<=x1 ~ x2>=z with x1 ~ z?', 'c<=x1, x2>=z, x1 ~ x2, x2 >= x1 or x1 >= x2']
tot = hard_tot = 0; st = {k: 0 for k in keys}; sth = {k: 0 for k in keys}; ex = {}
for a, c in pairs:
    ident = lambda p: th(p, a) == th(p, c)
    I = [p for p in P if ident(p)]
    E1 = [x for x in I if comm(x, c)]; E2 = set(y for y in I if any(comm(x, y) for x in E1)); E3 = set(z for z in I if any(comm(y, z) for y in E2))
    E1ge = [x for x in E1 if le(c, x)]
    for z in E3:
        tot += 1; hard = z not in E2; hard_tot += hard
        Y2ge = [y for y in I if le(z, y)]
        r = {'c<=x1<=x2>=z': any(le(x, y) for x in E1ge for y in Y2ge), 'c<=x1>=x2>=z': any(le(y, x) for x in E1ge for y in Y2ge),
             'c<=x>=z (2 steps)': any(le(z, x) for x in E1ge), 'c<=x1 ~ x2>=z with x1 ~ z?': any(comm(x, y) and comm(x, z) for x in E1ge for y in Y2ge),
             'c<=x1, x2>=z, x1 ~ x2, x2 >= x1 or x1 >= x2': any(le(x, y) or le(y, x) for x in E1ge for y in Y2ge)}
        for k in keys:
            st[k] += r[k]; sth[k] += (r[k] and hard)
            if not r[k] and k not in ex: ex[k] = (a, c, z)
print(f"n={n}: {tot} (a,c,z), {hard_tot} hard ({time.time()-t0:.0f}s)")
show = lambda p: '  '.join(('[' if t else '(') + ' '.join(map(str, sorted(bl))) + (']' if t else ')') for bl, t in blocks(p))
for k in keys:
    print(f"   {k:48s}: {st[k]}/{tot}  hard {sth[k]}/{hard_tot}")
    if k in ex: a, c, z = ex[k]; print(f"        fail: a = {show(a)}; c = {show(c)}; z = {show(z)}")
