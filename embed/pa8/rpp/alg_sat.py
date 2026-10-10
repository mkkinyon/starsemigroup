"""SAT check in P(P_m) of algebraic consequences of the (R'') hypotheses."""
import sys, time
sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import valid
H = [('mt','a','c'), ('mt','c','b'), ('comm','x','c'), ('eq',('x','a'),('x','c')), ('comm','y','b'), ('eq',('x','b'),('y','a'))]
m = int(sys.argv[1])
tests = {'xb=bx': ('comm','x','b'), 'cy=yc': ('comm','c','y'), 'th_x(b)=th_x(c)': ('eq',('x','b'),('x','c')),
         'th_y(b)=th_x(c)': ('eq',('y','b'),('x','c')), 'th_y(a)=th_x(c)': ('eq',('y','a'),('x','c')), 'a~b': ('mt','a','b')}
for name, c in tests.items():
    t = time.time(); print(f"m={m} {name}: {valid(H, c, m)} ({time.time()-t:.0f}s)", flush=True)
