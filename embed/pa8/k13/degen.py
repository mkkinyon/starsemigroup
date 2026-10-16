import sys, time
sys.path.append('/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import valid
exec(open('satdrop.py').read().split("path = ")[0].split("m = int")[1].split("\n",1)[1])
path = [('mt','a','c'), ('mt','c','b')]
for m in (4, 5):
    for name, hyps in C.items():
        atoms = path + [h[1] for h in hyps]
        t = time.time(); r = valid(atoms, ('eq', 'a', 'b'), m)
        print('%s => a=b in P_%d: %s (%.0fs)' % (name, m, r, time.time() - t), flush=True)
