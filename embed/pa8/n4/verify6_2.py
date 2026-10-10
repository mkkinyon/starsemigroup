"""m=6 SAT check of the 2-path candidates valid at m<=5 (hits_5_2b.txt.valid.json), modulo path reversal and x<->y."""
import sys, os, json, time
os.environ['EMBED_DIR'] = '/home/claude/pa8w/embed'
sys.path.insert(0, '/home/claude/pa8w/embed/pa8'); sys.path.insert(0, '/home/claude/pa8w/n4')
from pc3_verify import valid
from pathclose4b import atoms_for, fmt
n = 2; A = atoms_for(n); idx = {a: i for i, a in enumerate(A)}
def rev(at):   # reverse the path p_i -> p_{n-i}
    r = lambda i: n - i
    if at[0] == 'ch': return ('ch', r(at[2]), r(at[1]))
    if at[0] in ('x', 'y'):
        if at[1] in ('comm', 'zle'): return (at[0], at[1], r(at[2]))
        return (at[0], at[1]) + tuple(sorted((r(at[2]), r(at[3]))))
    k = at[1]
    if k in ('comm', 'xley', 'ylex'): return at
    if k in ('sees', 'seen'): return ('xy', k, r(at[2]))
    return ('xy', k, r(at[2]), r(at[3]))
def swap(at):
    sw = {'x': 'y', 'y': 'x'}
    if at[0] in ('x', 'y'): return (sw[at[0]],) + at[1:]
    if at[0] == 'xy':
        if at[1] == 'xley': return ('xy', 'ylex')
        if at[1] == 'ylex': return ('xy', 'xley')
        if at[1] in ('xsees', 'xseen'): return ('xy', at[1], at[3], at[2])
    return at
def canon(h):
    forms = []
    for f in (lambda a: a, rev, swap, lambda a: swap(rev(a))):
        forms.append(tuple(sorted(idx[f(A[k])] for k in h)))
    return min(forms)
cands = {canon(h) for h, v in json.load(open('hits_5_2b.txt.valid.json'))}
cands = sorted(cands, key=lambda h: (len(h), h))
print(len(cands), "candidates modulo symmetry", flush=True)
for h in cands:
    H = [A[k] for k in h]; s = ', '.join(fmt(a) for a in H); t = time.time()
    v = valid(H, n, 6)
    print(f"{'VALID' if v else 'FAILS'} m=6: {s}  ({time.time()-t:.0f}s)", flush=True)
