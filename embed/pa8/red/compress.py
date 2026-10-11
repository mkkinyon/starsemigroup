"""Compression of 3-chains c ~ y1 ~ y2 ~ z into normal form c <= x1 ~ x2 >= z with x1 := c on supp c, y1 outside; x2 := z on supp z, y2 outside."""
import sys, time, random
exec(open('canon2.py').read().split("CONS = {")[0])
le = lambda p, q: th(q, p) == p
def splice(p, q):   # p on supp p, q outside supp p  (requires q ~ p so that blocks of q outside supp p are unions... just take q's blocks restricted)
    Sp = frozenset().union(*[pts for pts, t in blocks(p) if t]) if any(t for _, t in blocks(p)) else frozenset()
    out = [(pts, True) for pts, t in blocks(p) if t]
    for pts, t in blocks(q):
        rest = pts - Sp
        if rest: out.append((rest, t))
    return build(out)
random.seed(0); t0 = time.time()
pairs = [(a, c) for a in P for c in P if a != c and mt(a, c) and rank(a) >= 1]
if n >= 5: pairs = random.sample(pairs, 150)
tot = ok = okid = okcomm = 0; fails = []
for a, c in pairs:
    ident = lambda p: th(p, a) == th(p, c)
    I = [p for p in P if ident(p)]
    E1 = [x for x in I if comm(x, c)]
    for y1 in E1:
        for y2 in I:
            if not comm(y1, y2): continue
            for z in I:
                if not comm(y2, z): continue
                tot += 1
                x1 = splice(c, y1); x2 = splice(z, y2)
                good = x1 in Pset and x2 in Pset and ident(x1) and ident(x2) and comm(x1, x2) and le(c, x1) and le(z, x2)
                ok += good
                if not good and len(fails) < 4: fails.append((a, c, y1, y2, z, x1, x2))
print(f"n={n}: splice construction works on {ok}/{tot} 3-chains ({time.time()-t0:.0f}s)")
show = lambda p: '  '.join(('[' if t else '(') + ' '.join(map(str, sorted(bl))) + (']' if t else ')') for bl, t in blocks(p))
for a, c, y1, y2, z, x1, x2 in fails:
    ident = lambda p: th(p, a) == th(p, c)
    print(f"   a={show(a)} | c={show(c)} ~ y1={show(y1)} ~ y2={show(y2)} ~ z={show(z)};  x1={show(x1)} (id {ident(x1)}) x2={show(x2)} (id {ident(x2)}) comm {comm(x1,x2)}")
