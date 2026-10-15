import sys, time
sys.path.append('/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import valid
m = int(sys.argv[1])
K4 = [('mt','a','c'), ('mt','c','b'), ('fix','a','y'), ('le','b','z'), ('comm','y','c'), ('eq',('z','y'),('b','a')), ('eq',('z','a'),('a','b'))]
t = time.time(); r = valid(K4, ('mt','a','b'), m, verbose=True)
print('K4 in P_%d: %s (%.0fs)' % (m, 'HOLDS' if r else 'FAILS', time.time() - t), flush=True)
