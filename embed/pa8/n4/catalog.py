"""Pick the smallest m=5-valid explanation per candidate path from explain3b_all.log (+ explain3b_0.log), convert to
qi atoms, and check: violation of order-9 candidates / P_8's / embeddable census, validity at m=6."""
import sys, re, json, time
sys.path.insert(0, '/home/claude/pa8w/n4')
from checkK import fast_viol, census
from qi import valid
E = '/home/claude/pa8w/embed/pa8/'
def parse(body):
    atoms = [('mt','a','c'), ('mt','c','b')]
    for cl in body.split(' | '):
        mem = cl.split('=')
        def term(s):
            m = re.fullmatch(r'th_(\w)\((\w)\)', s); return (m.group(1), m.group(2)) if m else s
        ms = [term(s) for s in mem]
        base = next((s for s in ms if isinstance(s, str)), ms[0])
        for s in ms:
            if s != base: atoms.append(('eq', s, base))
    return atoms
txt = open('explain3b_all.log').read() + '##### 0 7 2 8\n' + open('explain3b_0.log').read()
chosen = {}
for block in txt.split('#####')[1:]:
    lines = block.strip().split('\n'); head = lines[0].strip()
    sets = [l.split(':  ')[1].split('   [')[0] for l in lines[1:] if 'valid m=5: True' in l]
    if not sets: continue
    def key(body):
        aux = set(ch for ch in re.findall(r'th_(\w)\(|\((\w)\)|\b([xyz])\b', body) for ch in ch if ch in 'xyz')
        return (len(aux), body.count('|'), len(body))
    sets.sort(key=key); chosen[head] = sets[0]
C9 = json.load(open(E + 'cand9.json'))
P8 = [json.loads(l)['A'] for l in open(E + 'post8.log') if json.loads(l).get('embeds') is None]
alg = census(); concl = ('mt','a','b')
for head, body in chosen.items():
    H = parse(body); vars_ = sorted({x for at in H for t in at[1:] for x in (t if isinstance(t, tuple) else (t,))})
    t = time.time()
    v9 = [k for k, T in enumerate(C9) if fast_viol(T, H, concl, vars_)]
    v8 = [k+1 for k, T in enumerate(P8) if fast_viol(T, H, concl, vars_)]
    bad = sum(1 for T in alg if fast_viol(T, H, concl, vars_))
    print(f"path {head}: {body}\n    violates cand9 {v9}, P8 {v8}, embeddable-census violations {bad} [{time.time()-t:.0f}s]", flush=True)
    t = time.time(); print(f"    valid m=6: {valid(H, concl, 6)} [{time.time()-t:.0f}s]", flush=True)
