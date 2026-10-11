import sys
m_arg = sys.argv[1]; sys.argv = ['x', m_arg]
exec(open('modules.py').read().split("step = ")[0])
step = [('mt','a','c'), idf('x'), ('comm','x','y'), idf('y')]
base2 = [('mt','a','c'), ('comm','x','c'), idf('x'), ('comm','x','y'), idf('y')]
hy = [('A','x'), ('M','x'), ('Np_cblock','x')]
C = {
 'delta: c-block meeting an N(y)-block does not meet supp y': (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), c.Tl(c.i[p], u), -c.Tl(c.i[p], v)]),
 'eps: two points of a c-block outside supp y are in one y-block': (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), c.Tl(c.i[p], u), c.Tl(c.i[p], v), c.E(c.i[p], u, v)]),
 'delta_T: T(c)-block meeting an N(y)-block does not meet supp y': (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), -c.Tl(c.i['c'], u), c.Tl(c.i[p], u), -c.Tl(c.i[p], v)]),
 'delta_N: N(c)-block meeting an N(y)-block does not meet supp y': (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), c.Tl(c.i['c'], u), c.Tl(c.i[p], u), -c.Tl(c.i[p], v)]),
 'eps_N: N(c)-block, two points outside supp y => one y-block': (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), c.Tl(c.i['c'], u), c.Tl(c.i[p], u), c.Tl(c.i[p], v), c.E(c.i[p], u, v)]),
 'zeta: c-block E, u outside supp y, v in supp y => u,v in one x-block or v in supp x?': (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), c.Tl(c.i[p], u), -c.Tl(c.i[p], v), c.E(c.i['x'], u, v), c.Tl(c.i['x'], v)]),
 'eta: c-block E, u outside supp y: u outside supp x or E inside supp x?': (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), c.Tl(c.i[p], u), -c.Tl(c.i['x'], u), c.Tl(c.i['x'], v)]),
 'theta: N(y)-block of type (ii) [union of T(x)] lies in one class of x v a': (2, lambda c, p, u, v, w: [-c.E(c.i[p], u, v), c.Tl(c.i[p], u), -c.Tl(c.i['x'], u), c.J(c.i['a'], c.i['x'], u, v)]),
 'iota: N(y)-block of type (ii) lies in one class of x v c': (2, lambda c, p, u, v, w: [-c.E(c.i[p], u, v), c.Tl(c.i[p], u), -c.Tl(c.i['x'], u), c.J(c.i['c'], c.i['x'], u, v)]),
 'kappa: c-block meeting a type-(ii) N(y)-block lies inside it': (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), c.Tl(c.i[p], u), -c.Tl(c.i['x'], u), c.E(c.i[p], u, v)]),
 'lambda: c-block meeting a type-(ii) N(y)-block N at u: v in N or v outside supp y': (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), c.Tl(c.i[p], u), -c.Tl(c.i['x'], u), c.E(c.i[p], u, v), -c.Tl(c.i[p], v)]),
}
for nm, pr in C.items():
    PRED[nm] = pr
    print(f"m={m}: [{nm}]: valid at pos 2 (real chain): {run(base2, [], (nm, 'y'))}; from hyps(A,M,Np): {run(step, hy, (nm, 'y'))}", flush=True)
