import sys, time
sys.path.insert(0, '/home/claude/pa8w/n4'); sys.path.append('/home/claude/pa8w/embed')
from qi import valid
E = lambda p, q: (p, q); path = [('mt','a','c'), ('mt','c','b')]
base = [('comm','x','y'), ('comm','y','b'), ('comm','z','y'), ('comm','z','b'), ('eq',E('y','b'),E('z','b')), ('eq',E('z','x'),E('z','b')), ('eq',E('x','z'),E('x','y'))]
concl = ('eq', E('b','x'), E('y','b'))
variants = {
 'L*1 (no a,c)': base,
 'L*2 (+path, c~x, cx=xy, th_z(c)=zb)': path + base + [('comm','c','x'), ('eq',E('c','x'),E('x','y')), ('eq',E('z','c'),E('z','b'))],
 'L*3 (+path, th_x(a)=xy)': path + base + [('eq',E('x','a'),E('x','y'))],
 'L*4 (+path, th_x(a)=xy, c~x, cx=xy)': path + base + [('eq',E('x','a'),E('x','y')), ('comm','c','x'), ('eq',E('c','x'),E('x','y'))],
 'L*5 (+path, th_x(a)=xy, th_z(c)=zb, c~x)': path + base + [('eq',E('x','a'),E('x','y')), ('eq',E('z','c'),E('z','b')), ('comm','c','x')],
 'L*6 (+path, yb=th_b(a))': path + base + [('eq',E('y','b'),E('b','a'))],
 'L*7 (+path, yb=th_b(a), th_x(a)=xy)': path + base + [('eq',E('y','b'),E('b','a')), ('eq',E('x','a'),E('x','y'))],
 'L*8 (+path, yb=th_b(a), th_x(a)=xy, c~x, th_z(c)=zb)': path + base + [('eq',E('y','b'),E('b','a')), ('eq',E('x','a'),E('x','y')), ('comm','c','x'), ('eq',E('z','c'),E('z','b'))],
}
for name, hyps in variants.items():
    for m in (4, 5):
        t = time.time(); r = valid(hyps, concl, m)
        print('%-52s m=%d: %s (%.0fs)' % (name, m, r, time.time() - t), flush=True)
        if not r: break
