import sys, time
sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import valid
B3 = [('mt','a','d'), ('mt','d','b'), ('comm','h','d'), ('eq',('h','a'),('h','d')), ('comm','i','b'), ('eq',('h','b'),('i','a'))]
t = time.time(); print("B3 valid m=7:", valid(B3, ('mt','a','b'), 7), f"{time.time()-t:.0f}s", flush=True)
