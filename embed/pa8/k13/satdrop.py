"""SAT dropped-hypothesis map for K1a..K3c in P(P_m): validity of the condition and of each single-hypothesis drop.
Usage: python3 satdrop.py m [COND ...]   (appends to satdrop_m.log; skips checks already logged)"""
import sys, time, os
sys.path.append('/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import valid
m = int(sys.argv[1]); which = sys.argv[2:]
E = lambda p, q: (p, q)
C = {
 'K1a': [('aya=a', ('fix','a','y')), ('th_y(b)=th_z(x)', ('eq',E('y','b'),E('z','x'))), ('th_x(b)=u', ('eq',E('x','b'),E('a','b'))),
         ('u=v', ('comm','a','b')), ('th_c(z)=th_x(z)', ('eq',E('c','z'),E('x','z')))],
 'K1b': [('aya=a', ('fix','a','y')), ('th_z(c)=b', ('eq',E('z','c'),'b')), ('th_y(a)=th_y(x)', ('eq',E('y','a'),E('y','x'))),
         ('th_x(c)=u', ('eq',E('x','c'),E('a','b'))), ('th_z(x)=u', ('eq',E('z','x'),E('a','b'))), ('th_y(z)=v', ('eq',E('y','z'),E('b','a')))],
 'K1c': [('bxb=b', ('fix','b','x')), ('th_y(a)=th_z(y)', ('eq',E('y','a'),E('z','y'))), ('th_c(z)=th_x(a)', ('eq',E('c','z'),E('x','a'))),
         ('th_x(a)=th_y(x)', ('eq',E('x','a'),E('y','x'))), ('th_z(x)=v', ('eq',E('z','x'),E('b','a')))],
 'K3a': [('th_z(c)=a', ('eq',E('z','c'),'a')), ('byb=b', ('fix','b','y')), ('th_x(c)=th_x(y)', ('eq',E('x','c'),E('x','y'))),
         ('th_y(b)=th_y(x)', ('eq',E('y','b'),E('y','x'))), ('th_x(b)=u', ('eq',E('x','b'),E('a','b'))), ('u=v', ('comm','a','b')), ('yz=zy', ('comm','y','z'))],
 'K3b': [('th_x(c)=a', ('eq',E('x','c'),'a')), ('byb=b', ('fix','b','y')), ('bzb=b', ('fix','b','z')), ('th_y(c)=th_y(b)', ('eq',E('y','c'),E('y','b'))),
         ('th_z(c)=th_z(b)', ('eq',E('z','c'),E('z','b'))), ('th_y(z)=u', ('eq',E('y','z'),E('a','b'))), ('th_z(y)=u', ('eq',E('z','y'),E('a','b'))), ('th_x(b)=v', ('eq',E('x','b'),E('b','a')))],
 'K3c': [('bxb=b', ('fix','b','x')), ('th_x(a)=th_x(b)', ('eq',E('x','a'),E('x','b'))), ('th_x(y)=th_y(z)', ('eq',E('x','y'),E('y','z'))),
         ('th_z(y)=u', ('eq',E('z','y'),E('a','b'))), ('u=v', ('comm','a','b')), ('zc=cz', ('comm','z','c'))],
}
path = [('mt','a','c'), ('mt','c','b')]; concl = ('mt','a','b')
logf = 'satdrop_%d.log' % m
done = set(l.split('|')[0].strip() for l in open(logf)) if os.path.exists(logf) else set()
for name in (which or list(C)):
    hyps = C[name]
    for drop in [None] + [h[0] for h in hyps]:
        key = '%s minus %s' % (name, drop) if drop else '%s full' % name
        if key in done: continue
        atoms = path + [h[1] for h in hyps if h[0] != drop]
        t = time.time(); r = valid(atoms, concl, m)
        line = '%s | %s in P_%d (%.0fs)' % (key, 'HOLDS' if r else 'FAILS', m, time.time() - t)
        print(line, flush=True); open(logf, 'a').write(line + '\n')
