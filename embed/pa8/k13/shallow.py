"""For each consequence atom (consq_COND.log, m=5 survivors) and each hypothesis h: does the atom follow from the
other hypotheses in P(P_4) (SAT)?  Prints, per atom, the hypotheses it needs.  Usage: python3 shallow.py COND"""
import sys, re, time
sys.path.append('/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import valid
exec(open('satdrop.py').read().split("path = ")[0].split("m = int")[1].split("\n",1)[1])
name = sys.argv[1]; m = int(sys.argv[2]) if len(sys.argv) > 2 else 4
line = [l for l in open('consq_%s.log' % name) if l.startswith('m=5:')][-1]
atoms_s = line.split('hold: ')[1].strip().split('; ')
def term(s):
    mm = re.fullmatch(r'th_(\w)\((\w)\)', s)
    if mm: return (mm.group(1), mm.group(2))
    return {'u': ('a','b'), 'v': ('b','a')}.get(s, s)
def pretty(s, t):
    for p, q in [(s, t), (t, s)]:
        mm = re.fullmatch(r'th_(\w)\((\w)\)', q)
        if mm and p in 'abcxyz' and not mm.group(1) == mm.group(2) == p:
            if mm.group(1) == p: return f'th_{p}({mm.group(2)})={p}'
            if mm.group(2) == p: return f'{p}<={mm.group(1)}'
    m1 = re.fullmatch(r'th_(\w)\((\w)\)', s); m2 = re.fullmatch(r'th_(\w)\((\w)\)', t)
    if m1 and m2 and m1.group(1) == m2.group(2) and m1.group(2) == m2.group(1): return f'{m1.group(1)}~{m1.group(2)}'
    return f'{s}={t}'
path = [('mt','a','c'), ('mt','c','b')]; hyps = C[name]
t0 = time.time(); rows = []
for a in atoms_s:
    s, t = a.split('=')
    if re.fullmatch(r'th_(\w)\(\1\)', t) and t[3] == s: continue
    concl = ('eq', term(s), term(t)); need = []
    for h in hyps:
        others = path + [g[1] for g in hyps if g is not h]
        if not valid(others, concl, m): need.append(h[0])
    rows.append((pretty(s, t), need))
rows.sort(key=lambda r: (len(r[1]), r[0]))
print('%s in P_%d: %d consequence atoms; hypotheses each one needs (%.0fs)' % (name, m, len(rows), time.time() - t0))
for p, need in rows: print('  %-18s needs %s' % (p, 'ALL' if len(need) == len(hyps) else (need or 'none (path only)')))
