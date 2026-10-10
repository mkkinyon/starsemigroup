import sys, time
sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import valid
P = [('mt','a','c'), ('mt','c','b'), ('comm','x','c'), ('eq',('x','a'),('x','c')), ('comm','x','z'), ('eq',('z','a'),('z','c')), ('comm','y','a'), ('eq',('z','b'),('y','b'))]
for m in (5,6):
    t=time.time(); print(f"(R'_2) valid in P(P_{m}):", valid(P, ('mt','a','b'), m), f"({time.time()-t:.0f}s)", flush=True)
