import sys, time
sys.argv = ['x', sys.argv[1]]
exec(open('pairstat.py').read().split("base2 = ")[0])
base2 = [('mt','a','c'), ('comm','x','c'), idf('x'), ('comm','x','y'), idf('y')]
step = [('mt','a','c'), idf('x'), ('comm','x','y'), idf('y')]
five = ['pAC', 'aCP', 'Cin_T', 'Nin_N', 'cx_classes']
S = {
 'S1: x-block, joined in yvc => joined in yva': (2, lambda c, p, u, v, w: [-c.E(c.i['x'], u, v), -c.J(c.i['c'], c.i[p], u, v), c.J(c.i['a'], c.i[p], u, v)]),
 'S6: c-block meeting N(y)-block inside supp x lies in it': (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), c.Tl(c.i[p], u), -c.Tl(c.i['x'], u), c.E(c.i[p], u, v)]),
 'S7: S6 restricted to u outside supp a': (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), c.Tl(c.i[p], u), -c.Tl(c.i['x'], u), c.Tl(c.i['a'], u), c.E(c.i[p], u, v)]),
 'S8: c-block meeting N(y)-block lies in one class of yva (= A restricted)': (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), c.Tl(c.i[p], u), c.J(c.i['a'], c.i[p], u, v)]),
 'S9: N(x)-block = union of T(y) lies in one class of yva': (2, lambda c, p, u, v, w: [-c.E(c.i['x'], u, v), c.Tl(c.i['x'], u), -c.Tl(c.i[p], u), c.J(c.i['a'], c.i[p], u, v)]),
 'S10: N(x)-block = union of T(y) lies in one class of yvc': (2, lambda c, p, u, v, w: [-c.E(c.i['x'], u, v), c.Tl(c.i['x'], u), -c.Tl(c.i[p], u), c.J(c.i['c'], c.i[p], u, v)]),
 'S11: two points of supp y in one x-block, joined in xvc => joined in yvc': (2, lambda c, p, u, v, w: [-c.E(c.i['x'], u, v), -c.Tl(c.i[p], u), -c.Tl(c.i[p], v), -c.J(c.i['c'], c.i['x'], u, v), c.J(c.i['c'], c.i[p], u, v)]),
 'S12: c-block with a point outside supp y lies in one y-block': (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), c.Tl(c.i[p], u), c.E(c.i[p], u, v)]),
 'S13: c-block E, u outside supp y, v in supp y => joined in yva (A restricted)': (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), c.Tl(c.i[p], u), -c.Tl(c.i[p], v), c.J(c.i['a'], c.i[p], u, v)]),
 'S14: c-block E, u,v both outside supp y => joined in yva': (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), c.Tl(c.i[p], u), c.Tl(c.i[p], v), c.J(c.i['a'], c.i[p], u, v)]),
 'S15: c-block E, u,v both outside supp y => same y-block': (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), c.Tl(c.i[p], u), c.Tl(c.i[p], v), c.E(c.i[p], u, v)]),
}
for nm, pr in S.items(): PRED[nm] = pr
for nm in S:
    v2 = run(base2, [], (nm, 'y'))
    line = f"m={m}: [{nm}] valid at pos 2: {v2}"
    if v2:
        line += f"; from five(x)+step: {run(step, [(q, 'x') for q in five], (nm, 'y'))}; with it, A(y) from A(x) only: {run(step, [('A', 'x'), (nm, 'y')], ('A', 'y'))}"
    print(line, flush=True)
