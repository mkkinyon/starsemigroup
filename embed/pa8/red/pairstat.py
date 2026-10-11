import sys, time
sys.argv = ['x', sys.argv[1]]
exec(open('lemA_dec.py').read().split("base1 = ")[0])
# pair statements about (x, y): expressed as predicates with p = y and x fixed by name
PRED['x_le_ya'] = (2, lambda c, p, u, v, w: [-c.E(c.i['x'], u, v), c.J(c.i['a'], c.i[p], u, v)])      # eps_x <= eps_a v eps_p
PRED['x_le_yc'] = (2, lambda c, p, u, v, w: [-c.E(c.i['x'], u, v), c.J(c.i['c'], c.i[p], u, v)])
PRED['xa_le_ya'] = (2, lambda c, p, u, v, w: [-c.J(c.i['a'], c.i['x'], u, v), c.J(c.i['a'], c.i[p], u, v)])   # eps_x v eps_a <= eps_y v eps_a
PRED['Tx_le_ya'] = (2, lambda c, p, u, v, w: [-c.E(c.i['x'], u, v), -c.Tl(c.i['x'], u), c.J(c.i['a'], c.i[p], u, v)])
PRED['Nx_le_ya'] = (2, lambda c, p, u, v, w: [-c.E(c.i['x'], u, v), c.Tl(c.i['x'], u), c.J(c.i['a'], c.i[p], u, v)])
base2 = [('mt','a','c'), ('comm','x','c'), idf('x'), ('comm','x','y'), idf('y')]
base3 = base2 + [('comm','y','z'), idf('z')]
for nm in ['x_le_ya', 'x_le_yc', 'xa_le_ya', 'Tx_le_ya', 'Nx_le_ya']:
    r2 = run(base2, [], (nm, 'y'))
    print(f"m={m}: {nm} (x -> y, position 2): {r2}", flush=True)
# at position 3 (y -> z): rename: use x:=y, p:=z  -> need predicates with 'y' in place of 'x'; do via a copy of PRED entries
PRED['y_le_za'] = (2, lambda c, p, u, v, w: [-c.E(c.i['y'], u, v), c.J(c.i['a'], c.i[p], u, v)])
print(f"m={m}: y_le_za (position 3): {run(base3, [], ('y_le_za', 'z'))}", flush=True)
# does x_le_ya follow from the five x-statements + x~y + y id + x id (no c~x)?
step = [('mt','a','c'), idf('x'), ('comm','x','y'), idf('y')]
five = ['pAC', 'aCP', 'Cin_T', 'Nin_N', 'cx_classes']
print(f"m={m}: five(x) + x~y + y id + x id => x_le_ya: {run(step, [(q, 'x') for q in five], ('x_le_ya', 'y'))}", flush=True)
print(f"m={m}: A(x) + x_le_ya => A(y) (sanity): {run(step, [('A', 'x'), ('x_le_ya', 'y')], ('A', 'y'))}", flush=True)
