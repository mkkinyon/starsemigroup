"""The modules of the (W_2) proof plan, as SAT implications.  Usage: python3 modules.py m [module ...]"""
import sys, time
m_arg = sys.argv[1]; which = sys.argv[2:]
sys.argv = ['x', m_arg]
exec(open('endstep.py').read().split("I12 = ")[0])      # PRED (incl. L1', G2abc, Cmeet), run, run2, Ctx, make_J3, idf
PRED['Np_cblock'] = (2, lambda c, p, u, v, w: [-c.E(c.i[p], u, v), c.Tl(c.i[p], u), c.Tl(c.i['c'], u), c.E(c.i['c'], u, v)])
PRED['Cin_T'] = (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), -c.Tl(c.i['c'], u), c.Tl(c.i[p], u), c.E(c.i[p], u, v)])
PRED['Nin_N'] = (2, lambda c, p, u, v, w: [-c.E(c.i['c'], u, v), c.Tl(c.i['c'], u), c.Tl(c.i[p], u), c.E(c.i[p], u, v)])
PRED['cx_classes'] = (2, lambda c, p, u, v, w: [-c.J(c.i['c'], c.i[p], u, v), c.Tl(c.i[p], u), c.Tl(c.i['c'], u), c.E(c.i['c'], u, v)])
step = [('mt','a','c'), idf('x'), ('comm','x','y'), idf('y')]
end = [('mt','a','c'), ('mt','c','b'), ('comm','y','b'), idf('y')]
five = ['A', 'pAC', 'aCP', 'N2', "G2'"]
MOD = {
 'M2':  (step, [('A','x'), ('M','x'), ('Np_cblock','x')], ('A','y'), run),
 'M3a': (step, [('A','x'), ('M','x')], ('M','y'), run),
 'M3b': (step, [('A','x'), ('M','x')], ('pAC','y'), run),
 'M3c': (step, [('A','x'), ('M','x')], ('aCP','y'), run),
 'M4':  (step, [('N2','x'), ('S','x')], ('N2','y'), run),
 'M5':  (step, [(q, 'x') for q in ['a_Gamma', 'A', 'M', "G2'", "G2'a", 'N1', 'N2', 'S', 'pAC', 'aCP', 'Np_cblock', 'Cin_T', 'Nin_N', 'cx_classes']], ("G2'",'y'), run),
 'M6a': (end, [(q, 'y') for q in five], ('A','b'), run2),
 'M6b': (end, [(q, 'y') for q in five], ('G2abc','b'), run2),
}
for name in (which or MOD):
    H, hy, g, f = MOD[name]; t = time.time(); r = f(H, hy, g)
    print(f"m={m}: {name}: {r} ({time.time()-t:.0f}s)", flush=True)
