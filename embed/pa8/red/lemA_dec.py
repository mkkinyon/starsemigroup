"""Which consequences of c~x (local statements about (x; a, c)) suffice, with x~y and y identifying, for Lemma A(y)?"""
import sys, time, pickle
sys.argv = ['x', sys.argv[1]]
exec(open('invfam.py').read().split("if __name__ == '__main__':")[0])
# add the position-1-only predicates and a few more about x
PRED['Cin_T'] = (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), -c.Tl(c.i['c'], u), c.Tl(c.i[p], u), c.E(c.i[p], u, v)])      # T(c)-block outside supp p lies in one p-block
PRED['Nin_N'] = (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), c.Tl(c.i['c'], u), c.Tl(c.i[p], u), c.E(c.i[p], u, v)])       # N(c)-block outside supp p lies in one p-block
PRED['Tc_in_p'] = (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), -c.Tl(c.i['c'], u), -c.Tl(c.i[p], u), c.Tl(c.i[p], v)])   # T(c)-block meeting supp p inside it
PRED['Nc_in_p'] = (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), c.Tl(c.i['c'], u), -c.Tl(c.i[p], u), c.Tl(c.i[p], v)])     # N(c)-block meeting supp p inside it
PRED['Np_unionC'] = (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), -c.E(c.i[p], u, v), c.Tl(c.i[p], u), -c.Tl(c.i['c'], u), c.Tl(c.i['c'], v)])  # placeholder-ish
PRED['pT_in_c'] = (2, lambda c, p, u, v, w: [-c.E(c.i[p], u, v), -c.Tl(c.i[p], u), -c.Tl(c.i['c'], u), c.Tl(c.i['c'], v)])    # T(p)-block meeting supp c inside it
PRED['pN_in_c'] = (2, lambda c, p, u, v, w: [-c.E(c.i[p], u, v), c.Tl(c.i[p], u), -c.Tl(c.i['c'], u), c.Tl(c.i['c'], v)])     # N(p)-block meeting supp c inside it
PRED['Np_cblock'] = (2, lambda c, p, u, v, w: [-c.E(c.i[p], u, v), c.Tl(c.i[p], u), c.Tl(c.i['c'], u), c.E(c.i['c'], u, v)])  # N(p)-block with a point outside supp c lies in one c-block
PRED['cx_classes'] = (2, lambda c, p, u, v, w: [-c.J(c.i['c'], c.i[p], u, v), c.Tl(c.i[p], u), c.Tl(c.i['c'], u), c.E(c.i['c'], u, v)])  # a class of c v p containing a point outside both supports is one c-block
base1 = [('mt','a','c'), ('comm','x','c'), idf('x')]
names = list(PRED)
valid1 = [nm for nm in names if run(base1, [], (nm, 'x'))]
print(f"m={m}: valid for x with c~x, x id: {valid1}", flush=True)
step = [('mt','a','c'), idf('x'), ('comm','x','y'), idf('y')]
t0 = time.time()
ok = run(step, [(q, 'x') for q in valid1], ('A', 'y'))
print(f"m={m}: all valid-at-1 statements for x + x~y + y id => A(y): {ok} ({time.time()-t0:.0f}s)", flush=True)
if ok:
    cur = list(valid1)
    for nm in list(cur):
        trial = [q for q in cur if q != nm]
        if run(step, [(q, 'x') for q in trial], ('A', 'y')): cur = trial
    print("minimal:", cur)
