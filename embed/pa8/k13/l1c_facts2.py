import sys, time
sys.path.insert(0, '/home/claude/pa8w/n4'); sys.path.append('/home/claude/pa8w/embed')
from qi import valid
E = lambda p, q: (p, q); path = [('mt','a','c'), ('mt','c','b')]
core = [('eq','u',E('a','b')), ('eq','v',E('b','a')), ('eq','w',E('x','a')), ('eq','r',E('y','a')), ('eq',E('y','a'),E('z','y')), ('eq',E('c','z'),E('x','a')), ('eq',E('x','a'),E('y','x')), ('eq',E('z','x'),E('b','a'))]
tests = [('th_a(x)=u', ('eq',E('a','x'),E('a','b'))), ('th_b(z)=v', ('eq',E('b','z'),E('b','a'))), ('th_y(b)=v', ('eq',E('y','b'),E('b','a'))),
         ('th_z(a)=v', ('eq',E('z','a'),E('b','a'))), ('th_z(a)=r', ('eq',E('z','a'),E('y','a'))), ('th_c(y)=w', ('eq',E('c','y'),E('x','a'))),
         ('th_x(z)=w', ('eq',E('x','z'),E('x','a'))), ('th_a(y)=u', ('eq',E('a','y'),E('a','b'))), ('th_a(z)=u', ('eq',E('a','z'),E('a','b'))),
         ('th_b(y)=v', ('eq',E('b','y'),E('b','a'))), ('th_c(x)=w', ('eq',E('c','x'),E('x','a'))), ('r<=y', ('le','r','y')),
         ('v<=r', ('le','v','r')), ('th_y(v)=v', ('le','v','y')), ('w<=z?', ('le','w','z')),
         ('th_z(w)=v', ('eq',E('z','w'),'v')), ('th_x(v)=w', ('eq',E('x','v'),'w')), ('th_b(w)=v', ('eq',E('b','w'),'v'))]
for m in (4, 5, 6):
    for name, concl in tests:
        t = time.time(); r = valid(path + core, concl, m)
        print('m=%d core => %-12s %s (%.0fs)' % (m, name, r, time.time() - t), flush=True)
