import sys, time
sys.path.insert(0, '/home/claude/pa8w/n4'); sys.path.append('/home/claude/pa8w/embed')
from qi import valid
E = lambda p, q: (p, q); path = [('mt','a','c'), ('mt','c','b')]
K1d = [('eq',E('a','b'),E('a','x')), ('eq',E('y','a'),E('y','z')), ('comm','c','x'), ('comm','b','z'), ('comm','x','y'), ('le','z','y'), ('fix','b','x')]
core = K1d[:-1]
for m in (4, 5, 6):
    t = time.time(); print('core => th_b(x)=th_b(a) at m=%d:' % m, valid(path + core, ('eq', E('b','x'), E('b','a')), m), '(%.0fs)' % (time.time()-t), flush=True)
for m in (4, 5):
    for h in core:
        t = time.time(); print('   core minus', h, '=> th_b(x)=th_b(a) at m=%d:' % m, valid(path + [g for g in core if g is not h], ('eq', E('b','x'), E('b','a')), m), flush=True)
