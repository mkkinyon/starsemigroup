import sys, time
sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import valid
H = [('mt','a','c'), ('mt','c','b'), ('comm','x','c'), ('eq',('x','a'),('x','c')), ('comm','y','b'), ('eq',('x','b'),('y','a'))]
tests = {'th_y(c)=th_y(a)': ('eq',('y','c'),('y','a')), 'th_c(y)=th_c(x)': ('eq',('c','y'),('c','x')), 'th_b(y)=th_b(x)': ('eq',('b','y'),('b','x')),
         'u~w': None}
for m in (6, 7):
    for name, c in tests.items():
        if c is None: continue
        t = time.time(); print(f"m={m} {name}: {valid(H, c, m)} ({time.time()-t:.0f}s)", flush=True)
