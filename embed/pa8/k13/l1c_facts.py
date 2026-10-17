import sys, time
sys.path.insert(0, '/home/claude/pa8w/n4'); sys.path.append('/home/claude/pa8w/embed')
from qi import valid
E = lambda p, q: (p, q); path = [('mt','a','c'), ('mt','c','b')]
H = {'yz': ('eq',E('y','a'),E('z','y')), 'cx': ('eq',E('c','z'),E('x','a')), 'xy': ('eq',E('x','a'),E('y','x')), 'zv': ('eq',E('z','x'),E('b','a'))}
tests = [
 ('th_z(x)=v => b~z', ['zv'], ('comm','b','z')),
 ('th_z(x)=v => th_b(z)=v', ['zv'], ('eq',E('b','z'),E('b','a'))),
 ('th_z(x)=v => th_a(x)=u', ['zv'], ('eq',E('a','x'),E('a','b'))),
 ('cx,zv => th_z(c)=v', ['cx','zv'], ('eq',E('z','c'),E('b','a'))),
 ('cx => c~x', ['cx'], ('comm','c','x')),
 ('xy => x~y', ['xy'], ('comm','x','y')),
 ('cx,xy => c~y', ['cx','xy'], ('comm','c','y')),
 ('yz,cx,xy => th_c(y)=w', ['yz','cx','xy'], ('eq',E('c','y'),E('x','a'))),
 ('yz,xy,zv => b~y', ['yz','xy','zv'], ('comm','b','y')),
 ('yz,xy,zv => th_y(b)=v', ['yz','xy','zv'], ('eq',E('y','b'),E('b','a'))),
 ('yz,xy,zv => th_x(z)=w', ['yz','xy','zv'], ('eq',E('x','z'),E('x','a'))),
 ('yz => y~z', ['yz'], ('comm','y','z')),
]
for m in (4, 5):
    for name, hs, concl in tests:
        t = time.time(); r = valid(path + [H[h] for h in hs], concl, m)
        print('m=%d %-28s %s (%.0fs)' % (m, name, r, time.time() - t), flush=True)
