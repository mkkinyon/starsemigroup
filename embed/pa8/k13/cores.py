"""The identification cores of K1b, K1c, K3b (each condition = core + one half-matching + friends/descent):
validity at m = 4,5,6 and single-hypothesis drops at m = 5."""
import sys, time
sys.path.append('/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import valid
exec(open('satdrop.py').read().split("path = ")[0].split("m = int")[1].split("\n",1)[1])
path = [('mt','a','c'), ('mt','c','b')]
cores = {
 'L1b': ([h for h in C['K1b'] if h[0] != 'aya=a'], ('eq', ('a','y'), ('a','b')), 'theta_a(y) = theta_a(b); then aya=a gives theta_a(b)=a'),
 'L1c': ([h for h in C['K1c'] if h[0] != 'bxb=b'], ('eq', ('b','x'), ('b','a')), 'theta_b(x) = theta_b(a); then bxb=b gives theta_b(a)=b'),
 'L3b': ([h for h in C['K3b'] if h[0] != 'byb=b'], ('eq', ('y','b'), ('a','b')), 'theta_y(b) = theta_a(b); then byb=b and friends give b><u, descent u=a'),
}
for name, (hyps, concl, text) in cores.items():
    print(name, ':', ', '.join(h[0] for h in hyps), '=>', text, flush=True)
    for m in (4, 5, 6):
        t = time.time(); r = valid(path + [h[1] for h in hyps], concl, m)
        print('   P_%d: %s (%.0fs)' % (m, 'HOLDS' if r else 'FAILS', time.time() - t), flush=True)
    for h in hyps:
        t = time.time(); r = valid(path + [g[1] for g in hyps if g is not h], concl, 5)
        print('   minus %-18s P_5: %s (%.0fs)' % (h[0], 'HOLDS' if r else 'FAILS', time.time() - t), flush=True)
