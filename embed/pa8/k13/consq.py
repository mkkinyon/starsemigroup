"""SAT-verify the consequence atoms found in P_4 (recon_COND_4.pkl) at m = 4, 5, 6. Usage: python3 consq.py COND"""
import sys, pickle, re, time
sys.path.append('/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import valid
exec(open('satdrop.py').read().split("path = ")[0].split("m = int")[1].split("\n",1)[1])
name = sys.argv[1]; d = pickle.load(open('recon_%s_4.pkl' % name, 'rb'))
terms = d['terms']; cons = [(terms[i], terms[j]) for i, j in d['cons']]
def term(s):
    m = re.fullmatch(r'th_(\w)\((\w)\)', s); return (m.group(1), m.group(2)) if m else s
def trivial(s, t):
    ts, tt = term(s), term(t)
    if isinstance(tt, tuple) and tt[0] == tt[1] == ts: return True      # p = th_p(p)
    if isinstance(ts, tuple) and ts[0] == ts[1] == tt: return True
    return False
atoms = [h[1] for h in C[name]] + [('mt','a','c'), ('mt','c','b')]
cands = [(s, t) for s, t in cons if not trivial(s, t)]
print(name, len(cands), 'candidate consequence atoms from P_4 sample', flush=True)
alive = cands
for m in (4, 5):
    nxt = []
    for s, t in alive:
        ts, tt = term(s), term(t)
        if ts == 'u': ts = ('a','b')
        if ts == 'v': ts = ('b','a')
        if tt == 'u': tt = ('a','b')
        if tt == 'v': tt = ('b','a')
        t0 = time.time(); r = valid(atoms, ('eq', ts, tt), m)
        if r: nxt.append((s, t))
        else: print('  fails at m=%d: %s=%s (%.0fs)' % (m, s, t, time.time() - t0), flush=True)
    alive = nxt
    print('m=%d: %d consequence atoms hold:' % (m, len(alive)), '; '.join('%s=%s' % a for a in alive), flush=True)
